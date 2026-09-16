"""
Bilingual content translation service.

Canonical source: English fields. Arabic fields (`*_ar`) are stored side-by-side
in the same record and remain admin-editable at all times.

Behavior:
- When an Arabic field is blank, the public API translates the English source
  (LibreTranslate-compatible `TRANSLATION_API_URL`, then MyMemory as free
  fallback) and the result is PERSISTED to the model field and marked
  machine-generated in the model's `ar_is_machine` JSON registry
  ({ar_field_name: True}). Missing/False means human-reviewed Arabic.
- Provider results are cached in the shared Django cache (Redis when REDIS_URL
  is configured) for `TRANSLATION_CACHE_TTL` seconds.
- FAILED translations are NEVER cached or persisted as English — a failure is
  only marked with a short-lived marker (FAILURE_CACHE_TTL) so the next read
  or the retry endpoint can call the provider again.
- Human Arabic entered by an admin is never overwritten by the machine;
  overwriting requires the explicit force flags on `retranslate_object`.
- `clear_translation_cache` / `invalidate_object_translations` invalidate cache
  entries when English or Arabic source content changes (wired via pre_save
  signals in models.py).
"""
import hashlib
import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Kept for backwards compatibility; the live TTL now comes from settings.
CACHE_TTL = getattr(settings, "TRANSLATION_CACHE_TTL", 60 * 60 * 24 * 30)

# Short TTL for the "we could not translate this right now" marker so failed
# lookups are retried soon instead of being remembered as English for a month.
FAILURE_CACHE_TTL = 60  # seconds

# Global circuit breaker: after a provider failure, skip all network calls for
# this long so bulk saves/reads with a dead provider don't stall the app.
PROVIDER_DOWN_TTL = 30  # seconds

DEFAULT_TIMEOUT = 5

# Name of the JSONField on translatable models that records which Arabic
# fields were machine-generated. A model-level equivalent of per-field
# `<field>_ar_is_machine` flags (single column instead of dozens).
MACHINE_FLAG_FIELD = "ar_is_machine"


def _cache_backend():
    """The shared Django cache (Redis when configured, locmem otherwise)."""
    return cache


def _cache_key(text: str, source: str, target: str) -> str:
    h = hashlib.md5(f"{source}:{target}:{text}".encode("utf-8")).hexdigest()
    return f"translate:{h}"


def _failure_cache_key(text: str, source: str, target: str) -> str:
    h = hashlib.md5(f"{source}:{target}:{text}".encode("utf-8")).hexdigest()
    return f"translate:failed:{h}"


def _is_arabic(text: str) -> bool:
    if not text:
        return False
    arabic = sum(1 for c in text if "\u0600" <= c <= "\u06FF")
    return arabic / max(len(text), 1) > 0.3


def _translate_via_libre(text: str, source: str, target: str) -> str | None:
    url = getattr(settings, "TRANSLATION_API_URL", "") or ""
    if not url:
        return None
    try:
        resp = requests.post(
            url,
            json={"q": text, "source": source, "target": target, "format": "text"},
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.ok:
            data = resp.json()
            t = data.get("translatedText") or data.get("translation")
            if t and str(t).strip():
                return str(t).strip()
    except Exception as e:
        logger.debug("LibreTranslate failed: %s", e)
    return None


def _translate_via_mymemory(text: str, source: str, target: str) -> str | None:
    try:
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"{source}|{target}"},
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.ok:
            data = resp.json()
            translated = (data.get("responseData") or {}).get("translatedText")
            # MyMemory returns the original text on failure; detect via the
            # warning marker or by comparing against the source.
            if translated and "MYMEMORY WARNING" not in translated and translated.strip() != text.strip():
                return translated.strip()
            # Even if identical, accept it when it actually looks Arabic.
            if translated and _is_arabic(translated):
                return translated.strip()
    except Exception as e:
        logger.debug("MyMemory translate failed: %s", e)
    return None


def _translate_via_google_gtx(text: str, source: str = "en", target: str = "ar") -> str | None:
    try:
        resp = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text},
            timeout=DEFAULT_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        if resp.ok:
            data = resp.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                translated = "".join(part[0] for part in data[0] if part and len(part) > 0 and part[0])
                if translated and translated.strip():
                    return translated.strip()
    except Exception as e:
        logger.debug("Google GTX translate failed: %s", e)
    return None


def _call_providers(text: str, source: str, target: str) -> str | None:
    """Call translation providers in order: LibreTranslate -> Google GTX -> MyMemory."""
    res = _translate_via_libre(text, source, target)
    if res:
        return res
    res = _translate_via_google_gtx(text, source, target)
    if res:
        return res
    res = _translate_via_mymemory(text, source, target)
    if res:
        return res
    return None


def _mark_failure(text: str, source: str, target: str) -> None:
    """Remember a failure briefly so consecutive requests don't hammer providers."""
    try:
        _cache_backend().set(
            _failure_cache_key(text, source, target), True, FAILURE_CACHE_TTL
        )
    except Exception:
        pass


