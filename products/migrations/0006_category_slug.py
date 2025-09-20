from django.db import migrations, models
from django.utils.text import slugify

def backfill_slugs(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    existing = set(
        s for s, in Category.objects.exclude(slug__isnull=True).exclude(slug='').values_list('slug', flat=False)
    )
    for cat in Category.objects.all().order_by('id'):
        base = slugify(cat.friendly_name or cat.name or f"category-{cat.id}")[:60] or f"category-{cat.id}"
        slug = base
        i = 2
        while slug in existing:
            suffix = f"-{i}"
            slug = (base[: (60 - len(suffix))] + suffix)
            i += 1
        cat.slug = slug
        cat.save(update_fields=['slug'])
        existing.add(slug)

class Migration(migrations.Migration):

    dependencies = [
            ('products', '0005_alter_product_image')
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=60, unique=True, null=True, blank=True),
        ),
        migrations.RunPython(backfill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=60, unique=True),
        ),
    ]
