import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .enums import (
    Emirates,
    Language,
    MaritalStage,
    MediaCategory,
    NewsCategory,
    ResourceType,
    SessionType,
    ShortCategory,
    Source,
    Status,
    SupportProgram,
)


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Short(TimeStampedModel):
    """Short / video entity (API spec 2.1)."""

    video_title = models.CharField('Video Title', max_length=300)
    video_title_ar = models.CharField('Video Title (Arabic)', max_length=300, blank=True)
    slug = models.SlugField('Slug', max_length=320, unique=True)
    description = models.TextField('Description', blank=True)

    category = models.CharField('Category', max_length=60, choices=ShortCategory.choices, blank=True)
    organization = models.CharField('Organization', max_length=200, blank=True)
    family = models.CharField('Family', max_length=200, blank=True)
    language = models.CharField('Language', max_length=10, choices=Language.choices, default=Language.ENGLISH)
    marital_stage = models.CharField(
        'Marital Stage', max_length=30, choices=MaritalStage.choices, default=MaritalStage.PREMARITAL
    )

    duration = models.CharField('Duration', max_length=20, blank=True)
    published_at = models.DateTimeField('Published Date', blank=True, null=True)
    cover_image = models.CharField('Cover Image', max_length=500, blank=True)
    video_url = models.CharField('Video URL', max_length=1000, blank=True)
    speaker = models.CharField('Speaker', max_length=200, blank=True)
    views = models.PositiveIntegerField('Views', default=0)

    key_topics = models.JSONField('Key Topics', default=list, blank=True)
    resources = models.JSONField('Resources', default=list, blank=True)
    share_url = models.CharField('Share URL', max_length=1000, blank=True)

    show_key_topics = models.BooleanField('Show Key Topics', default=True)
    show_resources = models.BooleanField('Show Resources', default=True)
    show_share = models.BooleanField('Show Share', default=True)
    show_speaker = models.BooleanField('Show Speaker', default=True)
    show_views = models.BooleanField('Show Views', default=True)
    show_related = models.BooleanField('Show Related', default=True)

    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.video_title


class NewsArticle(TimeStampedModel):
    """News article entity (API spec 2.2)."""

    slug = models.SlugField('Slug', max_length=320, unique=True)
    article_title = models.CharField('Article Title', max_length=300)
    article_title_ar = models.CharField('Article Title (Arabic)', max_length=300, blank=True)
    category = models.CharField('Category', max_length=40, choices=NewsCategory.choices, blank=True)
    source = models.CharField('Source', max_length=30, choices=Source.choices, default=Source.GOVERNMENT)
    language = models.CharField('Language', max_length=10, choices=Language.choices, default=Language.BOTH)

    content = models.TextField('Content', blank=True)
    cover_image = models.CharField('Cover Image', max_length=500, blank=True)

    author = models.CharField('Author', max_length=200, blank=True)
    editorial_team = models.CharField('Editorial Team', max_length=200, blank=True)
    organization = models.CharField('Organization', max_length=200, blank=True)
    moc = models.CharField('MOC / Issuing Body', max_length=200, blank=True)
    city = models.CharField('City', max_length=200, blank=True)
    emirates = models.CharField('Emirates', max_length=30, choices=Emirates.choices, blank=True)
    published_date = models.DateField('Published Date', null=True, blank=True)
    updated_date = models.DateField('Updated Date', null=True, blank=True)

    resources = models.JSONField('Resources', default=list, blank=True)
    share_url = models.CharField('Share URL', max_length=1000, blank=True)

    show_article_info = models.BooleanField('Show Article Info', default=True)
    show_related_resources = models.BooleanField('Show Related Resources', default=True)
    show_share = models.BooleanField('Show Share', default=True)
    show_related_stories = models.BooleanField('Show Related Stories', default=True)

    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.article_title


