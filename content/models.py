import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .enums import (
    Emirates,
    Language,
    MaritalStage,
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

    class Meta:
        verbose_name = 'Page Presentation'
        verbose_name_plural = 'Page Presentations'
        ordering = ['key']

    def __str__(self):
        return dict(self.SECTION_CHOICES).get(self.key, self.key)