"""
Tests for the bilingual translation engine (content/translation.py) and its
wiring in models, public serializers and the admin retranslate endpoint.

Covers the confirmed production bugs and the required behaviors:
- human Arabic is never overwritten (unless force_human is explicit)
- missing Arabic is translated and persisted exactly once
- successful translations are cached and the provider is not re-called
- failed provider results are NOT retained as long-lived successes
- cache TTL comes from TRANSLATION_CACHE_TTL
- changing English invalidates the translation cache
- retry works; force/force_human semantics are explicit
- English API mode stays correct
"""
from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings

from content.models import AboutContent, NewsArticle, Short
from content.translation import (
    clear_provider_down_marker,
    clear_failure_marker,
    clear_translation_cache,
    get_translated,
    is_machine_generated,
    persist_translation,
    retranslate_object,
    translate_text,
    _cache_key,
)

FAKE_ARABIC = 'نص عربي تجريبي'
FAKE_ARABIC_2 = 'نص عربي آخر'


def _fake_provider_result(text, source='en', target='ar'):
    return FAKE_ARABIC


class TranslationServiceTests(TestCase):
    """Core engine behaviors (translate_text / persist_translation)."""

    def setUp(self):
        cache.clear()

    def test_failure_is_not_cached_as_success(self):
        """A failed provider call returns English but caches no success entry."""
        with mock.patch(
            'content.translation._call_providers', return_value=None
        ) as provider:
            result = translate_text('Hello world')

        self.assertEqual(result, 'Hello world')
        provider.assert_called_once()
        self.assertIsNone(cache.get(_cache_key('Hello world', 'en', 'ar')))

    def test_failed_result_retries_after_failure_marker_expires(self):
        """The failure marker is short-lived; a later attempt calls the provider."""
        with mock.patch(
            'content.translation._call_providers', return_value=None
        ) as provider:
            first = translate_text('Hello world')
            second = translate_text('Hello world')  # failure marker active
            self.assertEqual(first, 'Hello world')
            self.assertEqual(second, 'Hello world')

        # Clear the short-lived failure marker -> engine may call provider again.
        clear_failure_marker('Hello world')
        clear_provider_down_marker()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            self.assertEqual(translate_text('Hello world'), FAKE_ARABIC)

    def test_success_is_cached_with_settings_ttl(self):
        """Successful results are cached once with the configured TTL."""
        with override_settings(TRANSLATION_CACHE_TTL=123):
            with mock.patch(
                'content.translation._call_providers', return_value=FAKE_ARABIC
            ) as provider:
                with mock.patch('content.translation.cache.set') as cache_set:
                    self.assertEqual(translate_text('Hello world'), FAKE_ARABIC)
        provider.assert_called_once()
        args, kwargs = cache_set.call_args
        self.assertEqual(args[0], _cache_key('Hello world', 'en', 'ar'))
        self.assertEqual(args[1], FAKE_ARABIC)
        self.assertEqual(args[2], 123)

    def test_cached_success_does_not_call_provider_again(self):
        """A cached successful translation short-circuits the provider call."""
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            translate_text('Hello world')

        with mock.patch(
            'content.translation._call_providers'
        ) as provider:
            self.assertEqual(translate_text('Hello world'), FAKE_ARABIC)
            provider.assert_not_called()

    def test_clear_translation_cache_forces_provider_recall(self):
        cache.set(_cache_key('Hello world', 'en', 'ar'), FAKE_ARABIC, 300)
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC_2
        ) as provider:
            clear_translation_cache('Hello world')
            self.assertEqual(translate_text('Hello world'), FAKE_ARABIC_2)
            provider.assert_called_once()

    def test_get_translated_english_mode_never_translates(self):
        """target=en returns English (or Arabic fallback) without any provider call."""
        with mock.patch('content.translation._call_providers') as provider:
            self.assertEqual(get_translated('عربي', 'English', 'en'), 'English')
            self.assertEqual(get_translated('عربي', '', 'en'), 'عربي')
            provider.assert_not_called()

    def test_get_translated_arabic_mode_falls_back_to_engine(self):
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            self.assertEqual(get_translated('', 'English', 'ar'), FAKE_ARABIC)


