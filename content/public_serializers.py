from django.db.models import Q

from rest_framework import serializers

from .models import Category, Consultation, Emirate, HomepageContent, Initiative, NewsArticle, PagePresentation, Short


class ShortListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    videoTitle = serializers.CharField(source='video_title', read_only=True)
    videoTitleAr = serializers.CharField(source='video_title_ar', read_only=True)
    maritalStage = serializers.CharField(source='marital_stage', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    publishedAt = serializers.DateTimeField(source='published_at', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Short
        fields = ['id', 'videoTitle', 'videoTitleAr', 'slug', 'category', 'organization',
                  'maritalStage', 'duration', 'coverImage', 'views', 'publishedAt', 'status']


class ShortDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    videoTitle = serializers.CharField(source='video_title', read_only=True)
    videoTitleAr = serializers.CharField(source='video_title_ar', read_only=True)
    maritalStage = serializers.CharField(source='marital_stage', read_only=True)
    publishedAt = serializers.DateTimeField(source='published_at', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    videoUrl = serializers.CharField(source='video_url', read_only=True)
    keyTopics = serializers.JSONField(source='key_topics', read_only=True)
    shareUrl = serializers.CharField(source='share_url', read_only=True)
    showKeyTopics = serializers.BooleanField(source='show_key_topics', read_only=True)
    showResources = serializers.BooleanField(source='show_resources', read_only=True)
    showShare = serializers.BooleanField(source='show_share', read_only=True)
    showSpeaker = serializers.BooleanField(source='show_speaker', read_only=True)
    showViews = serializers.BooleanField(source='show_views', read_only=True)
    showRelated = serializers.BooleanField(source='show_related', read_only=True)
    lastUpdated = serializers.DateTimeField(source='updated_at', read_only=True)
    relatedVideos = serializers.SerializerMethodField()

    class Meta:
        model = Short
        fields = ['id', 'videoTitle', 'videoTitleAr', 'slug', 'category', 'organization', 'family',
                  'language', 'maritalStage', 'duration', 'publishedAt', 'coverImage', 'videoUrl',
                  'speaker', 'views', 'description', 'keyTopics', 'resources', 'shareUrl',
                  'showKeyTopics', 'showResources', 'showShare', 'showSpeaker', 'showViews',
                  'showRelated', 'status', 'lastUpdated', 'relatedVideos']

    def get_relatedVideos(self, obj):
        qs = Short.objects.filter(
            category=obj.category, status='Published'
        ).exclude(pk=obj.pk).order_by('-published_at')[:4]
        return ShortListSerializer(qs, many=True).data


class NewsListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    articleTitle = serializers.CharField(source='article_title', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    publishedDate = serializers.DateField(source='published_date', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'slug', 'articleTitle', 'category', 'source', 'coverImage',
                  'publishedDate', 'status']


class RelatedStorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    articleTitle = serializers.CharField(source='article_title', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    publishedDate = serializers.DateField(source='published_date', read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'slug', 'articleTitle', 'category', 'coverImage', 'publishedDate']


class NewsDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    articleTitle = serializers.CharField(source='article_title', read_only=True)
    articleTitleAr = serializers.CharField(source='article_title_ar', read_only=True)
    editorialTeam = serializers.CharField(source='editorial_team', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    emirate = serializers.CharField(source='emirates', read_only=True)
    publishedDate = serializers.DateField(source='published_date', read_only=True)
    updatedDate = serializers.DateField(source='updated_date', read_only=True)
    shareUrl = serializers.CharField(source='share_url', read_only=True)
    showArticleInfo = serializers.BooleanField(source='show_article_info', read_only=True)
    showRelatedResources = serializers.BooleanField(source='show_related_resources', read_only=True)
    showShare = serializers.BooleanField(source='show_share', read_only=True)
    showRelatedStories = serializers.BooleanField(source='show_related_stories', read_only=True)
    relatedStories = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = ['id', 'slug', 'articleTitle', 'articleTitleAr', 'category', 'source', 'language',
                  'content', 'coverImage', 'author', 'editorialTeam', 'organization', 'moc', 'city',
                  'emirate', 'publishedDate', 'updatedDate', 'resources', 'shareUrl', 'showArticleInfo',
                  'showRelatedResources', 'showShare', 'showRelatedStories', 'status', 'relatedStories']

    def get_relatedStories(self, obj):
        qs = NewsArticle.objects.filter(
            category=obj.category, status='Published'
        ).exclude(pk=obj.pk).order_by('-published_date')[:3]
        return RelatedStorySerializer(qs, many=True).data


class InitiativeListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    titleAr = serializers.CharField(source='title_ar', read_only=True)
    subtitleAr = serializers.CharField(source='subtitle_ar', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    endDate = serializers.DateField(source='end_date', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    officialWebsiteUrl = serializers.CharField(source='official_website_url', read_only=True)
    shareUrl = serializers.CharField(source='share_url', read_only=True)
    isFeatured = serializers.BooleanField(source='is_featured', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Initiative
        fields = ['id', 'slug', 'title', 'titleAr', 'subtitle', 'subtitleAr', 'category', 'emirates',
                  'startDate', 'endDate', 'coverImage', 'badge', 'officialWebsiteUrl', 'shareUrl',
                  'isFeatured', 'status']


class InitiativeDetailSerializer(InitiativeListSerializer):
    supportOffered = serializers.SerializerMethodField()
    basicInformation = serializers.JSONField(source='basic_information', read_only=True)
    showAbout = serializers.BooleanField(source='show_about', read_only=True)
    showSupportOffered = serializers.BooleanField(source='show_support_offered', read_only=True)
    showBenefits = serializers.BooleanField(source='show_benefits', read_only=True)
    showApplicationForm = serializers.BooleanField(source='show_application_form', read_only=True)

    class Meta:
        model = Initiative
        fields = InitiativeListSerializer.Meta.fields + [
            'description', 'purpose', 'objectives', 'basicInformation', 'supportOffered',
            'benefits', 'contact', 'showAbout', 'showSupportOffered', 'showBenefits',
            'showApplicationForm',
        ]

    def get_supportOffered(self, obj):
        return obj.support_offered


class InitiativeLightSerializer(serializers.ModelSerializer):
    """Lightweight initiative used under an emirate."""

    id = serializers.UUIDField(source='pk', read_only=True)
    coverImage = serializers.CharField(source='cover_image', read_only=True)
    officialWebsiteUrl = serializers.CharField(source='official_website_url', read_only=True)
    shareUrl = serializers.CharField(source='share_url', read_only=True)

    class Meta:
        model = Initiative
        fields = ['id', 'slug', 'title', 'subtitle', 'badge', 'coverImage',
                  'officialWebsiteUrl', 'shareUrl']


class ConsultationListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    sessionTitle = serializers.CharField(source='session_title', read_only=True)
    sessionType = serializers.CharField(source='session_type', read_only=True)
    maritalStage = serializers.CharField(source='marital_stage', read_only=True)
    startTime = serializers.CharField(source='start_time', read_only=True)
    endTime = serializers.CharField(source='end_time', read_only=True)
    isFree = serializers.BooleanField(source='is_free', read_only=True)
    seatsLeft = serializers.SerializerMethodField()
    coverImage = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'slug', 'sessionTitle', 'category', 'sessionType', 'emirates',
                  'maritalStage', 'language', 'date', 'startTime', 'endTime', 'duration', 'isFree',
                  'fee', 'seatsLeft', 'coverImage', 'status']

    def get_seatsLeft(self, obj):
        return obj.seats_left

    def get_coverImage(self, obj):
        gallery = obj.gallery or []
        return gallery[0] if gallery else ''


class ConsultationDetailSerializer(ConsultationListSerializer):
    sessionTitleAr = serializers.CharField(source='session_title_ar', read_only=True)
    publishedDate = serializers.DateField(source='published_date', read_only=True)
    timeZone = serializers.CharField(source='time_zone', read_only=True)
    meetingFormat = serializers.CharField(source='meeting_format', read_only=True)
    sessionLink = serializers.CharField(source='session_link', read_only=True)
    maxParticipants = serializers.IntegerField(source='max_participants', read_only=True)
    processingFee = serializers.DecimalField(source='processing_fee', max_digits=10, decimal_places=2, read_only=True)
    counselorPhoto = serializers.CharField(source='counselor_photo', read_only=True)
    counselorTitle = serializers.CharField(source='counselor_title', read_only=True)
    counselorBio = serializers.CharField(source='counselor_bio', read_only=True)
    learnMore = serializers.JSONField(source='learn_more', read_only=True)
    whatYouWillLearn = serializers.JSONField(source='what_you_will_learn', read_only=True)
    whoShouldAttend = serializers.JSONField(source='who_should_attend', read_only=True)
    bookingNotice = serializers.CharField(source='booking_notice', read_only=True)
    showDoctor = serializers.BooleanField(source='show_doctor', read_only=True)
    showLearnMore = serializers.BooleanField(source='show_learn_more', read_only=True)
    showGallery = serializers.BooleanField(source='show_gallery', read_only=True)
    showSchedule = serializers.BooleanField(source='show_schedule', read_only=True)
    showBooking = serializers.BooleanField(source='show_booking', read_only=True)
    isBookable = serializers.BooleanField(source='is_bookable', read_only=True)

    class Meta:
        model = Consultation
        fields = ConsultationListSerializer.Meta.fields + [
            'sessionTitleAr', 'publishedDate', 'timeZone', 'meetingFormat', 'sessionLink',
            'maxParticipants', 'processingFee', 'discount', 'counselor', 'counselorPhoto',
            'counselorTitle', 'counselorBio', 'learnMore', 'gallery', 'description', 'objectives',
            'whatYouWillLearn', 'whoShouldAttend', 'schedule', 'bookingNotice', 'showDoctor',
            'showLearnMore', 'showGallery', 'showSchedule', 'showBooking', 'isBookable',
        ]


class EmirateListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    emiratesName = serializers.CharField(source='emirates_name', read_only=True)
    centerCount = serializers.CharField(source='center_count', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Emirate
        fields = ['id', 'slug', 'emiratesName', 'title', 'description', 'centerCount', 'image', 'status']


class EmirateDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    emiratesName = serializers.CharField(source='emirates_name', read_only=True)
    emiratesNameAr = serializers.CharField(source='emirates_name_ar', read_only=True)
    dateTime = serializers.DateTimeField(source='date_time', read_only=True)
    contactPhone = serializers.CharField(source='contact_phone', read_only=True)
    serviceCenters = serializers.IntegerField(source='service_centers', read_only=True)
    centerCount = serializers.CharField(source='center_count', read_only=True)
    websiteUrl = serializers.CharField(source='website_url', read_only=True)
    showStatus = serializers.BooleanField(source='show_status', read_only=True)
    status = serializers.CharField(read_only=True)
    initiatives = serializers.SerializerMethodField()

    class Meta:
        model = Emirate
        fields = ['id', 'slug', 'emiratesName', 'emiratesNameAr', 'title', 'description', 'dateTime',
                  'contactPhone', 'serviceCenters', 'centerCount', 'image', 'websiteUrl', 'showStatus',
                  'status', 'initiatives']

    def get_initiatives(self, obj):
        qs = Initiative.objects.filter(
            Q(emirates=obj.emirates_name) | Q(emirates=obj.slug),
            status='Published',
        )
        return InitiativeLightSerializer(qs, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    category = serializers.CharField(source='name', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category', 'description', 'date', 'status']


class PagePresentationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    titleAr = serializers.CharField(source='title_ar', read_only=True)
    descriptionAr = serializers.CharField(source='description_ar', read_only=True)
    heroImage = serializers.CharField(source='hero_image', read_only=True)

    class Meta:
        model = PagePresentation
        fields = ['id', 'key', 'title', 'titleAr', 'description', 'descriptionAr', 'badge', 'heroImage']


class HomepageContentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)

    # Hero
    heroEyebrow = serializers.CharField(source='hero_eyebrow', read_only=True)
    heroEyebrowAr = serializers.CharField(source='hero_eyebrow_ar', read_only=True)
    heroTitle = serializers.CharField(source='hero_title', read_only=True)
    heroTitleAr = serializers.CharField(source='hero_title_ar', read_only=True)
    heroSubtitle = serializers.CharField(source='hero_subtitle', read_only=True)
    heroSubtitleAr = serializers.CharField(source='hero_subtitle_ar', read_only=True)
    heroSearchPlaceholder = serializers.CharField(source='hero_search_placeholder', read_only=True)
    heroSearchPlaceholderAr = serializers.CharField(source='hero_search_placeholder_ar', read_only=True)
    heroSearchButton = serializers.CharField(source='hero_search_button', read_only=True)
    heroSearchButtonAr = serializers.CharField(source='hero_search_button_ar', read_only=True)
    heroPrimaryCtaLabel = serializers.CharField(source='hero_primary_cta_label', read_only=True)
    heroPrimaryCtaLabelAr = serializers.CharField(source='hero_primary_cta_label_ar', read_only=True)
    heroPrimaryCtaLink = serializers.CharField(source='hero_primary_cta_link', read_only=True)
    heroSecondaryCtaLabel = serializers.CharField(source='hero_secondary_cta_label', read_only=True)
    heroSecondaryCtaLabelAr = serializers.CharField(source='hero_secondary_cta_label_ar', read_only=True)
    heroSecondaryCtaLink = serializers.CharField(source='hero_secondary_cta_link', read_only=True)
    heroImage = serializers.CharField(source='hero_image', read_only=True)
    heroImageAlt = serializers.CharField(source='hero_image_alt', read_only=True)
    heroFloatingCards = serializers.JSONField(source='hero_floating_cards', read_only=True)

    # Stats
    stats = serializers.JSONField(read_only=True)

    # Shorts
    shortsTitle = serializers.CharField(source='shorts_title', read_only=True)
    shortsTitleAr = serializers.CharField(source='shorts_title_ar', read_only=True)
    shortsSubtitle = serializers.CharField(source='shorts_subtitle', read_only=True)
    shortsSubtitleAr = serializers.CharField(source='shorts_subtitle_ar', read_only=True)
    shortsCtaLabel = serializers.CharField(source='shorts_cta_label', read_only=True)
    shortsCtaLabelAr = serializers.CharField(source='shorts_cta_label_ar', read_only=True)
    shortsEmptyText = serializers.CharField(source='shorts_empty_text', read_only=True)
    shortsEmptyTextAr = serializers.CharField(source='shorts_empty_text_ar', read_only=True)

    # News
    newsTitle = serializers.CharField(source='news_title', read_only=True)
    newsTitleAr = serializers.CharField(source='news_title_ar', read_only=True)
    newsSubtitle = serializers.CharField(source='news_subtitle', read_only=True)
    newsSubtitleAr = serializers.CharField(source='news_subtitle_ar', read_only=True)
    newsCtaLabel = serializers.CharField(source='news_cta_label', read_only=True)
    newsCtaLabelAr = serializers.CharField(source='news_cta_label_ar', read_only=True)

    # Initiatives
    initiativesTitle = serializers.CharField(source='initiatives_title', read_only=True)
    initiativesTitleAr = serializers.CharField(source='initiatives_title_ar', read_only=True)
    initiativesSubtitle = serializers.CharField(source='initiatives_subtitle', read_only=True)
    initiativesSubtitleAr = serializers.CharField(source='initiatives_subtitle_ar', read_only=True)
    initiativesCtaLabel = serializers.CharField(source='initiatives_cta_label', read_only=True)
    initiativesCtaLabelAr = serializers.CharField(source='initiatives_cta_label_ar', read_only=True)

    # Consultations
    consultationsTitle = serializers.CharField(source='consultations_title', read_only=True)
    consultationsTitleAr = serializers.CharField(source='consultations_title_ar', read_only=True)
    consultationsSubtitle = serializers.CharField(source='consultations_subtitle', read_only=True)
    consultationsSubtitleAr = serializers.CharField(source='consultations_subtitle_ar', read_only=True)
    consultationsCtaLabel = serializers.CharField(source='consultations_cta_label', read_only=True)
    consultationsCtaLabelAr = serializers.CharField(source='consultations_cta_label_ar', read_only=True)
    consultationsFreeTab = serializers.CharField(source='consultations_free_tab', read_only=True)
    consultationsFreeTabAr = serializers.CharField(source='consultations_free_tab_ar', read_only=True)
    consultationsPaidTab = serializers.CharField(source='consultations_paid_tab', read_only=True)
    consultationsPaidTabAr = serializers.CharField(source='consultations_paid_tab_ar', read_only=True)

    # Emirates
    emiratesTitle = serializers.CharField(source='emirates_title', read_only=True)
    emiratesTitleAr = serializers.CharField(source='emirates_title_ar', read_only=True)
    emiratesSubtitle = serializers.CharField(source='emirates_subtitle', read_only=True)
    emiratesSubtitleAr = serializers.CharField(source='emirates_subtitle_ar', read_only=True)
    emiratesCapitalLabel = serializers.CharField(source='emirates_capital_label', read_only=True)
    emiratesCapitalLabelAr = serializers.CharField(source='emirates_capital_label_ar', read_only=True)
    emiratesHeadquartersLabel = serializers.CharField(source='emirates_headquarters_label', read_only=True)
    emiratesHeadquartersLabelAr = serializers.CharField(source='emirates_headquarters_label_ar', read_only=True)
    emiratesCtaLabel = serializers.CharField(source='emirates_cta_label', read_only=True)
    emiratesCtaLabelAr = serializers.CharField(source='emirates_cta_label_ar', read_only=True)

    # CTA
    ctaTitle = serializers.CharField(source='cta_title', read_only=True)
    ctaTitleAr = serializers.CharField(source='cta_title_ar', read_only=True)
    ctaSubtitle = serializers.CharField(source='cta_subtitle', read_only=True)
    ctaSubtitleAr = serializers.CharField(source='cta_subtitle_ar', read_only=True)
    ctaPrimaryLabel = serializers.CharField(source='cta_primary_label', read_only=True)
    ctaPrimaryLabelAr = serializers.CharField(source='cta_primary_label_ar', read_only=True)
    ctaPrimaryLink = serializers.CharField(source='cta_primary_link', read_only=True)
    ctaSecondaryLabel = serializers.CharField(source='cta_secondary_label', read_only=True)
    ctaSecondaryLabelAr = serializers.CharField(source='cta_secondary_label_ar', read_only=True)
    ctaSecondaryLink = serializers.CharField(source='cta_secondary_link', read_only=True)

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
                  'ctaSecondaryLabel', 'ctaSecondaryLabelAr', 'ctaSecondaryLink']