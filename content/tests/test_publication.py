"""
Publication and canonical visibility tests for CMS page content.

Covers task requirements:
- Unpublished PagePresentation detail 404, list excludes unpublished.
- Unpublished Homepage/About/Contact/Footer returns 404 (safe unavailable).
- Hidden section API hides corresponding data.
- Default visibility maps merge correctly, obsolete keys stripped.
- Regression: translation + entity hiding still works (via existing suites).
"""
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

# copy patch for Django 5 + py3.14
import copy as _copy
from django.template.context import BaseContext, Context
def _patched_base_copy(self):
    dup = self.__class__.__new__(self.__class__)
    dup.__dict__ = _copy.copy(self.__dict__)
    dup.dicts = self.dicts[:]
    return dup
def _patched_context_copy(self):
    dup = _patched_base_copy(self)
    dup.render_context = _copy.copy(self.render_context)
    return dup
BaseContext.__copy__ = _patched_base_copy
Context.__copy__ = _patched_context_copy

from content.models import (
    AboutContent, ContactContent, FooterContent, HomepageContent, PagePresentation,
    ABOUT_SECTION_KEYS, CONTACT_SECTION_KEYS, FOOTER_SECTION_KEYS,
    HOME_SECTION_KEYS, SHORTS_SECTION_KEYS, NEWS_SECTION_KEYS,
    INITIATIVES_SECTION_KEYS, CONSULTATION_SECTION_KEYS, EMIRATES_SECTION_KEYS,
    _canonical_visibility,
)


@override_settings(DEBUG=False)
class SingletonPublicationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_homepage_published_public_200_unpublished_404(self):
        HomepageContent.objects.create(published=True, hero_title="Hello")
        resp = self.client.get('/api/homepage')
        self.assertEqual(resp.status_code, 200, resp.data)
        # unpublished hides completely
        obj = HomepageContent.objects.first()
        obj.published = False
        obj.save()
        resp2 = self.client.get('/api/homepage')
        self.assertEqual(resp2.status_code, 404)
        self.assertIn('not available', str(resp2.data).lower())

    def test_about_published_200_unpublished_404(self):
        AboutContent.objects.create(published=True, title="About")
        self.assertEqual(self.client.get('/api/about').status_code, 200)
        obj = AboutContent.objects.first()
        obj.published = False
        obj.save()
        self.assertEqual(self.client.get('/api/about').status_code, 404)

    def test_contact_published_200_unpublished_404(self):
        ContactContent.objects.create(published=True, title="Contact")
        self.assertEqual(self.client.get('/api/contact').status_code, 200)
        obj = ContactContent.objects.first()
        obj.published = False
        obj.save()
        self.assertEqual(self.client.get('/api/contact').status_code, 404)

    def test_footer_published_200_unpublished_404(self):
        FooterContent.objects.create(published=True, brand_text="Brand")
        self.assertEqual(self.client.get('/api/footer').status_code, 200)
        obj = FooterContent.objects.first()
        obj.published = False
        obj.save()
        self.assertEqual(self.client.get('/api/footer').status_code, 404)

    def test_singleton_unpublished_no_leak_fields(self):
        """Unpublished should not leak via any field diff - 404 has no content payload."""
        HomepageContent.objects.create(published=False, hero_title="Secret")
        resp = self.client.get('/api/homepage')
        self.assertEqual(resp.status_code, 404)
        # response should not contain the secret title
        self.assertNotIn('Secret', str(resp.data))

    def test_footer_missing_returns_404(self):
        # ensure empty DB gives unavailable not 500
        FooterContent.objects.all().delete()
        resp = self.client.get('/api/footer')
        self.assertEqual(resp.status_code, 404)


@override_settings(DEBUG=False)
class PagePresentationPublicationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_excludes_unpublished(self):
        PagePresentation.objects.create(key='shorts', title='A', published=True)
        PagePresentation.objects.create(key='news', title='B', published=False)
        resp = self.client.get('/api/presentations')
        self.assertEqual(resp.status_code, 200)
        keys = [p['key'] for p in resp.data]
        self.assertIn('shorts', keys)
        self.assertNotIn('news', keys)
        # ensure unpublished data not leaked in list
        self.assertNotIn('B', str(resp.data))

    def test_detail_published_200_unpublished_404(self):
        PagePresentation.objects.create(key='initiatives', title='Pub', published=True)
        PagePresentation.objects.create(key='consultation', title='Hidden', published=False)
        self.assertEqual(self.client.get('/api/presentations/initiatives').status_code, 200)
        resp = self.client.get('/api/presentations/consultation')
        self.assertEqual(resp.status_code, 404)
        self.assertNotIn('Hidden', str(resp.data))

    def test_detail_not_found_also_404(self):
        PagePresentation.objects.create(key='shorts', title='A', published=True)
        self.assertEqual(self.client.get('/api/presentations/unknown').status_code, 404)