def _recently_failed(text: str, source: str, target: str) -> bool:
    try:
        return bool(_cache_backend().get(_failure_cache_key(text, source, target)))
    except Exception:
        return False


def _provider_down_key() -> str:
    return "translate:provider:down"


def _mark_provider_down() -> None:
    try:
        _cache_backend().set(_provider_down_key(), True, PROVIDER_DOWN_TTL)
    except Exception:
        pass


def _provider_down() -> bool:
    try:
        return bool(_cache_backend().get(_provider_down_key()))
    except Exception:
        return False


def clear_failure_marker(text: str, source: str = "en", target: str = "ar") -> None:
    """Drop the short-lived failure marker for a text (used before retries)."""
    try:
        _cache_backend().delete(_failure_cache_key(text, source, target))
    except Exception:
        pass


def clear_provider_down_marker() -> None:
    """Reset the global circuit breaker (used by the retry endpoint/tests)."""
    try:
        _cache_backend().delete(_provider_down_key())
    except Exception:
        pass


def reset_failure_state() -> None:
    """Clear every failure marker + the circuit breaker, keeping success cache.

    Called by the admin retry endpoint so a retranslation attempt genuinely
    reaches the provider again even if it failed moments earlier.
    """
    try:
        _cache_backend().delete_pattern("translate:failed:*")
    except Exception:
        pass
    clear_provider_down_marker()


def clear_translation_cache(text: str | None = None, source: str = "en", target: str = "ar") -> None:
    """Invalidate the cache entry for `text` (or all `translate:*` entries)."""
    backend = _cache_backend()
    try:
        if text:
            backend.delete(_cache_key(text, source, target))
            clear_failure_marker(text, source, target)
        else:
            backend.delete_pattern("translate:*")
    except Exception as e:
        logger.debug("clear_translation_cache failed: %s", e)


def translate_text(text: str, source: str = "en", target: str = "ar") -> str:
    """Translate `text` bidirectionally with caching and graceful fallback.

    Returns source text when translation fails (never blank) but NEVER caches
    that fallback as a successful translation.
    """
    if not text or not text.strip():
        return ""
    if target == "ar" and _is_arabic(text):
        return text
    if target == "en" and not _is_arabic(text):
        return text
    if not getattr(settings, "TRANSLATION_ENABLED", True):
        return text

    ttl = getattr(settings, "TRANSLATION_CACHE_TTL", CACHE_TTL)
    key = _cache_key(text, source, target)
    try:
        cached = _cache_backend().get(key)
    except Exception:
        cached = None
    if cached:
        return cached

    if _recently_failed(text, source, target) or _provider_down():
        return text

    result = _call_providers(text, source, target)
    if not result:
        _mark_failure(text, source, target)
        _mark_provider_down()
        return text  # fallback: return source text, do NOT cache it as success

    try:
        _cache_backend().delete(_provider_down_key())
    except Exception:
        pass

    try:
        _cache_backend().set(key, result, ttl)
    except Exception:
        pass
    return result


def get_translated(value_ar: str | None, value_en: str | None, target: str = "ar") -> str:
    """Return the value for the requested locale (bidirectional).

    - target == "ar": Arabic if present, else auto-translate English source.
    - target == "en": English if present, else auto-translate Arabic source.
    """
    if target == "ar":
        if value_ar and value_ar.strip():
            return value_ar
        if value_en and value_en.strip():
            return translate_text(value_en, source="en", target="ar")
        return value_ar or value_en or ""
    else:
        if value_en and value_en.strip():
            return value_en
        if value_ar and value_ar.strip():
            return translate_text(value_ar, source="ar", target="en")
        return value_en or value_ar or ""


# ---------------------------------------------------------------------------
# Persistence layer: translate once, then store the result on the model record
# and mark it machine-generated so it is never confused with human entries.
# ---------------------------------------------------------------------------

def _registry_get(instance, ar_field: str) -> bool:
    reg = getattr(instance, MACHINE_FLAG_FIELD, None)
    return bool(reg.get(ar_field)) if isinstance(reg, dict) else False


def _registry_set(instance, ar_field: str, value: bool) -> dict:
    reg = getattr(instance, MACHINE_FLAG_FIELD, None)
    reg = dict(reg) if isinstance(reg, dict) else {}
    if value:
        reg[ar_field] = True
    else:
        reg.pop(ar_field, None)
    setattr(instance, MACHINE_FLAG_FIELD, reg)
    return reg


