from rest_framework import serializers

from .enums import ShortCategory
from .models import AboutContent, Category, Consultation, ContactContent, Emirate, HomepageContent, Initiative, MediaItem, NewsArticle, PagePresentation, Short
from .utils import unique_slug


class ShortAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    videoTitle = serializers.CharField(source='video_title', required=False, allow_blank=True)
    videoTitleAr = serializers.CharField(source='video_title_ar', required=False, allow_blank=True)
    maritalStage = serializers.CharField(source='marital_stage', required=False, allow_blank=True)
    coverImage = serializers.CharField(source='cover_image', required=False, allow_blank=True)
    publishedAt = serializers.DateTimeField(source='published_at', required=False, allow_null=True)
    videoUrl = serializers.CharField(source='video_url', required=False, allow_blank=True)
    keyTopics = serializers.JSONField(source='key_topics', required=False)
    shareUrl = serializers.CharField(source='share_url', required=False, allow_blank=True)
    showKeyTopics = serializers.BooleanField(source='show_key_topics', required=False)
    showResources = serializers.BooleanField(source='show_resources', required=False)
    showShare = serializers.BooleanField(source='show_share', required=False)
    showSpeaker = serializers.BooleanField(source='show_speaker', required=False)
    showViews = serializers.BooleanField(source='show_views', required=False)
    showRelated = serializers.BooleanField(source='show_related', required=False)

    class Meta:
        model = Short
        fields = ['id', 'videoTitle', 'videoTitleAr', 'slug', 'category', 'organization', 'family',
                  'language', 'maritalStage', 'duration', 'publishedAt', 'coverImage', 'videoUrl',
                  'speaker', 'views', 'description', 'keyTopics', 'resources', 'shareUrl',
                  'showKeyTopics', 'showResources', 'showShare', 'showSpeaker', 'showViews',
                  'showRelated', 'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(Short, instance.video_title or 'short', instance.pk)
            instance.save(update_fields=['slug'])
        return instance


class NewsAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    articleTitle = serializers.CharField(source='article_title', required=False, allow_blank=True)
    articleTitleAr = serializers.CharField(source='article_title_ar', required=False, allow_blank=True)
    editorialTeam = serializers.CharField(source='editorial_team', required=False, allow_blank=True)
    coverImage = serializers.CharField(source='cover_image', required=False, allow_blank=True)
    emirate = serializers.CharField(source='emirates', required=False, allow_blank=True)
    publishedDate = serializers.DateField(source='published_date', required=False, allow_null=True)
    updatedDate = serializers.DateField(source='updated_date', required=False, allow_null=True)
    shareUrl = serializers.CharField(source='share_url', required=False, allow_blank=True)
    showArticleInfo = serializers.BooleanField(source='show_article_info', required=False)
    showRelatedResources = serializers.BooleanField(source='show_related_resources', required=False)
    showShare = serializers.BooleanField(source='show_share', required=False)
    showRelatedStories = serializers.BooleanField(source='show_related_stories', required=False)

    class Meta:
        model = NewsArticle
        fields = ['id', 'slug', 'articleTitle', 'articleTitleAr', 'category', 'source', 'language',
                  'content', 'coverImage', 'author', 'editorialTeam', 'organization', 'moc', 'city',
                  'emirate', 'publishedDate', 'updatedDate', 'resources', 'shareUrl', 'showArticleInfo',
                  'showRelatedResources', 'showShare', 'showRelatedStories', 'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(NewsArticle, instance.article_title or 'news', instance.pk)
            instance.save(update_fields=['slug'])
        return instance


class InitiativeAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    titleAr = serializers.CharField(source='title_ar', required=False, allow_blank=True)
    subtitleAr = serializers.CharField(source='subtitle_ar', required=False, allow_blank=True)
    startDate = serializers.DateField(source='start_date', required=False, allow_null=True)
    endDate = serializers.DateField(source='end_date', required=False, allow_null=True)
    coverImage = serializers.CharField(source='cover_image', required=False, allow_blank=True)
    officialWebsiteUrl = serializers.CharField(source='official_website_url', required=False, allow_blank=True)
    shareUrl = serializers.CharField(source='share_url', required=False, allow_blank=True)
    supportOffered = serializers.JSONField(source='support_offered', required=False)
    basicInformation = serializers.JSONField(source='basic_information', required=False)
    isFeatured = serializers.BooleanField(source='is_featured', required=False)
    isListed = serializers.BooleanField(source='is_listed', required=False)
    showAbout = serializers.BooleanField(source='show_about', required=False)
    showSupportOffered = serializers.BooleanField(source='show_support_offered', required=False)
    showBenefits = serializers.BooleanField(source='show_benefits', required=False)
    showApplicationForm = serializers.BooleanField(source='show_application_form', required=False)

    class Meta:
        model = Initiative
        fields = ['id', 'slug', 'title', 'titleAr', 'subtitle', 'subtitleAr', 'category', 'emirates',
                  'description', 'purpose', 'objectives', 'basicInformation', 'supportOffered',
                  'benefits', 'startDate', 'endDate', 'coverImage', 'badge', 'contact',
                  'officialWebsiteUrl', 'shareUrl', 'isFeatured', 'isListed',
                  'showAbout', 'showSupportOffered',
                  'showBenefits', 'showApplicationForm', 'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(Initiative, instance.title or 'initiative', instance.pk)
            instance.save(update_fields=['slug'])
        return instance


class ConsultationAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    sessionTitle = serializers.CharField(source='session_title', required=False, allow_blank=True)
    sessionTitleAr = serializers.CharField(source='session_title_ar', required=False, allow_blank=True)
    sessionType = serializers.CharField(source='session_type', required=False, allow_blank=True)
    maritalStage = serializers.CharField(source='marital_stage', required=False, allow_blank=True)
    startTime = serializers.CharField(source='start_time', required=False, allow_blank=True)
    endTime = serializers.CharField(source='end_time', required=False, allow_blank=True)
    isFree = serializers.BooleanField(source='is_free', required=False)
    seatsLeft = serializers.IntegerField(source='max_participants', required=False)
    coverImage = serializers.CharField(source='gallery', required=False, allow_blank=True)
    publishedDate = serializers.DateField(source='published_date', required=False, allow_null=True)
    timeZone = serializers.CharField(source='time_zone', required=False, allow_blank=True)
    meetingFormat = serializers.CharField(source='meeting_format', required=False, allow_blank=True)
    sessionLink = serializers.CharField(source='session_link', required=False, allow_blank=True)
    maxParticipants = serializers.IntegerField(source='max_participants', required=False)
    processingFee = serializers.DecimalField(source='processing_fee', max_digits=10, decimal_places=2, required=False)
    counselorPhoto = serializers.CharField(source='counselor_photo', required=False, allow_blank=True)
    counselorTitle = serializers.CharField(source='counselor_title', required=False, allow_blank=True)
    counselorBio = serializers.CharField(source='counselor_bio', required=False, allow_blank=True)
    learnMore = serializers.JSONField(source='learn_more', required=False)
    whatYouWillLearn = serializers.JSONField(source='what_you_will_learn', required=False)
    whoShouldAttend = serializers.JSONField(source='who_should_attend', required=False)
    bookingNotice = serializers.CharField(source='booking_notice', required=False, allow_blank=True)
    showDoctor = serializers.BooleanField(source='show_doctor', required=False)
    showLearnMore = serializers.BooleanField(source='show_learn_more', required=False)
    showGallery = serializers.BooleanField(source='show_gallery', required=False)
    showSchedule = serializers.BooleanField(source='show_schedule', required=False)
    showBooking = serializers.BooleanField(source='show_booking', required=False)
    isBookable = serializers.BooleanField(source='is_bookable', required=False)

    class Meta:
        model = Consultation
        fields = ['id', 'slug', 'sessionTitle', 'sessionTitleAr', 'category', 'sessionType',
                  'emirates', 'maritalStage', 'language', 'date', 'startTime', 'endTime', 'duration',
                  'isFree', 'fee', 'seatsLeft', 'coverImage', 'publishedDate', 'timeZone',
                  'meetingFormat', 'sessionLink', 'maxParticipants', 'processingFee', 'discount',
                  'counselor', 'counselorPhoto', 'counselorTitle', 'counselorBio', 'learnMore',
                  'gallery', 'description', 'objectives', 'whatYouWillLearn', 'whoShouldAttend',
                  'schedule', 'bookingNotice', 'showDoctor', 'showLearnMore', 'showGallery',
                  'showSchedule', 'showBooking', 'isBookable', 'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(Consultation, instance.session_title or 'consultation', instance.pk)
            instance.save(update_fields=['slug'])
        return instance


class EmirateAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    emiratesName = serializers.CharField(source='emirates_name', required=False, allow_blank=True)
    emiratesNameAr = serializers.CharField(source='emirates_name_ar', required=False, allow_blank=True)
    dateTime = serializers.DateTimeField(source='date_time', required=False, allow_null=True)
    contactPhone = serializers.CharField(source='contact_phone', required=False, allow_blank=True)
    serviceCenters = serializers.IntegerField(source='service_centers', required=False)
    centerCount = serializers.CharField(source='center_count', required=False, allow_blank=True)
    websiteUrl = serializers.CharField(source='website_url', required=False, allow_blank=True)
    showStatus = serializers.BooleanField(source='show_status', required=False)

    class Meta:
        model = Emirate
        fields = ['id', 'slug', 'emiratesName', 'emiratesNameAr', 'title', 'description', 'dateTime',
                  'contactPhone', 'serviceCenters', 'centerCount', 'image', 'websiteUrl', 'showStatus',
                  'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(Emirate, instance.emirates_name or 'emirate', instance.pk)
            instance.save(update_fields=['slug'])
        return instance


class CategoryAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    category = serializers.CharField(source='name', required=False, allow_blank=True)

    class Meta:
        model = Category
        fields = ['id', 'category', 'description', 'date', 'status']
        read_only_fields = ['id']


class PagePresentationAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    titleAr = serializers.CharField(source='title_ar', required=False, allow_blank=True)
    descriptionAr = serializers.CharField(source='description_ar', required=False, allow_blank=True)
    heroImage = serializers.CharField(source='hero_image', required=False, allow_blank=True)
    topics = serializers.JSONField(source='shorts_topics', required=False)
    contributors = serializers.JSONField(source='shorts_contributors', required=False)
    faqs = serializers.JSONField(source='shorts_faqs', required=False)
    sectionVisibility = serializers.JSONField(source='shorts_section_visibility', required=False)
    initiativesTopics = serializers.JSONField(source='initiatives_topics', required=False)
    initiativesContributors = serializers.JSONField(source='initiatives_contributors', required=False)
    initiativesFaqs = serializers.JSONField(source='initiatives_faqs', required=False)
    initiativesSectionVisibility = serializers.JSONField(source='initiatives_section_visibility', required=False)
    consultationTopics = serializers.JSONField(source='consultation_topics', required=False)
    consultationContributors = serializers.JSONField(source='consultation_contributors', required=False)
    consultationFaqs = serializers.JSONField(source='consultation_faqs', required=False)
    consultationSectionVisibility = serializers.JSONField(source='consultation_section_visibility', required=False)
    emiratesTopics = serializers.JSONField(source='emirates_topics', required=False)
    emiratesContributors = serializers.JSONField(source='emirates_contributors', required=False)
    emiratesFaqs = serializers.JSONField(source='emirates_faqs', required=False)
    emiratesSectionVisibility = serializers.JSONField(source='emirates_section_visibility', required=False)
    newsTopics = serializers.JSONField(source='news_topics', required=False)
    newsContributors = serializers.JSONField(source='news_contributors', required=False)
    newsFaqs = serializers.JSONField(source='news_faqs', required=False)
    newsSectionVisibility = serializers.JSONField(source='news_section_visibility', required=False)

    class Meta:
        model = PagePresentation
        fields = ['id', 'key', 'title', 'titleAr', 'description', 'descriptionAr', 'badge',
                  'heroImage', 'published', 'topics', 'contributors', 'faqs', 'sectionVisibility',
                  'initiativesTopics', 'initiativesContributors', 'initiativesFaqs',
                  'initiativesSectionVisibility',
                  'consultationTopics', 'consultationContributors', 'consultationFaqs',
                  'consultationSectionVisibility',
                  'emiratesTopics', 'emiratesContributors', 'emiratesFaqs',
                  'emiratesSectionVisibility',
                  'newsTopics', 'newsContributors', 'newsFaqs',
                  'newsSectionVisibility']
        read_only_fields = ['id', 'key']


class HomepageContentAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)

    # Hero
    heroEyebrow = serializers.CharField(source='hero_eyebrow', required=False, allow_blank=True)
    heroEyebrowAr = serializers.CharField(source='hero_eyebrow_ar', required=False, allow_blank=True)
    heroTitle = serializers.CharField(source='hero_title', required=False, allow_blank=True)
    heroTitleAr = serializers.CharField(source='hero_title_ar', required=False, allow_blank=True)
    heroSubtitle = serializers.CharField(source='hero_subtitle', required=False, allow_blank=True)
    heroSubtitleAr = serializers.CharField(source='hero_subtitle_ar', required=False, allow_blank=True)
    heroSearchPlaceholder = serializers.CharField(source='hero_search_placeholder', required=False, allow_blank=True)
    heroSearchPlaceholderAr = serializers.CharField(source='hero_search_placeholder_ar', required=False, allow_blank=True)
    heroSearchButton = serializers.CharField(source='hero_search_button', required=False, allow_blank=True)
    heroSearchButtonAr = serializers.CharField(source='hero_search_button_ar', required=False, allow_blank=True)
    heroPrimaryCtaLabel = serializers.CharField(source='hero_primary_cta_label', required=False, allow_blank=True)
    heroPrimaryCtaLabelAr = serializers.CharField(source='hero_primary_cta_label_ar', required=False, allow_blank=True)
    heroPrimaryCtaLink = serializers.CharField(source='hero_primary_cta_link', required=False, allow_blank=True)
    heroSecondaryCtaLabel = serializers.CharField(source='hero_secondary_cta_label', required=False, allow_blank=True)
    heroSecondaryCtaLabelAr = serializers.CharField(source='hero_secondary_cta_label_ar', required=False, allow_blank=True)
    heroSecondaryCtaLink = serializers.CharField(source='hero_secondary_cta_link', required=False, allow_blank=True)
    heroImage = serializers.CharField(source='hero_image', required=False, allow_blank=True)
    heroImageAlt = serializers.CharField(source='hero_image_alt', required=False, allow_blank=True)
    heroFloatingCards = serializers.JSONField(source='hero_floating_cards', required=False)

    # Stats
    stats = serializers.JSONField(required=False)

    # Shorts
    shortsTitle = serializers.CharField(source='shorts_title', required=False, allow_blank=True)
    shortsTitleAr = serializers.CharField(source='shorts_title_ar', required=False, allow_blank=True)
    shortsSubtitle = serializers.CharField(source='shorts_subtitle', required=False, allow_blank=True)
    shortsSubtitleAr = serializers.CharField(source='shorts_subtitle_ar', required=False, allow_blank=True)
    shortsCtaLabel = serializers.CharField(source='shorts_cta_label', required=False, allow_blank=True)
    shortsCtaLabelAr = serializers.CharField(source='shorts_cta_label_ar', required=False, allow_blank=True)
    shortsEmptyText = serializers.CharField(source='shorts_empty_text', required=False, allow_blank=True)
    shortsEmptyTextAr = serializers.CharField(source='shorts_empty_text_ar', required=False, allow_blank=True)

    # News
    newsTitle = serializers.CharField(source='news_title', required=False, allow_blank=True)
    newsTitleAr = serializers.CharField(source='news_title_ar', required=False, allow_blank=True)
    newsSubtitle = serializers.CharField(source='news_subtitle', required=False, allow_blank=True)
    newsSubtitleAr = serializers.CharField(source='news_subtitle_ar', required=False, allow_blank=True)
    newsCtaLabel = serializers.CharField(source='news_cta_label', required=False, allow_blank=True)
    newsCtaLabelAr = serializers.CharField(source='news_cta_label_ar', required=False, allow_blank=True)

    # Initiatives
    initiativesTitle = serializers.CharField(source='initiatives_title', required=False, allow_blank=True)
    initiativesTitleAr = serializers.CharField(source='initiatives_title_ar', required=False, allow_blank=True)
    initiativesSubtitle = serializers.CharField(source='initiatives_subtitle', required=False, allow_blank=True)
    initiativesSubtitleAr = serializers.CharField(source='initiatives_subtitle_ar', required=False, allow_blank=True)
    initiativesCtaLabel = serializers.CharField(source='initiatives_cta_label', required=False, allow_blank=True)
    initiativesCtaLabelAr = serializers.CharField(source='initiatives_cta_label_ar', required=False, allow_blank=True)

    # Consultations
    consultationsTitle = serializers.CharField(source='consultations_title', required=False, allow_blank=True)
    consultationsTitleAr = serializers.CharField(source='consultations_title_ar', required=False, allow_blank=True)
    consultationsSubtitle = serializers.CharField(source='consultations_subtitle', required=False, allow_blank=True)
    consultationsSubtitleAr = serializers.CharField(source='consultations_subtitle_ar', required=False, allow_blank=True)
    consultationsCtaLabel = serializers.CharField(source='consultations_cta_label', required=False, allow_blank=True)
    consultationsCtaLabelAr = serializers.CharField(source='consultations_cta_label_ar', required=False, allow_blank=True)
    consultationsFreeTab = serializers.CharField(source='consultations_free_tab', required=False, allow_blank=True)
    consultationsFreeTabAr = serializers.CharField(source='consultations_free_tab_ar', required=False, allow_blank=True)
    consultationsPaidTab = serializers.CharField(source='consultations_paid_tab', required=False, allow_blank=True)
    consultationsPaidTabAr = serializers.CharField(source='consultations_paid_tab_ar', required=False, allow_blank=True)

    # Emirates
    emiratesTitle = serializers.CharField(source='emirates_title', required=False, allow_blank=True)
    emiratesTitleAr = serializers.CharField(source='emirates_title_ar', required=False, allow_blank=True)
    emiratesSubtitle = serializers.CharField(source='emirates_subtitle', required=False, allow_blank=True)
    emiratesSubtitleAr = serializers.CharField(source='emirates_subtitle_ar', required=False, allow_blank=True)
    emiratesCapitalLabel = serializers.CharField(source='emirates_capital_label', required=False, allow_blank=True)
    emiratesCapitalLabelAr = serializers.CharField(source='emirates_capital_label_ar', required=False, allow_blank=True)
    emiratesHeadquartersLabel = serializers.CharField(source='emirates_headquarters_label', required=False, allow_blank=True)
    emiratesHeadquartersLabelAr = serializers.CharField(source='emirates_headquarters_label_ar', required=False, allow_blank=True)
    emiratesCtaLabel = serializers.CharField(source='emirates_cta_label', required=False, allow_blank=True)
    emiratesCtaLabelAr = serializers.CharField(source='emirates_cta_label_ar', required=False, allow_blank=True)

    # CTA
    ctaTitle = serializers.CharField(source='cta_title', required=False, allow_blank=True)
    ctaTitleAr = serializers.CharField(source='cta_title_ar', required=False, allow_blank=True)
    ctaSubtitle = serializers.CharField(source='cta_subtitle', required=False, allow_blank=True)
    ctaSubtitleAr = serializers.CharField(source='cta_subtitle_ar', required=False, allow_blank=True)
    ctaPrimaryLabel = serializers.CharField(source='cta_primary_label', required=False, allow_blank=True)
    ctaPrimaryLabelAr = serializers.CharField(source='cta_primary_label_ar', required=False, allow_blank=True)
    ctaPrimaryLink = serializers.CharField(source='cta_primary_link', required=False, allow_blank=True)
    ctaSecondaryLabel = serializers.CharField(source='cta_secondary_label', required=False, allow_blank=True)
    ctaSecondaryLabelAr = serializers.CharField(source='cta_secondary_label_ar', required=False, allow_blank=True)
    ctaSecondaryLink = serializers.CharField(source='cta_secondary_link', required=False, allow_blank=True)

    sectionVisibility = serializers.JSONField(source='section_visibility', required=False)

    class Meta:
        model = HomepageContent
        fields = ['id',
                  'heroEyebrow', 'heroEyebrowAr', 'heroTitle', 'heroTitleAr',
                  'heroSubtitle', 'heroSubtitleAr', 'heroSearchPlaceholder', 'heroSearchPlaceholderAr',
                  'heroSearchButton', 'heroSearchButtonAr',
                  'heroPrimaryCtaLabel', 'heroPrimaryCtaLabelAr', 'heroPrimaryCtaLink',
                  'heroSecondaryCtaLabel', 'heroSecondaryCtaLabelAr', 'heroSecondaryCtaLink',
                  'heroImage', 'heroImageAlt', 'heroFloatingCards',
                  'stats',
                  'shortsTitle', 'shortsTitleAr', 'shortsSubtitle', 'shortsSubtitleAr',
                  'shortsCtaLabel', 'shortsCtaLabelAr', 'shortsEmptyText', 'shortsEmptyTextAr',
                  'newsTitle', 'newsTitleAr', 'newsSubtitle', 'newsSubtitleAr',
                  'newsCtaLabel', 'newsCtaLabelAr',
                  'initiativesTitle', 'initiativesTitleAr', 'initiativesSubtitle', 'initiativesSubtitleAr',
                  'initiativesCtaLabel', 'initiativesCtaLabelAr',
                  'consultationsTitle', 'consultationsTitleAr', 'consultationsSubtitle', 'consultationsSubtitleAr',
                  'consultationsCtaLabel', 'consultationsCtaLabelAr',
                  'consultationsFreeTab', 'consultationsFreeTabAr', 'consultationsPaidTab', 'consultationsPaidTabAr',
                  'emiratesTitle', 'emiratesTitleAr', 'emiratesSubtitle', 'emiratesSubtitleAr',
                  'emiratesCapitalLabel', 'emiratesCapitalLabelAr',
                  'emiratesHeadquartersLabel', 'emiratesHeadquartersLabelAr',
                  'emiratesCtaLabel', 'emiratesCtaLabelAr',
                  'ctaTitle', 'ctaTitleAr', 'ctaSubtitle', 'ctaSubtitleAr',
                  'ctaPrimaryLabel', 'ctaPrimaryLabelAr', 'ctaPrimaryLink',
                  'ctaSecondaryLabel', 'ctaSecondaryLabelAr', 'ctaSecondaryLink',
                  'sectionVisibility',
                  'published']
        read_only_fields = ['id']


class AboutContentAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)

    titleAr = serializers.CharField(source='title_ar', required=False, allow_blank=True)
    descriptionAr = serializers.CharField(source='description_ar', required=False, allow_blank=True)
    browseSession = serializers.CharField(source='browse_session', required=False, allow_blank=True)
    browseSessionAr = serializers.CharField(source='browse_session_ar', required=False, allow_blank=True)
    contactSupport = serializers.CharField(source='contact_support', required=False, allow_blank=True)
    contactSupportAr = serializers.CharField(source='contact_support_ar', required=False, allow_blank=True)
    heroImage = serializers.CharField(source='hero_image', required=False, allow_blank=True)
    heroImageAlt = serializers.CharField(source='hero_image_alt', required=False, allow_blank=True)

    ourStory = serializers.CharField(source='our_story', required=False, allow_blank=True)
    ourStoryAr = serializers.CharField(source='our_story_ar', required=False, allow_blank=True)
    ourStoryText = serializers.CharField(source='our_story_text', required=False, allow_blank=True)
    ourStoryTextAr = serializers.CharField(source='our_story_text_ar', required=False, allow_blank=True)

    ourMission = serializers.CharField(source='our_mission', required=False, allow_blank=True)
    ourMissionAr = serializers.CharField(source='our_mission_ar', required=False, allow_blank=True)
    ourMissionText = serializers.CharField(source='our_mission_text', required=False, allow_blank=True)
    ourMissionTextAr = serializers.CharField(source='our_mission_text_ar', required=False, allow_blank=True)

    ourVision = serializers.CharField(source='our_vision', required=False, allow_blank=True)
    ourVisionAr = serializers.CharField(source='our_vision_ar', required=False, allow_blank=True)
    ourVisionText = serializers.CharField(source='our_vision_text', required=False, allow_blank=True)
    ourVisionTextAr = serializers.CharField(source='our_vision_text_ar', required=False, allow_blank=True)

    ourObjective = serializers.CharField(source='our_objective', required=False, allow_blank=True)
    ourObjectiveAr = serializers.CharField(source='our_objective_ar', required=False, allow_blank=True)
    ourObjectiveText = serializers.CharField(source='our_objective_text', required=False, allow_blank=True)
    ourObjectiveTextAr = serializers.CharField(source='our_objective_text_ar', required=False, allow_blank=True)
    objectives = serializers.JSONField(required=False)

    whatWeOffer = serializers.CharField(source='what_we_offer', required=False, allow_blank=True)
    whatWeOfferAr = serializers.CharField(source='what_we_offer_ar', required=False, allow_blank=True)
    whatWeOfferText = serializers.CharField(source='what_we_offer_text', required=False, allow_blank=True)
    whatWeOfferTextAr = serializers.CharField(source='what_we_offer_text_ar', required=False, allow_blank=True)
    offerings = serializers.JSONField(required=False)

    ourImpact = serializers.CharField(source='our_impact', required=False, allow_blank=True)
    ourImpactAr = serializers.CharField(source='our_impact_ar', required=False, allow_blank=True)
    ourImpactText = serializers.CharField(source='our_impact_text', required=False, allow_blank=True)
    ourImpactTextAr = serializers.CharField(source='our_impact_text_ar', required=False, allow_blank=True)
    impact = serializers.JSONField(required=False)

    whyChoose = serializers.CharField(source='why_choose', required=False, allow_blank=True)
    whyChooseAr = serializers.CharField(source='why_choose_ar', required=False, allow_blank=True)
    whyChooseText = serializers.CharField(source='why_choose_text', required=False, allow_blank=True)
    whyChooseTextAr = serializers.CharField(source='why_choose_text_ar', required=False, allow_blank=True)
    whyValues = serializers.JSONField(source='why_values', required=False)

    coreValues = serializers.CharField(source='core_values', required=False, allow_blank=True)
    coreValuesAr = serializers.CharField(source='core_values_ar', required=False, allow_blank=True)
    coreValuesText = serializers.CharField(source='core_values_text', required=False, allow_blank=True)
    coreValuesTextAr = serializers.CharField(source='core_values_text_ar', required=False, allow_blank=True)
    coreValueList = serializers.JSONField(source='core_value_list', required=False)

    class Meta:
        model = AboutContent
        fields = ['id',
                  'title', 'titleAr', 'description', 'descriptionAr',
                  'browseSession', 'browseSessionAr', 'contactSupport', 'contactSupportAr',
                  'heroImage', 'heroImageAlt',
                  'ourStory', 'ourStoryAr', 'ourStoryText', 'ourStoryTextAr',
                  'ourMission', 'ourMissionAr', 'ourMissionText', 'ourMissionTextAr',
                  'ourVision', 'ourVisionAr', 'ourVisionText', 'ourVisionTextAr',
                  'ourObjective', 'ourObjectiveAr', 'ourObjectiveText', 'ourObjectiveTextAr', 'objectives',
                  'whatWeOffer', 'whatWeOfferAr', 'whatWeOfferText', 'whatWeOfferTextAr', 'offerings',
                  'ourImpact', 'ourImpactAr', 'ourImpactText', 'ourImpactTextAr', 'impact',
                  'whyChoose', 'whyChooseAr', 'whyChooseText', 'whyChooseTextAr', 'whyValues',
                  'coreValues', 'coreValuesAr', 'coreValuesText', 'coreValuesTextAr', 'coreValueList',
                  'published']
        read_only_fields = ['id']


class ContactContentAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)

    titleAr = serializers.CharField(source='title_ar', required=False, allow_blank=True)
    descriptionAr = serializers.CharField(source='description_ar', required=False, allow_blank=True)
    browseSession = serializers.CharField(source='browse_session', required=False, allow_blank=True)
    browseSessionAr = serializers.CharField(source='browse_session_ar', required=False, allow_blank=True)
    contactSupport = serializers.CharField(source='contact_support', required=False, allow_blank=True)
    contactSupportAr = serializers.CharField(source='contact_support_ar', required=False, allow_blank=True)

    sendMessage = serializers.CharField(source='send_message', required=False, allow_blank=True)
    sendMessageAr = serializers.CharField(source='send_message_ar', required=False, allow_blank=True)
    sendMessageSub = serializers.CharField(source='send_message_sub', required=False, allow_blank=True)
    sendMessageSubAr = serializers.CharField(source='send_message_sub_ar', required=False, allow_blank=True)
    fullName = serializers.CharField(source='full_name', required=False, allow_blank=True)
    fullNameAr = serializers.CharField(source='full_name_ar', required=False, allow_blank=True)
    fullNamePlaceholder = serializers.CharField(source='full_name_placeholder', required=False, allow_blank=True)
    fullNamePlaceholderAr = serializers.CharField(source='full_name_placeholder_ar', required=False, allow_blank=True)
    emailLabel = serializers.CharField(source='email_label', required=False, allow_blank=True)
    emailLabelAr = serializers.CharField(source='email_label_ar', required=False, allow_blank=True)
    emailPlaceholder = serializers.CharField(source='email_placeholder', required=False, allow_blank=True)
    emailPlaceholderAr = serializers.CharField(source='email_placeholder_ar', required=False, allow_blank=True)
    userType = serializers.CharField(source='user_type', required=False, allow_blank=True)
    userTypeAr = serializers.CharField(source='user_type_ar', required=False, allow_blank=True)
    selectUserType = serializers.CharField(source='select_user_type', required=False, allow_blank=True)
    selectUserTypeAr = serializers.CharField(source='select_user_type_ar', required=False, allow_blank=True)
    individual = serializers.CharField(required=False, allow_blank=True)
    individualAr = serializers.CharField(source='individual_ar', required=False, allow_blank=True)
    couple = serializers.CharField(required=False, allow_blank=True)
    coupleAr = serializers.CharField(source='couple_ar', required=False, allow_blank=True)
    organization = serializers.CharField(required=False, allow_blank=True)
    organizationAr = serializers.CharField(source='organization_ar', required=False, allow_blank=True)
    subjectLabel = serializers.CharField(source='subject_label', required=False, allow_blank=True)
    subjectLabelAr = serializers.CharField(source='subject_label_ar', required=False, allow_blank=True)
    subjectPlaceholder = serializers.CharField(source='subject_placeholder', required=False, allow_blank=True)
    subjectPlaceholderAr = serializers.CharField(source='subject_placeholder_ar', required=False, allow_blank=True)
    phoneLabel = serializers.CharField(source='phone_label', required=False, allow_blank=True)
    phoneLabelAr = serializers.CharField(source='phone_label_ar', required=False, allow_blank=True)
    phonePlaceholder = serializers.CharField(source='phone_placeholder', required=False, allow_blank=True)
    phonePlaceholderAr = serializers.CharField(source='phone_placeholder_ar', required=False, allow_blank=True)
    messageLabel = serializers.CharField(source='message_label', required=False, allow_blank=True)
    messageLabelAr = serializers.CharField(source='message_label_ar', required=False, allow_blank=True)
    messagePlaceholder = serializers.CharField(source='message_placeholder', required=False, allow_blank=True)
    messagePlaceholderAr = serializers.CharField(source='message_placeholder_ar', required=False, allow_blank=True)
    sendButton = serializers.CharField(source='send_button', required=False, allow_blank=True)
    sendButtonAr = serializers.CharField(source='send_button_ar', required=False, allow_blank=True)
    successMessage = serializers.CharField(source='success_message', required=False, allow_blank=True)
    successMessageAr = serializers.CharField(source='success_message_ar', required=False, allow_blank=True)
    sending = serializers.CharField(required=False, allow_blank=True)
    sendingAr = serializers.CharField(source='sending_ar', required=False, allow_blank=True)

    contactInfo = serializers.CharField(source='contact_info', required=False, allow_blank=True)
    contactInfoAr = serializers.CharField(source='contact_info_ar', required=False, allow_blank=True)
    officeAddress = serializers.CharField(source='office_address', required=False, allow_blank=True)
    officeAddressAr = serializers.CharField(source='office_address_ar', required=False, allow_blank=True)
    workingHours = serializers.CharField(source='working_hours', required=False, allow_blank=True)
    workingHoursAr = serializers.CharField(source='working_hours_ar', required=False, allow_blank=True)
    generalInquiries = serializers.CharField(source='general_inquiries', required=False, allow_blank=True)
    generalInquiriesAr = serializers.CharField(source='general_inquiries_ar', required=False, allow_blank=True)
    supportHeading = serializers.CharField(source='support_heading', required=False, allow_blank=True)
    supportHeadingAr = serializers.CharField(source='support_heading_ar', required=False, allow_blank=True)
    addressLines = serializers.JSONField(source='address_lines', required=False)
    addressLinesAr = serializers.JSONField(source='address_lines_ar', required=False)
    hoursLines = serializers.JSONField(source='hours_lines', required=False)
    hoursLinesAr = serializers.JSONField(source='hours_lines_ar', required=False)
    inquiriesLines = serializers.JSONField(source='inquiries_lines', required=False)
    inquiriesLinesAr = serializers.JSONField(source='inquiries_lines_ar', required=False)
    supportLines = serializers.JSONField(source='support_lines', required=False)
    supportLinesAr = serializers.JSONField(source='support_lines_ar', required=False)

    ourLocation = serializers.CharField(source='our_location', required=False, allow_blank=True)
    ourLocationAr = serializers.CharField(source='our_location_ar', required=False, allow_blank=True)
    ourLocationText = serializers.CharField(source='our_location_text', required=False, allow_blank=True)
    ourLocationTextAr = serializers.CharField(source='our_location_text_ar', required=False, allow_blank=True)
    mapTitle = serializers.CharField(source='map_title', required=False, allow_blank=True)
    mapTitleAr = serializers.CharField(source='map_title_ar', required=False, allow_blank=True)
    mapEmbedUrl = serializers.CharField(source='map_embed_url', required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ContactContent
        fields = ['id',
                  'title', 'titleAr', 'description', 'descriptionAr',
                  'browseSession', 'browseSessionAr', 'contactSupport', 'contactSupportAr',
                  'sendMessage', 'sendMessageAr', 'sendMessageSub', 'sendMessageSubAr',
                  'fullName', 'fullNameAr', 'fullNamePlaceholder', 'fullNamePlaceholderAr',
                  'emailLabel', 'emailLabelAr', 'emailPlaceholder', 'emailPlaceholderAr',
                  'userType', 'userTypeAr', 'selectUserType', 'selectUserTypeAr',
                  'individual', 'individualAr', 'couple', 'coupleAr',
                  'organization', 'organizationAr',
                  'subjectLabel', 'subjectLabelAr', 'subjectPlaceholder', 'subjectPlaceholderAr',
                  'phoneLabel', 'phoneLabelAr', 'phonePlaceholder', 'phonePlaceholderAr',
                  'messageLabel', 'messageLabelAr', 'messagePlaceholder', 'messagePlaceholderAr',
                  'sendButton', 'sendButtonAr', 'successMessage', 'successMessageAr',
                  'sending', 'sendingAr',
                  'contactInfo', 'contactInfoAr', 'officeAddress', 'officeAddressAr',
                  'workingHours', 'workingHoursAr', 'generalInquiries', 'generalInquiriesAr',
                  'supportHeading', 'supportHeadingAr',
                  'addressLines', 'addressLinesAr', 'hoursLines', 'hoursLinesAr',
                  'inquiriesLines', 'inquiriesLinesAr', 'supportLines', 'supportLinesAr',
                  'ourLocation', 'ourLocationAr', 'ourLocationText', 'ourLocationTextAr',
                  'mapTitle', 'mapTitleAr', 'mapEmbedUrl', 'latitude', 'longitude',
                  'published']
        read_only_fields = ['id']


class MediaItemAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    fileUrl = serializers.URLField(source='file_url', required=False, allow_blank=True)
    altAr = serializers.CharField(source='alt_ar', required=False, allow_blank=True)
    captionAr = serializers.CharField(source='caption_ar', required=False, allow_blank=True)
    fileSize = serializers.IntegerField(source='file_size', required=False)

    class Meta:
        model = MediaItem
        fields = ['id', 'slug', 'fileUrl', 'filename', 'alt', 'altAr', 'caption', 'captionAr',
                  'category', 'fileSize', 'width', 'height', 'status']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = unique_slug(MediaItem, instance.filename or 'media', instance.pk)
            instance.save(update_fields=['slug'])
        return instance