class PersistTranslationTests(TestCase):
    """translate-once-and-persist behaviors on real models."""

    def setUp(self):
        cache.clear()

    def _make_short(self, **kwargs):
        return Short.objects.create(
            video_title='A great video',
            slug='a-great-video',
            status='Published',
            **kwargs,
        )

    def test_missing_arabic_is_translated_and_persisted_once(self):
        short = self._make_short()
        self.assertEqual(short.video_title_ar, '')

        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            value = persist_translation(short, 'video_title', 'video_title_ar')

        self.assertEqual(value, FAKE_ARABIC)
        provider.assert_called_once()

        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, FAKE_ARABIC)
        self.assertTrue(is_machine_generated(short, 'video_title_ar'))

        # Second read: no provider call, value comes from the stored field.
        with mock.patch(
            'content.translation._call_providers'
        ) as provider_again:
            value_again = persist_translation(short, 'video_title', 'video_title_ar')
        self.assertEqual(value_again, FAKE_ARABIC)
        provider_again.assert_not_called()

    def test_human_arabic_is_never_overwritten(self):
        short = self._make_short(video_title_ar='كتبها الإنسان')
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            value = persist_translation(short, 'video_title', 'video_title_ar')
        self.assertEqual(value, 'كتبها الإنسان')
        provider.assert_not_called()
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, 'كتبها الإنسان')
        self.assertFalse(is_machine_generated(short, 'video_title_ar'))

    def test_machine_arabic_kept_without_force(self):
        short = self._make_short(video_title_ar=FAKE_ARABIC)
        # Field already machine-generated; non-force call keeps it.
        short.ar_is_machine = {'video_title_ar': True}
        with mock.patch('content.translation._call_providers') as provider:
            value = persist_translation(short, 'video_title', 'video_title_ar')
        self.assertEqual(value, FAKE_ARABIC)
        provider.assert_not_called()

    def test_force_regenerates_machine_arabic(self):
        short = self._make_short(video_title_ar=FAKE_ARABIC)
        short.ar_is_machine = {'video_title_ar': True}
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC_2
        ) as provider:
            retranslate_object(short, force=True)
        provider.assert_called()
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, FAKE_ARABIC_2)

    def test_force_does_not_touch_human_arabic(self):
        short = self._make_short(video_title_ar='كتبها الإنسان')
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            retranslate_object(short, force=True)
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, 'كتبها الإنسان')

    def test_force_human_overwrites_human_arabic_explicitly(self):
        short = self._make_short(video_title_ar='كتبها الإنسان')
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            retranslate_object(short, force_human=True)
        provider.assert_called()
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, FAKE_ARABIC)
        self.assertTrue(is_machine_generated(short, 'video_title_ar'))

    def test_failed_translation_not_persisted(self):
        short = self._make_short()
        with mock.patch(
            'content.translation._call_providers', return_value=None
        ) as provider:
            value = persist_translation(short, 'video_title', 'video_title_ar')
        self.assertEqual(value, 'A great video')  # English fallback, not stored
        provider.assert_called_once()
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, '')
        self.assertEqual(short.ar_is_machine, {})

    def test_changing_english_invalidates_cache(self):
        """Saving a record with changed English drops stale translation entries."""
        short = self._make_short()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            persist_translation(short, 'video_title', 'video_title_ar')
        self.assertIsNotNone(cache.get(_cache_key('A great video', 'en', 'ar')))

        short.video_title = 'A renamed video'
        short.save()
        self.assertIsNone(cache.get(_cache_key('A great video', 'en', 'ar')))

        # New English is translated fresh on the next read.
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC_2
        ) as provider:
            persist_translation(short, 'video_title', 'video_title_ar')
        provider.assert_called_once()
        short.refresh_from_db()
        self.assertEqual(short.video_title_ar, FAKE_ARABIC_2)
        self.assertTrue(is_machine_generated(short, 'video_title_ar'))


