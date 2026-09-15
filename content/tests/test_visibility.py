"""
Visibility tests for entity content.

Covers:
- Draft and Pending items are invisible on every public endpoint (list, detail by slug,
  detail by title (consultation), search, related, homepage/featured, category filters, nested).
- Published items remain accessible.
- show_* flags omit corresponding block data from public detail responses.
- Admin API still returns Draft/Pending.
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# Patch Django 5.0 + Python 3.14 copy bug for template Context (see test_translation comment)
import copy as _copy
from django.template.context import BaseContext, Context

def _patched_base_copy(self):
    dup = self.__class__.__new__(self.__class__)
    dup.__dict__ = _copy.copy(self.__dict__)
    dup.dicts = self.dicts[:]
    return dup

BaseContext.__copy__ = _patched_base_copy

def _patched_context_copy(self):
    dup = _patched_base_copy(self)
    dup.render_context = _copy.copy(self.render_context)
    return dup

Context.__copy__ = _patched_context_copy

from content.models import Category, Consultation, Emirate, Initiative, NewsArticle, Short


def _extract_list_ids(response):
    """Handle paginated {data, meta} or plain list."""
    payload = response.data
    if isinstance(payload, dict) and 'data' in payload:
        return payload['data']
    if isinstance(payload, list):
        return payload
    return []


@override_settings(DEBUG=False)
class PublicVisibilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin_user = User.objects.create_user(email='admin_vis@example.com', password='pass12345')

    def _admin_client(self):
        c = APIClient()
        c.force_authenticate(user=self.admin_user)
        return c

    # ---------- helpers ----------
    def _create_all(self):
        """Create Draft/Pending/Published for each entity with unique search token."""
        # Shorts
        self.short_draft = Short.objects.create(video_title='VIS Short Draft', slug='vis-short-draft', status='Draft', category='Education')
        self.short_pending = Short.objects.create(video_title='VIS Short Pending', slug='vis-short-pending', status='Pending', category='Education')
        self.short_pub = Short.objects.create(video_title='VIS Short Published', slug='vis-short-published', status='Published', category='Education', speaker='John', views=42, key_topics=['t1'], resources=[{'title':'r'}], share_url='https://share')

        # News
        self.news_draft = NewsArticle.objects.create(article_title='VIS News Draft', slug='vis-news-draft', status='Draft', category='education', content='c')
        self.news_pending = NewsArticle.objects.create(article_title='VIS News Pending', slug='vis-news-pending', status='Pending', category='education', content='c')
        self.news_pub = NewsArticle.objects.create(article_title='VIS News Published', slug='vis-news-published', status='Published', category='education', content='hello content', author='Alice', organization='Org', city='Dubai', resources=[{'title':'r'}], share_url='https://share')

        # Consultation
        self.cons_draft = Consultation.objects.create(session_title='VIS Cons Draft', slug='vis-cons-draft', status='Draft', counselor='Dr A', gallery=['img'], learn_more={'info':'x'}, schedule={'a':1})
        self.cons_pending = Consultation.objects.create(session_title='VIS Cons Pending', slug='vis-cons-pending', status='Pending', counselor='Dr B', gallery=['img2'])
        self.cons_pub = Consultation.objects.create(session_title='VIS Cons Published', slug='vis-cons-published', status='Published', counselor='Dr Pub', counselor_photo='photo', counselor_title='Title', counselor_bio='bio', gallery=['imgpub'], learn_more={'k':'v'}, schedule={'s':1}, is_bookable=True)

        # Initiative
        self.init_draft = Initiative.objects.create(title='VIS Init Draft', slug='vis-init-draft', status='Draft', is_listed=True, description='desc', purpose='purp', objectives=['o'], benefits=['b'], contact=['c'])
        self.init_pending = Initiative.objects.create(title='VIS Init Pending', slug='vis-init-pending', status='Pending', is_listed=True)
        self.init_pub = Initiative.objects.create(title='VIS Init Published', slug='vis-init-published', status='Published', is_listed=True, is_featured=True, description='desc-pub', purpose='purp-pub', objectives=['obj'], benefits=['ben'], contact=['c1'], financial_support=True)

        # Another Published initiative not listed (should be hidden from list/search but detail still Published)
        self.init_pub_unlisted = Initiative.objects.create(title='VIS Init Unlisted', slug='vis-init-unlisted', status='Published', is_listed=False)

        # Emirate
        self.emir_draft = Emirate.objects.create(emirates_name='VIS Emirate Draft', slug='vis-emirate-draft', status='Draft')
        self.emir_pending = Emirate.objects.create(emirates_name='VIS Emirate Pending', slug='vis-emirate-pending', status='Pending')
        self.emir_pub = Emirate.objects.create(emirates_name='VIS Emirate Published', slug='vis-emirate-published', status='Published')

        # Category
        self.cat_draft = Category.objects.create(name='VIS Cat Draft', status='Draft')
        self.cat_pending = Category.objects.create(name='VIS Cat Pending', status='Pending')
        self.cat_pub = Category.objects.create(name='VIS Cat Published', status='Published')

    # ---------- list visibility ----------
    def test_list_endpoints_exclude_draft_pending(self):
        self._create_all()
        cases = [
            ('/api/shorts', 'vis-short'),
            ('/api/news', 'vis-news'),
            ('/api/consultations', 'vis-cons'),
            ('/api/emirates', 'vis-emirate'),
            ('/api/categories', 'VIS Cat'),
            ('/api/initiatives', 'vis-init'),
        ]
        for url, token in cases:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
            data = _extract_list_ids(resp)
            texts = str(data)
            # Published should be present
            self.assertIn('Published', texts, f"Published missing in {url}")
            # Draft/Pending must not appear
            self.assertNotIn('Draft', texts, f"Draft leaked in {url}")
            self.assertNotIn('Pending', texts, f"Pending leaked in {url}")

    def test_initiative_list_respects_is_listed(self):
        self._create_all()
        resp = self.client.get('/api/initiatives')
        data = _extract_list_ids(resp)
        slugs = [d.get('slug') for d in data]
        self.assertIn('vis-init-published', slugs)
        self.assertNotIn('vis-init-unlisted', slugs)
        self.assertNotIn('vis-init-draft', slugs)

    # ---------- detail by slug ----------
    def test_detail_by_slug_404_for_draft_pending(self):
        self._create_all()
        cases = [
            ('/api/shorts/vis-short-draft', 404),
            ('/api/shorts/vis-short-pending', 404),
            ('/api/shorts/vis-short-published', 200),
            ('/api/news/vis-news-draft', 404),
            ('/api/news/vis-news-pending', 404),
            ('/api/news/vis-news-published', 200),
            ('/api/consultations/vis-cons-draft', 404),
            ('/api/consultations/vis-cons-pending', 404),
            ('/api/consultations/vis-cons-published', 200),
            ('/api/initiatives/vis-init-draft', 404),
            ('/api/initiatives/vis-init-pending', 404),
            ('/api/initiatives/vis-init-published', 200),
            ('/api/emirates/vis-emirate-draft', 404),
            ('/api/emirates/vis-emirate-pending', 404),
            ('/api/emirates/vis-emirate-published', 200),
        ]
        for url, expected in cases:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, expected, f"{url} expected {expected} got {resp.status_code}")

    # ---------- detail by title (consultation) ----------
    def test_consultation_detail_by_title_respects_status(self):
        from content.views_public import ConsultationPublicDetailByNameView
        from rest_framework.test import APIRequestFactory
        self._create_all()
        factory = APIRequestFactory()
        view = ConsultationPublicDetailByNameView.as_view()
        # Draft via title should 404
        req = factory.get('/api/consultations/VIS Cons Draft')
        resp = view(req, slug='VIS Cons Draft')
        self.assertEqual(resp.status_code, 404)
        # Published via title should 200
        req = factory.get('/api/consultations/VIS Cons Published')
        resp = view(req, slug='VIS Cons Published')
        self.assertEqual(resp.status_code, 200)

    # ---------- search ----------
    def test_global_search_excludes_draft_pending(self):
        self._create_all()
        # Use vis token that appears in titles
        resp = self.client.get('/api/search', {'q': 'VIS Short'})
        self.assertEqual(resp.status_code, 200)
        # Should contain Published short but not Draft/Pending
        shorts = resp.data.get('shorts', [])
        titles = [s.get('videoTitle') or s.get('slug') for s in shorts]
        joined = str(titles)
        self.assertTrue(any('Published' in t for t in titles))
        self.assertFalse(any('Draft' in t for t in titles))
        self.assertFalse(any('Pending' in t for t in titles))

        # Initiatives search should not leak unlisted or draft
        resp2 = self.client.get('/api/search', {'q': 'VIS Init'})
        initiatives = resp2.data.get('initiatives', [])
        slugs = [i.get('slug') for i in initiatives]
        self.assertIn('vis-init-published', slugs)
        self.assertNotIn('vis-init-draft', slugs)
        self.assertNotIn('vis-init-unlisted', slugs)

        # Category search via global search not including categories, but ensure emirates etc filtered
        resp3 = self.client.get('/api/search', {'q': 'VIS Emirate'})
        emirates = resp3.data.get('emirates', [])
        names = [e.get('emiratesName') for e in emirates]
        self.assertTrue(any('Published' in n for n in names))
        self.assertFalse(any('Draft' in n for n in names))

    # ---------- related content ----------
    def test_related_content_excludes_unpublished(self):
        self._create_all()
        # Create another published short same category for related
        other_pub = Short.objects.create(video_title='VIS Short Other', slug='vis-short-other', status='Published', category='Education')
        # Detail for vis-short-published should include relatedVideos only Published
        resp = self.client.get('/api/shorts/vis-short-published')
        self.assertEqual(resp.status_code, 200)
        related = resp.data.get('relatedVideos', [])
        slugs = [r.get('slug') for r in related]
        self.assertIn('vis-short-other', slugs)
        self.assertNotIn('vis-short-draft', slugs)
        self.assertNotIn('vis-short-pending', slugs)

        # News related
        other_news = NewsArticle.objects.create(article_title='VIS News Other', slug='vis-news-other', status='Published', category='education')
        resp2 = self.client.get('/api/news/vis-news-published')
        self.assertEqual(resp2.status_code, 200)
        related2 = resp2.data.get('relatedStories', [])
        slugs2 = [r.get('slug') for r in related2]
        self.assertIn('vis-news-other', slugs2)
        self.assertNotIn('vis-news-draft', slugs2)

    # ---------- nested emirate initiatives ----------
    def test_emirate_nested_initiatives_exclude_unpublished_and_unlisted(self):
        self._create_all()
        # Link initiatives to emirate via emirates field
        self.init_pub.emirates = 'vis-emirate-published'
        self.init_pub.save()
        self.init_draft.emirates = 'vis-emirate-published'
        self.init_draft.save()
        self.init_pub_unlisted.emirates = 'vis-emirate-published'
        self.init_pub_unlisted.save()
        resp = self.client.get('/api/emirates/vis-emirate-published')
        self.assertEqual(resp.status_code, 200)
        initiatives = resp.data.get('initiatives', [])
        slugs = [i.get('slug') for i in initiatives]
        self.assertIn('vis-init-published', slugs)
        self.assertNotIn('vis-init-draft', slugs)
        self.assertNotIn('vis-init-unlisted', slugs)

    # ---------- category filter on initiatives ----------
    def test_category_filter_excludes_unpublished(self):
        self._create_all()
        self.init_pub.category = 'education'
        self.init_pub.save()
        self.init_draft.category = 'education'
        self.init_draft.save()
        resp = self.client.get('/api/initiatives', {'category': 'education'})
        slugs = [d.get('slug') for d in _extract_list_ids(resp)]
        self.assertIn('vis-init-published', slugs)
        self.assertNotIn('vis-init-draft', slugs)

    # ---------- homepage featured ----------
    def test_featured_initiative_excludes_draft(self):
        self._create_all()
        # Ensure only draft is featured scenario: make pending featured but published exists
        resp = self.client.get('/api/initiatives/featured')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get('slug'), 'vis-init-published')
        # If we delete published, featured should 404 not return draft
        Initiative.objects.filter(status='Published').delete()
        # Leave only draft featured
        self.init_draft.is_featured = True
        self.init_draft.save()
        resp2 = self.client.get('/api/initiatives/featured')
        self.assertEqual(resp2.status_code, 404)

    # ---------- show_* hidden block data ----------
    def test_short_show_flags_hide_data(self):
        s = Short.objects.create(video_title='VIS Hide Short', slug='vis-hide-short', status='Published', category='Education', speaker='Spk', speaker_ar='متحدث', views=99, key_topics=['k'], resources=[{'title':'r'}], share_url='https://s', show_key_topics=False, show_resources=False, show_share=False, show_speaker=False, show_views=False, show_related=False)
        # Create related published to test show_related hiding
        Short.objects.create(video_title='VIS Hide Related', slug='vis-hide-related', status='Published', category='Education')
        resp = self.client.get('/api/shorts/vis-hide-short')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['keyTopics'], [])
        self.assertEqual(resp.data['resources'], [])
        self.assertEqual(resp.data['shareUrl'], '')
        self.assertEqual(resp.data['speaker'], '')
        self.assertEqual(resp.data['speakerAr'], '')
        self.assertEqual(resp.data['views'], 0)
        self.assertEqual(resp.data['relatedVideos'], [])

    def test_news_show_flags_hide_data(self):
        n = NewsArticle.objects.create(article_title='VIS Hide News', slug='vis-hide-news', status='Published', category='education', content='c', author='Auth', author_ar='مؤلف', editorial_team='Team', organization='Org', moc='MOC', city='City', emirates='dubai', resources=[{'title':'r'}], share_url='https://s', show_article_info=False, show_related_resources=False, show_share=False, show_related_stories=False)
        NewsArticle.objects.create(article_title='VIS Hide News Rel', slug='vis-hide-news-rel', status='Published', category='education')
        resp = self.client.get('/api/news/vis-hide-news')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['author'], '')
        self.assertEqual(resp.data['authorAr'], '')
        self.assertEqual(resp.data['editorialTeam'], '')
        self.assertEqual(resp.data['organization'], '')
        self.assertEqual(resp.data['moc'], '')
        self.assertEqual(resp.data['city'], '')
        self.assertEqual(resp.data['emirate'], '')
        self.assertEqual(resp.data['resources'], [])
        self.assertEqual(resp.data['shareUrl'], '')
        self.assertEqual(resp.data['relatedStories'], [])

    def test_initiative_show_flags_hide_data(self):
        i = Initiative.objects.create(title='VIS Hide Init', slug='vis-hide-init', status='Published', is_listed=True, description='d', description_ar='d_ar', purpose='p', purpose_ar='p_ar', objectives=['o'], objectives_ar=['o_ar'], benefits=['b'], benefits_ar=['b_ar'], contact=['c1'], financial_support=True, show_about=False, show_support_offered=False, show_benefits=False, show_application_form=False)
        resp = self.client.get('/api/initiatives/vis-hide-init')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['description'], '')
        self.assertEqual(resp.data['descriptionAr'], '')
        self.assertEqual(resp.data['purpose'], '')
        self.assertEqual(resp.data['purposeAr'], '')
        self.assertEqual(resp.data['objectives'], [])
        self.assertEqual(resp.data['objectivesAr'], [])
        self.assertEqual(resp.data['benefits'], [])
        self.assertEqual(resp.data['benefitsAr'], [])
        self.assertEqual(resp.data['contact'], [])
        self.assertEqual(resp.data['supportOffered'], {'financial_support': False, 'housing_support': False, 'educational_support': False, 'marriage_training_program': False, 'pre_marital_preparation': False})

    def test_consultation_show_flags_hide_data(self):
        c = Consultation.objects.create(session_title='VIS Hide Cons', slug='vis-hide-cons', status='Published', counselor='Dr', counselor_ar='دكتور', counselor_photo='photo', counselor_title='T', counselor_title_ar='ت', counselor_bio='bio', counselor_bio_ar='سيرة', gallery=['g'], learn_more={'x':1}, schedule={'s':1}, show_doctor=False, show_learn_more=False, show_gallery=False, show_schedule=False, show_booking=False, is_bookable=True)
        resp = self.client.get('/api/consultations/vis-hide-cons')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['counselor'], '')
        self.assertEqual(resp.data['counselorAr'], '')
        self.assertEqual(resp.data['counselorPhoto'], '')
        self.assertEqual(resp.data['counselorTitle'], '')
        self.assertEqual(resp.data['counselorTitleAr'], '')
        self.assertEqual(resp.data['counselorBio'], '')
        self.assertEqual(resp.data['counselorBioAr'], '')
        self.assertEqual(resp.data['learnMore'], {})
        self.assertEqual(resp.data['gallery'], [])
        self.assertEqual(resp.data['coverImage'], '')
        self.assertEqual(resp.data['schedule'], {})
        self.assertEqual(resp.data['isBookable'], False)

    def test_emirate_show_status_hides(self):
        e = Emirate.objects.create(emirates_name='VIS Hide Emirate', slug='vis-hide-emirate', status='Published', show_status=False)
        resp = self.client.get('/api/emirates/vis-hide-emirate')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'], '')

    # ---------- admin still sees drafts ----------
    def test_admin_can_view_drafts(self):
        self._create_all()
        admin = self._admin_client()
        for url in ['/api/admin/shorts', '/api/admin/news', '/api/admin/consultations', '/api/admin/initiatives', '/api/admin/emirates', '/api/admin/categories']:
            resp = admin.get(url)
            self.assertEqual(resp.status_code, 200, url)
            data = _extract_list_ids(resp)
            texts = str(data)
            self.assertIn('Draft', texts, f"Draft missing for admin {url}")

    def test_admin_can_retrieve_draft_detail(self):
        self._create_all()
        admin = self._admin_client()
        # Example: shorts detail
        resp = admin.get(f'/api/admin/shorts/{self.short_draft.pk}')
        self.assertEqual(resp.status_code, 200)
        # News
        resp2 = admin.get(f'/api/admin/news/{self.news_draft.pk}')
        self.assertEqual(resp2.status_code, 200)