def persist_translation(
    instance,
    en_field: str,
    ar_field: str,
    source: str = "en",
    target: str = "ar",
    force: bool = False,
    force_human: bool = False,
) -> str:
    """Translate between `en_field` and `ar_field` on `instance` and persist.

    Rules:
    - Automatically detects wrong-field content (e.g. Arabic entered in English field)
      and safely populates the opposite language without destroying original content.
    - Never overwrites non-blank target content unless force or force_human is enabled.
    - Updates DB via queryset.update() to avoid signal recursion.
    """
    en_value = str(getattr(instance, en_field, None) or "")
    ar_value = str(getattr(instance, ar_field, None) or "")

    # Check for wrong field placement (Arabic in English field or English in Arabic field)
    en_is_ar = _is_arabic(en_value)
    ar_is_en = bool(ar_value.strip()) and not _is_arabic(ar_value)

    db_updates = {}
    registry = dict(getattr(instance, MACHINE_FLAG_FIELD, None) or {})

    # Case 1: Arabic entered into English field
    if en_is_ar:
        if not ar_value.strip() or force or force_human:
            ar_value = en_value
            setattr(instance, ar_field, ar_value)
            db_updates[ar_field] = ar_value
        translated_en = translate_text(en_value, source="ar", target="en")
        if translated_en and translated_en != en_value:
            setattr(instance, en_field, translated_en)
            db_updates[en_field] = translated_en
            registry[en_field + "_is_machine"] = True

    # Case 2: English entered into Arabic field
    elif ar_is_en:
        if not en_value.strip() or force or force_human:
            en_value = ar_value
            setattr(instance, en_field, en_value)
            db_updates[en_field] = en_value
        translated_ar = translate_text(ar_value, source="en", target="ar")
        if translated_ar and translated_ar != ar_value:
            setattr(instance, ar_field, translated_ar)
            db_updates[ar_field] = translated_ar
            registry[ar_field] = True

    # Case 3: English present, Arabic blank
    elif en_value.strip() and not ar_value.strip():
        result = translate_text(en_value, source="en", target="ar")
        if result and result.strip() != en_value.strip():
            ar_value = result
            setattr(instance, ar_field, result)
            db_updates[ar_field] = result
            registry[ar_field] = True

    # Case 4: Arabic present, English blank
    elif ar_value.strip() and not en_value.strip():
        result = translate_text(ar_value, source="ar", target="en")
        if result and result.strip() != ar_value.strip():
            en_value = result
            setattr(instance, en_field, result)
            db_updates[en_field] = result
            registry[en_field + "_is_machine"] = True

    # Case 5: Both present - forced regeneration
    elif en_value.strip() and ar_value.strip():
        is_machine = registry.get(ar_field, False)
        if (is_machine and (force or force_human)) or (not is_machine and force_human):
            result = translate_text(en_value, source="en", target="ar")
            if result and result.strip() != en_value.strip():
                ar_value = result
                setattr(instance, ar_field, result)
                db_updates[ar_field] = result
                registry[ar_field] = True

    if db_updates:
        setattr(instance, MACHINE_FLAG_FIELD, registry)
        db_updates[MACHINE_FLAG_FIELD] = registry
        if getattr(instance, "pk", None):
            type(instance).objects.filter(pk=instance.pk).update(**db_updates)

    if target == "en":
        return getattr(instance, en_field, "") or ar_value
    return getattr(instance, ar_field, "") or en_value


def retranslate_object(instance, force: bool = False, force_human: bool = False) -> dict:
    """Re-run machine translation for every translatable field on `instance`.

    Returns {ar_field: value_after_call}.
    """
    from .models import TRANSLATABLE_FIELDS

    results = {}
    for en_field, ar_field in TRANSLATABLE_FIELDS.get(type(instance).__name__, []):
        en_value = str(getattr(instance, en_field, None) or "")
        current_ar = str(getattr(instance, ar_field, None) or "")
        if not current_ar.strip() or not en_value.strip() or _is_arabic(en_value) or not _is_arabic(current_ar):
            results[ar_field] = persist_translation(instance, en_field, ar_field, force=force, force_human=force_human)
            continue
        is_machine = _registry_get(instance, ar_field)
        if (is_machine and (force or force_human)) or (not is_machine and force_human):
            if en_value.strip():
                clear_translation_cache(en_value)
            results[ar_field] = persist_translation(instance, en_field, ar_field, force=True, force_human=force_human)
        else:
            results[ar_field] = current_ar
    return results


def invalidate_object_translations(instance) -> None:
    """Invalidate cached translations for every English & Arabic field on `instance`."""
    from .models import TRANSLATABLE_FIELDS, TRANSLATABLE_JSON_FIELDS

    for en_field, ar_field in TRANSLATABLE_FIELDS.get(type(instance).__name__, []):
        en_value = getattr(instance, en_field, None)
        ar_value = getattr(instance, ar_field, None)
        if en_value:
            clear_translation_cache(str(en_value), "en", "ar")
        if ar_value:
            clear_translation_cache(str(ar_value), "ar", "en")

    for json_field in TRANSLATABLE_JSON_FIELDS.get(type(instance).__name__, []):
        value = getattr(instance, json_field, None)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    clear_translation_cache(item, "en", "ar")
                    clear_translation_cache(item, "ar", "en")


def is_machine_generated(instance, ar_field: str) -> bool:
    """Public helper: is the Arabic in `ar_field` machine-generated?"""
    has_ar = bool(str(getattr(instance, ar_field, "") or "").strip())
    return has_ar and _registry_get(instance, ar_field)