class Initiative(TimeStampedModel):
    """Initiative entity (API spec 2.3)."""

    slug = models.SlugField('Slug', max_length=320, unique=True)
    title = models.CharField('Title', max_length=300)
    title_ar = models.CharField('Title (Arabic)', max_length=300, blank=True)
    subtitle = models.CharField('Subtitle', max_length=400, blank=True)
    subtitle_ar = models.CharField('Subtitle (Arabic)', max_length=400, blank=True)

    category = models.CharField('Category', max_length=40, blank=True)
    emirates = models.CharField('Emirates', max_length=30, choices=Emirates.choices, blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    cover_image = models.CharField('Cover Image', max_length=500, blank=True)
    badge = models.CharField('Badge', max_length=100, blank=True)
    official_website_url = models.CharField('Official Website URL', max_length=1000, blank=True)
    share_url = models.CharField('Share URL', max_length=1000, blank=True)

    description = models.TextField('Description', blank=True)
    purpose = models.TextField('Purpose', blank=True)
    objectives = models.JSONField('Objectives', default=list, blank=True)

    basic_information = models.JSONField('Basic Information', default=list, blank=True)

    financial_support = models.BooleanField('Financial Support', default=False)
    housing_support = models.BooleanField('Housing Support', default=False)
    educational_support = models.BooleanField('Educational Support', default=False)
    marriage_training_program = models.BooleanField('Marriage Training Program', default=False)
    pre_marital_preparation = models.BooleanField('Pre-Marital Preparation', default=False)

    benefits = models.JSONField('Benefits', default=list, blank=True)
    contact = models.JSONField('Contact', default=list, blank=True)

    is_featured = models.BooleanField('Featured on Home Page', default=False, help_text='If checked, this initiative is shown on the user panel (single featured).')
    is_listed = models.BooleanField('Show on Initiatives Listing', default=True, help_text='Show this initiative in the public /initiatives list. Featured initiatives are always listed.')

    show_about = models.BooleanField('Show About', default=True)
    show_support_offered = models.BooleanField('Show Support Offered', default=True)
    show_benefits = models.BooleanField('Show Benefits', default=True)
    show_application_form = models.BooleanField('Show Application Form', default=True)

    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = 'Initiative'
        verbose_name_plural = 'Initiatives'
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_featured:
            Initiative.objects.filter(is_featured=True).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)

    @property
    def support_offered(self):
        return {
            'financial_support': self.financial_support,
            'housing_support': self.housing_support,
            'educational_support': self.educational_support,
            'marriage_training_program': self.marriage_training_program,
            'pre_marital_preparation': self.pre_marital_preparation,
        }

    @support_offered.setter
    def support_offered(self, value):
        mapping = {
            'financial_support': 'financial_support',
            'housing_support': 'housing_support',
            'educational_support': 'educational_support',
            'marriage_training_program': 'marriage_training_program',
            'pre_marital_preparation': 'pre_marital_preparation',
        }
        if isinstance(value, dict):
            for key, model_field in mapping.items():
                if key in value:
                    setattr(self, model_field, bool(value[key]))


