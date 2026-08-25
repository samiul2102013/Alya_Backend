from rest_framework import serializers

from .enums import ShortCategory
from .models import Category, Consultation, Emirate, Initiative, NewsArticle, PagePresentation, Short
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
    showAbout = serializers.BooleanField(source='show_about', required=False)
    showSupportOffered = serializers.BooleanField(source='show_support_offered', required=False)
    showBenefits = serializers.BooleanField(source='show_benefits', required=False)
    showApplicationForm = serializers.BooleanField(source='show_application_form', required=False)

    class Meta:
        model = Initiative
        fields = ['id', 'slug', 'title', 'titleAr', 'subtitle', 'subtitleAr', 'category', 'emirates',
                  'description', 'purpose', 'objectives', 'basicInformation', 'supportOffered',
                  'benefits', 'startDate', 'endDate', 'coverImage', 'badge', 'contact',
                  'officialWebsiteUrl', 'shareUrl', 'isFeatured', 'showAbout', 'showSupportOffered',
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

    class Meta:
        model = PagePresentation
        fields = ['id', 'key', 'title', 'titleAr', 'description', 'descriptionAr', 'badge',
                  'heroImage', 'published']
        read_only_fields = ['id', 'key']