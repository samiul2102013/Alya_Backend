from django.utils.text import slugify


def unique_slug(model, value, instance_pk=None):
    slug = slugify(value) or 'item'
    base = slug
    counter = 1
    qs = model.objects.filter(slug=slug)
    if instance_pk:
        qs = qs.exclude(pk=instance_pk)
    while qs.exists():
        slug = f'{base}-{counter}'
        counter += 1
        qs = model.objects.filter(slug=slug)
        if instance_pk:
            qs = qs.exclude(pk=instance_pk)
    return slug