class Consultation(TimeStampedModel):
    """Consultation / session entity (API spec 2.4)."""

    slug = models.SlugField('Slug', max_length=320, unique=True)
    session_title = models.CharField('Session Title', max_length=300)
    session_title_ar = models.CharField('Session Title (Arabic)', max_length=300, blank=True)
    category = models.CharField('Category', max_length=40, blank=True)
    session_type = models.CharField('Session Type', max_length=30, choices=SessionType.choices, blank=True)
    emirates = models.CharField('Emirates', max_length=30, choices=Emirates.choices, blank=True)
    marital_stage = models.CharField(
        'Marital Stage', max_length=30, choices=MaritalStage.choices, default=MaritalStage.MARITAL
    )
    language = models.CharField('Language', max_length=10, choices=Language.choices, default=Language.BOTH)

    published_date = models.DateField('Published Date', null=True, blank=True)
    date = models.DateField('Session Date', null=True, blank=True)
    start_time = models.CharField('Start Time', max_length=10, blank=True)
    end_time = models.CharField('End Time', max_length=10, blank=True)
    duration = models.CharField('Duration', max_length=50, blank=True)
    time_zone = models.CharField('Time Zone', max_length=50, default='GST (UTC+4)')
    meeting_format = models.CharField(
        'Format', max_length=20, choices=[('online', 'Online'), ('onsite', 'Onsite')], default='online'
    )
    session_link = models.CharField('Session Link', max_length=1000, blank=True)

    max_participants = models.IntegerField('Max Participants', null=True, blank=True)
    is_free = models.BooleanField('Is Free', default=True)
    fee = models.DecimalField('Fee (AED)', max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    processing_fee = models.DecimalField(
        'Processing Fee (AED)', max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    discount = models.DecimalField(
        'Discount (AED)', max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    counselor = models.CharField('Counselor', max_length=200, blank=True)
    counselor_photo = models.CharField('Counselor Photo', max_length=500, blank=True)
    counselor_title = models.CharField('Counselor Title', max_length=200, blank=True)
    counselor_bio = models.TextField('Counselor Bio', blank=True)
    learn_more = models.JSONField('Learn More', default=dict, blank=True)

    gallery = models.JSONField('Gallery', default=list, blank=True)
    description = models.TextField('Description', blank=True)
    objectives = models.JSONField('Objectives', default=list, blank=True)
    what_you_will_learn = models.JSONField('What You Will Learn', default=list, blank=True)
    who_should_attend = models.JSONField('Who Should Attend', default=list, blank=True)

    schedule = models.JSONField('Schedule', default=dict, blank=True)
    booking_notice = models.CharField('Booking Notice', max_length=500, blank=True)

    show_doctor = models.BooleanField('Show Doctor', default=True)
    show_learn_more = models.BooleanField('Show Learn More', default=True)
    show_gallery = models.BooleanField('Show Gallery', default=True)
    show_schedule = models.BooleanField('Show Schedule', default=True)
    show_booking = models.BooleanField('Show Booking', default=True)
    is_bookable = models.BooleanField('Is Bookable', default=True)

    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.session_title

    @property
    def seats_left(self):
        from engagement.models import Booking
        confirmed = Booking.objects.filter(consultation_id=self.pk, status='confirmed').count()
        if self.max_participants is None:
            return None
        return max(self.max_participants - confirmed, 0)


class Emirate(TimeStampedModel):
    """Emirate entity (API spec 2.5)."""

    emirates_name = models.CharField('Emirates Name', max_length=100)
    emirates_name_ar = models.CharField('Emirates Name (Arabic)', max_length=100, blank=True)
    slug = models.SlugField('Slug', max_length=120, unique=True)
    title = models.CharField('Title', max_length=200, blank=True)
    description = models.TextField('Description', blank=True)
    date_time = models.DateTimeField('Date Time', blank=True, null=True)
    contact_phone = models.CharField('Contact Phone', max_length=50, blank=True)
    service_centers = models.PositiveIntegerField('Service Centers', default=0)
    center_count = models.CharField('Center Count', max_length=100, blank=True)
    image = models.CharField('Image', max_length=500, blank=True)
    website_url = models.CharField('Website URL', max_length=1000, blank=True)

    show_status = models.BooleanField('Show Status', default=True)
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.PUBLISHED)

    class Meta:
        verbose_name = 'Emirate'
        verbose_name_plural = 'Emirates'
        ordering = ['emirates_name']

    def __str__(self):
        return self.emirates_name


class Category(TimeStampedModel):
    """Category entity (API spec 2.6)."""

    name = models.CharField('Category', max_length=100, unique=True)
    description = models.TextField('Description', blank=True)
    date = models.DateField('Date', null=True, blank=True)
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.PUBLISHED)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class PagePresentation(TimeStampedModel):
    """Editable hero / page presentation for the user panel (News, Shorts, Consultation).

    Holds the localized title, description, badge and hero image that appear at the top
    of a section page. Content is managed from the admin dashboard and served to the user
    panel via the public API - nothing here is hard-coded in the frontend.
    """

    SECTION_CHOICES = [
        ('news', 'News'),
        ('shorts', 'Shorts'),
        ('consultation', 'Consultation'),
        ('home', 'Home'),
        ('initiatives', 'Initiatives'),
        ('emirates', 'Emirates'),
    ]

    key = models.CharField('Section Key', max_length=40, unique=True, choices=SECTION_CHOICES)
    title = models.CharField('Title (English)', max_length=300, blank=True)
    title_ar = models.CharField('Title (Arabic)', max_length=300, blank=True)
    description = models.TextField('Description (English)', blank=True)
    description_ar = models.TextField('Description (Arabic)', blank=True)
    badge = models.CharField('Badge', max_length=120, blank=True)
    hero_image = models.CharField('Hero Image', max_length=500, blank=True)
    published = models.BooleanField('Published', default=True)

    # Shorts page extras (topics / contributors / FAQs). Kept on the shared
    # presentation model so they can be managed from the admin dashboard.
    shorts_topics = models.JSONField(
        'Shorts Topics',
        default=list,
        blank=True,
        help_text='List of { "title", "videos", "icon" } items shown on the Shorts page.',
    )
    shorts_contributors = models.JSONField(
        'Shorts Contributors',
        default=list,
        blank=True,
        help_text='List of contributor names shown on the Shorts page.',
    )
    shorts_faqs = models.JSONField(
        'Shorts FAQs',
        default=list,
        blank=True,
        help_text='List of { "question", "questionAr", "answer", "answerAr" } items shown on the Shorts page.',
    )
    shorts_section_visibility = models.JSONField(
        'Shorts Section Visibility',
        default=dict,
        blank=True,
        help_text=(
            'Controls which sections render on the Shorts user-panel page. '
            'Keys: hero, topics, contributors, faqs. Missing keys default to true.'
        ),
    )

    class Meta:
        verbose_name = 'Page Presentation'
        verbose_name_plural = 'Page Presentations'
        ordering = ['key']

    def __str__(self):
        return dict(self.SECTION_CHOICES).get(self.key, self.key)


HOME_SECTION_KEYS = [
    'hero',
    'stats',
    'shorts',
    'news',
    'initiatives',
    'consultations',
    'emirates',
    'cta',
]


def _default_section_visibility():
    return {key: True for key in HOME_SECTION_KEYS}


class HomepageContent(TimeStampedModel):
    """Singleton model storing all editable homepage content.

    Only one record should ever exist. Admin saves via upsert (POST).
    The public API serves this single record to the user homepage.
    """

    # --- Hero Section ---
    hero_eyebrow = models.CharField('Hero Eyebrow', max_length=300, blank=True)
    hero_eyebrow_ar = models.CharField('Hero Eyebrow (Arabic)', max_length=300, blank=True)
    hero_title = models.CharField('Hero Title', max_length=500, blank=True)
    hero_title_ar = models.CharField('Hero Title (Arabic)', max_length=500, blank=True)
    hero_subtitle = models.TextField('Hero Subtitle', blank=True)
    hero_subtitle_ar = models.TextField('Hero Subtitle (Arabic)', blank=True)
    hero_search_placeholder = models.CharField('Hero Search Placeholder', max_length=300, blank=True)
    hero_search_placeholder_ar = models.CharField('Hero Search Placeholder (Arabic)', max_length=300, blank=True)
    hero_search_button = models.CharField('Hero Search Button', max_length=100, blank=True)
    hero_search_button_ar = models.CharField('Hero Search Button (Arabic)', max_length=100, blank=True)
    hero_primary_cta_label = models.CharField('Hero Primary CTA Label', max_length=150, blank=True)
    hero_primary_cta_label_ar = models.CharField('Hero Primary CTA Label (Arabic)', max_length=150, blank=True)
    hero_primary_cta_link = models.CharField('Hero Primary CTA Link', max_length=500, blank=True, default='/initiatives')
    hero_secondary_cta_label = models.CharField('Hero Secondary CTA Label', max_length=150, blank=True)
    hero_secondary_cta_label_ar = models.CharField('Hero Secondary CTA Label (Arabic)', max_length=150, blank=True)
    hero_secondary_cta_link = models.CharField('Hero Secondary CTA Link', max_length=500, blank=True, default='/news')
    hero_image = models.CharField('Hero Image', max_length=500, blank=True)
    hero_image_alt = models.CharField('Hero Image Alt', max_length=300, blank=True)
    hero_floating_cards = models.JSONField('Hero Floating Cards', default=list, blank=True,
        help_text='Array of 4 objects: {label, labelAr, sublabel, sublabelAr}')

    # --- Stats Section (FeatureGrid) ---
    stats = models.JSONField('Stats', default=list, blank=True,
        help_text='Array of 4 objects: {value, title, titleAr, subtitle, subtitleAr}')

    # --- Shorts Section Header ---
    shorts_title = models.CharField('Shorts Title', max_length=300, blank=True)
    shorts_title_ar = models.CharField('Shorts Title (Arabic)', max_length=300, blank=True)
    shorts_subtitle = models.TextField('Shorts Subtitle', blank=True)
    shorts_subtitle_ar = models.TextField('Shorts Subtitle (Arabic)', blank=True)
    shorts_cta_label = models.CharField('Shorts CTA Label', max_length=150, blank=True)
    shorts_cta_label_ar = models.CharField('Shorts CTA Label (Arabic)', max_length=150, blank=True)
    shorts_empty_text = models.CharField('Shorts Empty Text', max_length=300, blank=True)
    shorts_empty_text_ar = models.CharField('Shorts Empty Text (Arabic)', max_length=300, blank=True)

    # --- News Section Header ---
    news_title = models.CharField('News Title', max_length=300, blank=True)
    news_title_ar = models.CharField('News Title (Arabic)', max_length=300, blank=True)
    news_subtitle = models.TextField('News Subtitle', blank=True)
    news_subtitle_ar = models.TextField('News Subtitle (Arabic)', blank=True)
    news_cta_label = models.CharField('News CTA Label', max_length=150, blank=True)
    news_cta_label_ar = models.CharField('News CTA Label (Arabic)', max_length=150, blank=True)

    # --- Initiatives Section Header ---
    initiatives_title = models.CharField('Initiatives Title', max_length=300, blank=True)
    initiatives_title_ar = models.CharField('Initiatives Title (Arabic)', max_length=300, blank=True)
    initiatives_subtitle = models.TextField('Initiatives Subtitle', blank=True)
    initiatives_subtitle_ar = models.TextField('Initiatives Subtitle (Arabic)', blank=True)
    initiatives_cta_label = models.CharField('Initiatives CTA Label', max_length=150, blank=True)
    initiatives_cta_label_ar = models.CharField('Initiatives CTA Label (Arabic)', max_length=150, blank=True)

    # --- Consultations Section Header ---
    consultations_title = models.CharField('Consultations Title', max_length=300, blank=True)
    consultations_title_ar = models.CharField('Consultations Title (Arabic)', max_length=300, blank=True)
    consultations_subtitle = models.TextField('Consultations Subtitle', blank=True)
    consultations_subtitle_ar = models.TextField('Consultations Subtitle (Arabic)', blank=True)
    consultations_cta_label = models.CharField('Consultations CTA Label', max_length=150, blank=True)
    consultations_cta_label_ar = models.CharField('Consultations CTA Label (Arabic)', max_length=150, blank=True)
    consultations_free_tab = models.CharField('Free Session Tab', max_length=100, blank=True)
    consultations_free_tab_ar = models.CharField('Free Session Tab (Arabic)', max_length=100, blank=True)
    consultations_paid_tab = models.CharField('Paid Session Tab', max_length=100, blank=True)
    consultations_paid_tab_ar = models.CharField('Paid Session Tab (Arabic)', max_length=100, blank=True)

    # --- Emirates Section Header ---
    emirates_title = models.CharField('Emirates Title', max_length=300, blank=True)
    emirates_title_ar = models.CharField('Emirates Title (Arabic)', max_length=300, blank=True)
    emirates_subtitle = models.TextField('Emirates Subtitle', blank=True)
    emirates_subtitle_ar = models.TextField('Emirates Subtitle (Arabic)', blank=True)
    emirates_capital_label = models.CharField('Capital Region Label', max_length=100, blank=True)
    emirates_capital_label_ar = models.CharField('Capital Region Label (Arabic)', max_length=100, blank=True)
    emirates_headquarters_label = models.CharField('Main Headquarters Label', max_length=100, blank=True)
    emirates_headquarters_label_ar = models.CharField('Main Headquarters Label (Arabic)', max_length=100, blank=True)
    emirates_cta_label = models.CharField('Emirates CTA Label', max_length=150, blank=True)
    emirates_cta_label_ar = models.CharField('Emirates CTA Label (Arabic)', max_length=150, blank=True)

    # --- CTA Section ---
    cta_title = models.CharField('CTA Title', max_length=300, blank=True)
    cta_title_ar = models.CharField('CTA Title (Arabic)', max_length=300, blank=True)
    cta_subtitle = models.TextField('CTA Subtitle', blank=True)
    cta_subtitle_ar = models.TextField('CTA Subtitle (Arabic)', blank=True)
    cta_primary_label = models.CharField('CTA Primary Label', max_length=150, blank=True)
    cta_primary_label_ar = models.CharField('CTA Primary Label (Arabic)', max_length=150, blank=True)
    cta_primary_link = models.CharField('CTA Primary Link', max_length=500, blank=True, default='/initiatives')
    cta_secondary_label = models.CharField('CTA Secondary Label', max_length=150, blank=True)
    cta_secondary_label_ar = models.CharField('CTA Secondary Label (Arabic)', max_length=150, blank=True)
    cta_secondary_link = models.CharField('CTA Secondary Link', max_length=500, blank=True, default='/consultation')

    # --- Visibility ---
    published = models.BooleanField('Published', default=True)

    section_visibility = models.JSONField(
        'Section Visibility',
        default=_default_section_visibility,
        blank=True,
        help_text='Toggle which homepage sections render on the user panel. Keys: hero, stats, shorts, news, initiatives, consultations, emirates, cta. Missing keys default to true.',
    )

    class Meta:
        verbose_name = 'Homepage Content'
        verbose_name_plural = 'Homepage Content'

    def __str__(self):
        return 'Homepage Content'

    def save(self, *args, **kwargs):
        # Enforce singleton: only one record allowed
        if not self.pk and HomepageContent.objects.exists():
            existing = HomepageContent.objects.first()
            self.pk = existing.pk
        # Merge defaults so newly-added section keys always render.
        defaults = _default_section_visibility()
        current = dict(self.section_visibility or {})
        for key, value in defaults.items():
            current.setdefault(key, value)
        self.section_visibility = current
        super().save(*args, **kwargs)


class AboutContent(TimeStampedModel):
    """Singleton model for About Us page content."""

    # --- Hero Section ---
    title = models.CharField('Title', max_length=500, blank=True)
    title_ar = models.CharField('Title (Arabic)', max_length=500, blank=True)
    description = models.TextField('Description', blank=True)
    description_ar = models.TextField('Description (Arabic)', blank=True)
    browse_session = models.CharField('Browse Session Label', max_length=200, blank=True)
    browse_session_ar = models.CharField('Browse Session Label (Arabic)', max_length=200, blank=True)
    contact_support = models.CharField('Contact Support Label', max_length=200, blank=True)
    contact_support_ar = models.CharField('Contact Support Label (Arabic)', max_length=200, blank=True)
    hero_image = models.CharField('Hero Image URL', max_length=500, blank=True,
        help_text='Recommended 1280x600 px')
    hero_image_alt = models.CharField('Hero Image Alt Text', max_length=300, blank=True)

    # --- Our Story ---
    our_story = models.CharField('Our Story Heading', max_length=300, blank=True)
    our_story_ar = models.CharField('Our Story Heading (Arabic)', max_length=300, blank=True)
    our_story_text = models.TextField('Our Story Text', blank=True)
    our_story_text_ar = models.TextField('Our Story Text (Arabic)', blank=True)

    # --- Our Mission ---
    our_mission = models.CharField('Our Mission Heading', max_length=300, blank=True)
    our_mission_ar = models.CharField('Our Mission Heading (Arabic)', max_length=300, blank=True)
    our_mission_text = models.TextField('Our Mission Text', blank=True)
    our_mission_text_ar = models.TextField('Our Mission Text (Arabic)', blank=True)

    # --- Our Vision ---
    our_vision = models.CharField('Our Vision Heading', max_length=300, blank=True)
    our_vision_ar = models.CharField('Our Vision Heading (Arabic)', max_length=300, blank=True)
    our_vision_text = models.TextField('Our Vision Text', blank=True)
    our_vision_text_ar = models.TextField('Our Vision Text (Arabic)', blank=True)

    # --- Our Objective ---
    our_objective = models.CharField('Our Objective Heading', max_length=300, blank=True)
    our_objective_ar = models.CharField('Our Objective Heading (Arabic)', max_length=300, blank=True)
    our_objective_text = models.TextField('Our Objective Text', blank=True)
    our_objective_text_ar = models.TextField('Our Objective Text (Arabic)', blank=True)
    objectives = models.JSONField('Objectives', default=list, blank=True,
        help_text='Array of 6 objective labels')

    # --- What We Offer ---
    what_we_offer = models.CharField('What We Offer Heading', max_length=300, blank=True)
    what_we_offer_ar = models.CharField('What We Offer Heading (Arabic)', max_length=300, blank=True)
    what_we_offer_text = models.TextField('What We Offer Text', blank=True)
    what_we_offer_text_ar = models.TextField('What We Offer Text (Arabic)', blank=True)
    offerings = models.JSONField('Offerings', default=list, blank=True,
        help_text='Array of 6 objects: {title, titleAr, desc, descAr}')

    # --- Our Impact ---
    our_impact = models.CharField('Our Impact Heading', max_length=300, blank=True)
    our_impact_ar = models.CharField('Our Impact Heading (Arabic)', max_length=300, blank=True)
    our_impact_text = models.TextField('Our Impact Text', blank=True)
    our_impact_text_ar = models.TextField('Our Impact Text (Arabic)', blank=True)
    impact = models.JSONField('Impact', default=list, blank=True,
        help_text='Array of 4 objects: {label, labelAr, value, valueAr}')

    # --- Why Choose Alia ---
    why_choose = models.CharField('Why Choose Heading', max_length=300, blank=True)
    why_choose_ar = models.CharField('Why Choose Heading (Arabic)', max_length=300, blank=True)
    why_choose_text = models.TextField('Why Choose Text', blank=True)
    why_choose_text_ar = models.TextField('Why Choose Text (Arabic)', blank=True)
    why_values = models.JSONField('Why Values', default=list, blank=True,
        help_text='Array of 4 value labels')

    # --- Core Values ---
    core_values = models.CharField('Core Values Heading', max_length=300, blank=True)
    core_values_ar = models.CharField('Core Values Heading (Arabic)', max_length=300, blank=True)
    core_values_text = models.TextField('Core Values Text', blank=True)
    core_values_text_ar = models.TextField('Core Values Text (Arabic)', blank=True)
    core_value_list = models.JSONField('Core Value List', default=list, blank=True,
        help_text='Array of 5 core value labels')

    published = models.BooleanField('Published', default=True)

    class Meta:
        verbose_name = 'About Content'
        verbose_name_plural = 'About Content'

    def __str__(self):
        return 'About Content'

    def save(self, *args, **kwargs):
        if not self.pk and AboutContent.objects.exists():
            existing = AboutContent.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class ContactContent(TimeStampedModel):
    """Singleton model for Contact Us page content."""

    # --- Hero Section ---
    title = models.CharField('Title', max_length=500, blank=True)
    title_ar = models.CharField('Title (Arabic)', max_length=500, blank=True)
    description = models.TextField('Description', blank=True)
    description_ar = models.TextField('Description (Arabic)', blank=True)
    browse_session = models.CharField('Browse Session Label', max_length=200, blank=True)
    browse_session_ar = models.CharField('Browse Session Label (Arabic)', max_length=200, blank=True)
    contact_support = models.CharField('Contact Support Label', max_length=200, blank=True)
    contact_support_ar = models.CharField('Contact Support Label (Arabic)', max_length=200, blank=True)

    # --- Send Message Form ---
    send_message = models.CharField('Send Message Heading', max_length=300, blank=True)
    send_message_ar = models.CharField('Send Message Heading (Arabic)', max_length=300, blank=True)
    send_message_sub = models.CharField('Send Message Subheading', max_length=300, blank=True)
    send_message_sub_ar = models.CharField('Send Message Subheading (Arabic)', max_length=300, blank=True)
    full_name = models.CharField('Full Name Label', max_length=200, blank=True)
    full_name_ar = models.CharField('Full Name Label (Arabic)', max_length=200, blank=True)
    full_name_placeholder = models.CharField('Full Name Placeholder', max_length=200, blank=True)
    full_name_placeholder_ar = models.CharField('Full Name Placeholder (Arabic)', max_length=200, blank=True)
    email_label = models.CharField('Email Label', max_length=200, blank=True)
    email_label_ar = models.CharField('Email Label (Arabic)', max_length=200, blank=True)
    email_placeholder = models.CharField('Email Placeholder', max_length=200, blank=True)
    email_placeholder_ar = models.CharField('Email Placeholder (Arabic)', max_length=200, blank=True)
    user_type = models.CharField('User Type Label', max_length=200, blank=True)
    user_type_ar = models.CharField('User Type Label (Arabic)', max_length=200, blank=True)
    select_user_type = models.CharField('Select User Type', max_length=200, blank=True)
    select_user_type_ar = models.CharField('Select User Type (Arabic)', max_length=200, blank=True)
    individual = models.CharField('Individual Option', max_length=100, blank=True)
    individual_ar = models.CharField('Individual Option (Arabic)', max_length=100, blank=True)
    couple = models.CharField('Couple Option', max_length=100, blank=True)
    couple_ar = models.CharField('Couple Option (Arabic)', max_length=100, blank=True)
    organization = models.CharField('Organization Option', max_length=100, blank=True)
    organization_ar = models.CharField('Organization Option (Arabic)', max_length=100, blank=True)
    subject_label = models.CharField('Subject Label', max_length=200, blank=True)
    subject_label_ar = models.CharField('Subject Label (Arabic)', max_length=200, blank=True)
    subject_placeholder = models.CharField('Subject Placeholder', max_length=200, blank=True)
    subject_placeholder_ar = models.CharField('Subject Placeholder (Arabic)', max_length=200, blank=True)
    phone_label = models.CharField('Phone Label', max_length=200, blank=True)
    phone_label_ar = models.CharField('Phone Label (Arabic)', max_length=200, blank=True)
    phone_placeholder = models.CharField('Phone Placeholder', max_length=200, blank=True)
    phone_placeholder_ar = models.CharField('Phone Placeholder (Arabic)', max_length=200, blank=True)
    message_label = models.CharField('Message Label', max_length=200, blank=True)
    message_label_ar = models.CharField('Message Label (Arabic)', max_length=200, blank=True)
    message_placeholder = models.CharField('Message Placeholder', max_length=200, blank=True)
    message_placeholder_ar = models.CharField('Message Placeholder (Arabic)', max_length=200, blank=True)
    send_button = models.CharField('Send Button', max_length=100, blank=True)
    send_button_ar = models.CharField('Send Button (Arabic)', max_length=100, blank=True)
    success_message = models.CharField('Success Message', max_length=500, blank=True)
    success_message_ar = models.CharField('Success Message (Arabic)', max_length=500, blank=True)
    sending = models.CharField('Sending Label', max_length=100, blank=True)
    sending_ar = models.CharField('Sending Label (Arabic)', max_length=100, blank=True)

    # --- Contact Info Sidebar ---
    contact_info = models.CharField('Contact Info Heading', max_length=200, blank=True)
    contact_info_ar = models.CharField('Contact Info Heading (Arabic)', max_length=200, blank=True)
    office_address = models.CharField('Office Address Heading', max_length=200, blank=True)
    office_address_ar = models.CharField('Office Address Heading (Arabic)', max_length=200, blank=True)
    working_hours = models.CharField('Working Hours Heading', max_length=200, blank=True)
    working_hours_ar = models.CharField('Working Hours Heading (Arabic)', max_length=200, blank=True)
    general_inquiries = models.CharField('General Inquiries Heading', max_length=200, blank=True)
    general_inquiries_ar = models.CharField('General Inquiries Heading (Arabic)', max_length=200, blank=True)
    support_heading = models.CharField('Support Heading', max_length=200, blank=True)
    support_heading_ar = models.CharField('Support Heading (Arabic)', max_length=200, blank=True)
    address_lines = models.JSONField('Address Lines', default=list, blank=True,
        help_text='Array of 3 strings: address, email, phone')
    address_lines_ar = models.JSONField('Address Lines (Arabic)', default=list, blank=True)
    hours_lines = models.JSONField('Hours Lines', default=list, blank=True,
        help_text='Array of 3 strings: Mon-Fri, Sat, Sun')
    hours_lines_ar = models.JSONField('Hours Lines (Arabic)', default=list, blank=True)
    inquiries_lines = models.JSONField('Inquiries Lines', default=list, blank=True,
        help_text='Array of 2 strings: email, phone')
    inquiries_lines_ar = models.JSONField('Inquiries Lines (Arabic)', default=list, blank=True)
    support_lines = models.JSONField('Support Lines', default=list, blank=True,
        help_text='Array of 2 strings: email, phone')
    support_lines_ar = models.JSONField('Support Lines (Arabic)', default=list, blank=True)

    # --- Location / Map ---
    our_location = models.CharField('Our Location Heading', max_length=300, blank=True)
    our_location_ar = models.CharField('Our Location Heading (Arabic)', max_length=300, blank=True)
    our_location_text = models.TextField('Our Location Text', blank=True)
    our_location_text_ar = models.TextField('Our Location Text (Arabic)', blank=True)
    map_title = models.CharField('Map Title', max_length=300, blank=True)
    map_title_ar = models.CharField('Map Title (Arabic)', max_length=300, blank=True)
    map_embed_url = models.CharField('Map Embed URL', max_length=1000, blank=True)
    latitude = models.CharField('Latitude', max_length=50, blank=True)
    longitude = models.CharField('Longitude', max_length=50, blank=True)

    published = models.BooleanField('Published', default=True)

    class Meta:
        verbose_name = 'Contact Content'
        verbose_name_plural = 'Contact Content'

    def __str__(self):
        return 'Contact Content'

    def save(self, *args, **kwargs):
        if not self.pk and ContactContent.objects.exists():
            existing = ContactContent.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class MediaItem(TimeStampedModel):
    """Collection model for media library (images, videos, documents)."""

    slug = models.SlugField('Slug', max_length=320, unique=True)
    file_url = models.URLField('File URL', max_length=1000)
    filename = models.CharField('Filename', max_length=500)
    alt = models.CharField('Alt Text', max_length=300, blank=True)
    alt_ar = models.CharField('Alt Text (Arabic)', max_length=300, blank=True)
    caption = models.CharField('Caption', max_length=500, blank=True)
    caption_ar = models.CharField('Caption (Arabic)', max_length=500, blank=True)
    category = models.CharField('Category', max_length=20, choices=MediaCategory.choices, default=MediaCategory.IMAGE)
    file_size = models.PositiveIntegerField('File Size (bytes)', default=0)
    width = models.PositiveIntegerField('Width (px)', default=0)
    height = models.PositiveIntegerField('Height (px)', default=0)
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.PUBLISHED)

    class Meta:
        verbose_name = 'Media Item'
        verbose_name_plural = 'Media Items'
        ordering = ['-created_at']

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import unique_slug
            self.slug = unique_slug(MediaItem, self.filename or 'media', self.pk)
        super().save(*args, **kwargs)