@override_settings(DEBUG=False)
class HiddenSectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_pagepresentation_shorts_hidden_sections_omit_data(self):
        pp = PagePresentation.objects.create(
            key='shorts', title='T', published=True,
            shorts_topics=[{'title': 'Topic', 'videos': '1'}],
            shorts_contributors=['Alice'],
            shorts_faqs=[{'question': 'Q', 'answer': 'A'}],
            shorts_cta={'title': 'CTA'},
            shorts_section_visibility={'topics': False, 'contributors': False, 'faqs': False, 'cta': False}
        )
        resp = self.client.get('/api/presentations/shorts')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['topics'], [])
        self.assertEqual(resp.data['contributors'], [])
        self.assertEqual(resp.data['contributorsAr'], [])
        self.assertEqual(resp.data['faqs'], [])
        self.assertEqual(resp.data['shortsCta'], {})

    def test_pagepresentation_news_hidden_topics_omit(self):
        pp = PagePresentation.objects.create(
            key='news', title='N', published=True,
            news_topics=[{'title': 'T', 'videos': '1'}],
            news_contributors=['Bob'],
            news_faqs=[{'question': 'Q', 'answer': 'A'}],
            news_section_visibility={'topics': False, 'contributors': False, 'faqs': False, 'cta': True, 'categories': True, 'orgs': True}
        )
        resp = self.client.get('/api/presentations/news')
        self.assertEqual(resp.data['newsTopics'], [])
        self.assertEqual(resp.data['newsContributors'], [])
        self.assertEqual(resp.data['newsFaqs'], [])

    def test_homepage_hidden_sections_omit(self):
        HomepageContent.objects.create(
            published=True,
            hero_title='Hero', stats=[{'value': '1'}],
            shorts_title='Shorts',
            section_visibility={'hero': False, 'stats': False, 'shorts': False, 'news': True, 'initiatives': True, 'consultations': True, 'emirates': True, 'cta': False}
        )
        resp = self.client.get('/api/homepage')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['stats'], [])
        self.assertEqual(resp.data['heroTitle'], '')
        self.assertEqual(resp.data['shortsTitle'], '')
        self.assertEqual(resp.data['ctaTitle'], '')

    def test_about_hidden_sections_omit(self):
        AboutContent.objects.create(
            published=True, title='T',
            our_story='Story', our_story_text='text',
            objectives=['obj'],
            section_visibility={k: True for k in ABOUT_SECTION_KEYS} | {'ourStory': False, 'ourObjective': False}
        )
        resp = self.client.get('/api/about')
        self.assertEqual(resp.data['ourStory'], '')
        self.assertEqual(resp.data['objectives'], [])
        self.assertEqual(resp.data['ourMission'], resp.data['ourMission'])  # still present

    def test_contact_hidden_sections_omit(self):
        ContactContent.objects.create(
            published=True, title='T',
            send_message='Send', contact_info='Info', our_location='Loc', map_title='Map',
            section_visibility={'formLabels': False, 'contactInfo': False, 'locationMap': False}
        )
        resp = self.client.get('/api/contact')
        self.assertEqual(resp.data['sendMessage'], '')
        self.assertEqual(resp.data['contactInfo'], '')
        self.assertEqual(resp.data['ourLocation'], '')

    def test_footer_hidden_sections_omit(self):
        FooterContent.objects.create(
            published=True, brand_text='Brand', quick_links=[{'label': 'Home', 'href': '/'}],
            resource_links=[{'label': 'R', 'href': '#'}], phone='123',
            section_visibility={'brand': False, 'quickLinks': False, 'resources': False, 'contacts': False, 'bottomBar': False}
        )
        resp = self.client.get('/api/footer')
        self.assertEqual(resp.data['brandText'], '')
        self.assertEqual(resp.data['quickLinks'], [])
        self.assertEqual(resp.data['resourceLinks'], [])
        self.assertEqual(resp.data['phone'], '')
        self.assertEqual(resp.data['copyrightText'], '')