class AdminRetranslateEndpointTests(TestCase):
    """POST /api/admin/retranslate (JWT-protected)."""

    def setUp(self):
        cache.clear()
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(
            email='admin@example.com', password='secret-pass-123'
        )
        self.article = NewsArticle.objects.create(
            slug='news-1', article_title='A news title', status='Published'
        )

    def _login(self):
        """Return an authenticated APIClient.

        Uses force_authenticate directly: Django 5.0's debug-page rendering
        crashes under Python 3.14, so any failed JWT login attempt inside the
        test client would blow up before assertions run.
        """
        from rest_framework.test import APIClient

        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_retry_translates_blank_fields(self):
        client = self._login()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            clear_provider_down_marker()
            res = client.post(
                '/api/admin/retranslate',
                {'model': 'news', 'id': str(self.article.pk)},
                format='json',
            )
        self.assertEqual(res.status_code, 200)
        provider.assert_called()
        self.article.refresh_from_db()
        self.assertEqual(self.article.article_title_ar, FAKE_ARABIC)

    def test_retry_without_force_keeps_human_arabic(self):
        self.article.article_title_ar = 'كتبها المحرر'
        self.article.save()
        with mock.patch('content.translation._call_providers') as provider:
            client = self._login()
            res = client.post(
                '/api/admin/retranslate',
                {'model': 'news', 'id': str(self.article.pk), 'force': True},
                format='json',
            )
        provider.assert_not_called()
        self.article.refresh_from_db()
        self.assertEqual(self.article.article_title_ar, 'كتبها المحرر')

    def test_force_human_is_explicit_and_overwrites(self):
        self.article.article_title_ar = 'كتبها المحرر'
        self.article.save()
        client = self._login()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ):
            res = client.post(
                '/api/admin/retranslate',
                {'model': 'news', 'id': str(self.article.pk), 'force_human': True},
                format='json',
            )
        self.assertEqual(res.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.article_title_ar, FAKE_ARABIC)
        self.assertTrue(is_machine_generated(self.article, 'article_title_ar'))

    def test_unknown_model_returns_400(self):
        client = self._login()
        res = client.post(
            '/api/admin/retranslate', {'model': 'nope'}, format='json'
        )
        self.assertEqual(res.status_code, 400)

    def test_retry_clears_provider_down_marker(self):
        """The endpoint resets the circuit breaker so a retry really retries."""
        from content.translation import _provider_down_key

        cache.set(_provider_down_key(), True, 60)
        client = self._login()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            res = client.post(
                '/api/admin/retranslate',
                {'model': 'news', 'id': str(self.article.pk)},
                format='json',
            )
        self.assertEqual(res.status_code, 200)
        provider.assert_called()


class SingletonPageContentTests(TestCase):
    """PERSIST_BLANK_AR behavior on AboutContent via the serializer flag layer."""

    def setUp(self):
        cache.clear()
        AboutContent.objects.create(
            title='About Alia', description='We help families.'
        )

    def test_blank_arabic_persisted_on_first_serialization(self):
        from content.public_serializers import AboutContentSerializer

        obj = AboutContent.objects.first()
        with mock.patch(
            'content.translation._call_providers', return_value=FAKE_ARABIC
        ) as provider:
            data = AboutContentSerializer(obj).data
        self.assertEqual(data['titleAr'], FAKE_ARABIC)
        self.assertTrue(data['titleArIsMachine'])
        provider.assert_called()

        obj.refresh_from_db()
        self.assertEqual(obj.title_ar, FAKE_ARABIC)
        self.assertTrue(is_machine_generated(obj, 'title_ar'))
