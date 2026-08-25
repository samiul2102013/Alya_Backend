from django.db import models


class Status(models.TextChoices):
    PUBLISHED = 'Published', 'Published'
    DRAFT = 'Draft', 'Draft'
    REVIEW = 'Pending', 'Pending'


class Language(models.TextChoices):
    ENGLISH = 'en', 'English'
    ARABIC = 'ar', 'Arabic'
    BOTH = 'both', 'Both'


class Emirates(models.TextChoices):
    ABU_DHABI = 'abudhabi', 'Abu Dhabi'
    DUBAI = 'dubai', 'Dubai'
    SHARJAH = 'sharjah', 'Sharjah'
    AJMAN = 'ajman', 'Ajman'
    RAS_AL_KHAIMAH = 'rasalkhaimah', 'Ras Al Khaimah'
    FUJAIRAH = 'fujairah', 'Fujairah'
    UMM_AL_QUWAIN = 'ummAlquwain', 'Umm Al-Quwain'


class MaritalStage(models.TextChoices):
    PREMARITAL = 'premarital', 'Premarital'
    MARITAL = 'marital', 'Marital'
    POST_MARITAL = 'postMarital', 'Post-marital'


class SessionType(models.TextChoices):
    COUNSELING = 'counseling', 'Counseling'
    FINANCIAL = 'financial', 'Financial'
    LEGAL = 'legal', 'Legal'
    HEALTH = 'health', 'Health'
    WORKSHOP = 'workshop', 'Workshop'


class Source(models.TextChoices):
    GOVERNMENT = 'government', 'Government'
    NGO = 'ngo', 'NGO'
    PRIVATE = 'private', 'Private'


class NewsCategory(models.TextChoices):
    MARRIAGE = 'marriage', 'Marriage'
    FAMILY = 'family', 'Family'
    COUNSELING = 'counseling', 'Counseling'
    COMMUNITY = 'community', 'Community'
    POLICY = 'policy', 'Policy'
    EDUCATION = 'education', 'Education'
    SERVICE = 'service', 'Service'
    FINANCE = 'finance', 'Finance'
    HEALTH = 'health', 'Health'
    CULTURE = 'culture', 'Culture'


class ResourceType(models.TextChoices):
    OFFICIAL_WEBSITE = 'official_website', 'Official Website'
    GOVERNMENT_RESOURCE = 'government_resource', 'Government Resource'
    EDUCATIONAL_RESOURCE = 'educational_resource', 'Educational Resource'
    RELATED_INITIATIVE = 'related_initiative', 'Related Initiative'


class SupportProgram(models.TextChoices):
    FINANCIAL_SUPPORT = 'financial_support', 'Financial Support'
    HOUSING_SUPPORT = 'housing_support', 'Housing Support'
    EDUCATIONAL_SUPPORT = 'educational_support', 'Educational Support'
    MARRIAGE_TRAINING_PROGRAM = 'marriage_training_program', 'Marriage Training Program'
    PRE_MARITAL_PREPARATION = 'pre_marital_preparation', 'Pre-Marital Preparation'


class ShortCategory(models.TextChoices):
    """Admin category enum for videos (spec 2.1)."""

    INITIATIVE = 'Initiative', 'Initiative'
    EDUCATION = 'Education', 'Education'
    CULTURE = 'Culture', 'Culture'
    SERVICE = 'Service', 'Service'
    FINANCE = 'Finance', 'Finance'
    HEALTH = 'Health', 'Health'


class PaymentMethod(models.TextChoices):
    CARD = 'card', 'Card'
    APPLE_PAY = 'apple_pay', 'Apple Pay'


class BookingStatus(models.TextChoices):
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    PENDING_PAYMENT = 'pending_payment', 'Pending Payment'


class ApplicationStatus(models.TextChoices):
    RECEIVED = 'received', 'Received'
    REVIEWING = 'reviewing', 'Reviewing'
    SHORTLISTED = 'shortlisted', 'Shortlisted'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'


class UserType(models.TextChoices):
    INDIVIDUAL = 'individual', 'Individual'
    COUPLE = 'couple', 'Couple'
    ORGANIZATION = 'organization', 'Organization'