@override_settings(DEBUG=False)
class CanonicalVisibilityMapTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_missing_keys_default_to_visible(self):
        # Homepage missing keys
        HomepageContent.objects.create(published=True, section_visibility={})
        resp = self.client.get('/api/homepage')
        for k in HOME_SECTION_KEYS:
            self.assertIn(k, resp.data['sectionVisibility'])
            self.assertTrue(resp.data['sectionVisibility'][k], k)

        # About missing keys
        AboutContent.objects.create(published=True, section_visibility={})
        resp2 = self.client.get('/api/about')
        for k in ABOUT_SECTION_KEYS:
            self.assertTrue(resp2.data['sectionVisibility'][k])

        # Contact
        ContactContent.objects.create(published=True, section_visibility={})
        resp3 = self.client.get('/api/contact')
        for k in CONTACT_SECTION_KEYS:
            self.assertTrue(resp3.data['sectionVisibility'][k])

        # Footer
        FooterContent.objects.create(published=True, section_visibility={})
        resp4 = self.client.get('/api/footer')
        for k in FOOTER_SECTION_KEYS:
            self.assertTrue(resp4.data['sectionVisibility'][k])

    def test_obsolete_keys_stripped_on_save_and_api(self):
        # hero is obsolete for PagePresentation and About/Contact
        pp = PagePresentation.objects.create(key='shorts', title='T', published=True, shorts_section_visibility={'hero': False, 'topics': False, 'contributors': True, 'faqs': True, 'cta': True, 'obsolete': True})
        pp.refresh_from_db()
        self.assertNotIn('hero', pp.shorts_section_visibility)
        self.assertNotIn('obsolete', pp.shorts_section_visibility)
        resp = self.client.get('/api/presentations/shorts')
        self.assertNotIn('hero', resp.data['sectionVisibility'])
        self.assertNotIn('obsolete', resp.data['sectionVisibility'])
        self.assertEqual(set(resp.data['sectionVisibility'].keys()), set(SHORTS_SECTION_KEYS))

        AboutContent.objects.create(title='T', published=True, section_visibility={'hero': False, 'ourStory': True, 'extra': True})
        obj = AboutContent.objects.first()
        self.assertNotIn('hero', obj.section_visibility)
        self.assertNotIn('extra', obj.section_visibility)
        self.assertEqual(set(obj.section_visibility.keys()), set(ABOUT_SECTION_KEYS))

    def test_news_map_includes_categories_orgs(self):
        PagePresentation.objects.create(key='news', title='N', published=True, news_section_visibility={})
        resp = self.client.get('/api/presentations/news')
        for k in NEWS_SECTION_KEYS:
            self.assertIn(k, resp.data['newsSectionVisibility'])
        self.assertNotIn('hero', resp.data['newsSectionVisibility'])

    def test_shorts_map_does_not_include_categories_orgs(self):
        PagePresentation.objects.create(key='shorts', title='S', published=True, shorts_section_visibility={})
        resp = self.client.get('/api/presentations/shorts')
        self.assertNotIn('categories', resp.data['sectionVisibility'])
        self.assertNotIn('orgs', resp.data['sectionVisibility'])

    def test_canonical_visibility_helper(self):
        self.assertEqual(_canonical_visibility(None, ['a','b']), {'a': True, 'b': True})
        self.assertEqual(_canonical_visibility({'a': False}, ['a','b']), {'a': False, 'b': True})
        self.assertEqual(_canonical_visibility({'a': False, 'obsolete': True}, ['a','b']), {'a': False, 'b': True})

    def test_exact_supported_keys_documentation(self):
        """Assert the exact canonical key sets the task requires to be stable."""
        self.assertEqual(HOME_SECTION_KEYS, ['hero','stats','shorts','news','initiatives','consultations','emirates','cta'])
        self.assertEqual(ABOUT_SECTION_KEYS, ['ourStory','ourMission','ourVision','ourObjective','whatWeOffer','ourImpact','whyChoose','coreValues'])
        self.assertEqual(CONTACT_SECTION_KEYS, ['formLabels','contactInfo','locationMap'])
        self.assertEqual(FOOTER_SECTION_KEYS, ['brand','quickLinks','resources','contacts','bottomBar'])
        self.assertEqual(SHORTS_SECTION_KEYS, ['topics','contributors','faqs','cta'])
        self.assertEqual(NEWS_SECTION_KEYS, ['topics','contributors','faqs','cta','categories','orgs'])
        self.assertEqual(INITIATIVES_SECTION_KEYS, ['topics','contributors','faqs','cta'])
        self.assertEqual(CONSULTATION_SECTION_KEYS, ['topics','contributors','faqs','cta'])
        self.assertEqual(EMIRATES_SECTION_KEYS, ['topics','contributors','faqs','cta'])

