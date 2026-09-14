"""
Auto-translation helper.

If admin leaves an *_ar field blank, the public API auto-translates the English
source on the fly so the user panel is 100% Arabic when locale=ar.

Industry pattern (single DB, bilingual columns + runtime fallback) — same as
WooCommerce Polylang, Strapi i18n, Contentful fallback-locale:
- Store EN + AR side-by-side in one DB.
- When AR is blank, translate EN → AR at read time, optionally persisting.

Provider priority:
  1) LibreTranslate / custom URL via TRANSLATION_API_URL (if set)
  2) MyMemory free API (no key, best-effort)
  3) Fallback: return original English (never blank)

Set TRANSLATION_ENABLED=false to disable network calls and return English.
"""
import logging
import hashlib
from functools import lru_cache

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_TTL = 60 * 60 * 24 * 30  # 30 days


def _is_arabic(text: str) -> bool:
    if not text:
        return False
    # if >30% chars are Arabic unicode, treat as already Arabic
    arabic = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return arabic / max(len(text), 1) > 0.3


def _cache_key(text: str, source: str, target: str) -> str:
    h = hashlib.md5(f"{source}:{target}:{text}".encode("utf-8")).hexdigest()
    return f"translate:{h}"


@lru_cache(maxsize=2048)
def _translate_via_mymemory(text: str, source: str = "en", target: str = "ar") -> str | None:
    try:
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"{source}|{target}"},
            timeout=4,
        )
        if resp.ok:
            data = resp.json()
            translated = (data.get("responseData") or {}).get("translatedText")
            # MyMemory returns original on failure; detect by checking if it contains "MYMEMORY WARNING"
            if translated and "MYMEMORY WARNING" not in translated and translated.strip() != text.strip():
                return translated.strip()
            # Even if same, still return it if it looks Arabic
            if translated and _is_arabic(translated):
                return translated.strip()
    except Exception as e:
        logger.debug("MyMemory translate failed: %s", e)
    return None


def _translate_via_libre(text: str, source: str = "en", target: str = "ar") -> str | None:
    url = getattr(settings, "TRANSLATION_API_URL", "") or ""
    if not url:
        return None
    try:
        resp = requests.post(
            url,
            json={"q": text, "source": source, "target": target, "format": "text"},
            timeout=5,
        )
        if resp.ok:
            data = resp.json()
            # LibreTranslate returns {"translatedText": "..."}
            t = data.get("translatedText") or data.get("translation")
            if t:
                return t.strip()
    except Exception as e:
        logger.debug("LibreTranslate failed: %s", e)
    return None


def translate_text(text: str, source: str = "en", target: str = "ar") -> str:
    """Translate `text` from source→target, with caching and graceful fallback."""
    if not text or not text.strip():
        return ""
    if _is_arabic(text) and target == "ar":
        return text
    if not getattr(settings, "TRANSLATION_ENABLED", True):
        return text

    key = _cache_key(text, source, target)
    cached = cache.get(key)
    if cached:
        return cached

    # Try providers in order
    result = _translate_via_libre(text, source, target)
    if not result:
        result = _translate_via_mymemory(text, source, target)
    if not result:
        result = text  # fallback to original (never blank)

    try:
        cache.set(key, result, CACHE_TTL)
    except Exception:
        pass
    return result


def get_translated(value_ar: str | None, value_en: str | None, target: str = "ar") -> str:
    """
    Return the value for the requested locale.
    - If target==ar and value_ar is non-empty → value_ar
    - If target==ar and value_ar blank → auto-translate value_en → ar
    - If target==en → value_en (never translate)
    """
    if target == "ar":
        if value_ar and value_ar.strip():
            return value_ar
        if value_en and value_en.strip():
            return translate_text(value_en, source="en", target="ar")
        return value_ar or value_en or ""
    # English request
    return value_en or value_ar or ""
