# products/management/commands/push_images_to_cloudinary.py
"""
Usage:
  python manage.py push_images_to_cloudinary [--folder FOLDER] [--dry-run] [--limit N]

Scans your DB for Products that have a local image file (in ./media or MEDIA_ROOT),
uploads each to Cloudinary, and updates Product.image to the new Cloudinary public ID
(so templates can render {{ product.image.url }} on Heroku).

Safe to re-run; uses use_filename+overwrite so you don't get duplicates.
"""

import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from products.models import Product

try:
    import cloudinary
    from cloudinary.uploader import upload as cl_upload
except Exception as exc:  # pragma: no cover
    cloudinary = None
    cl_upload = None


def _guess_local_path(name: str) -> Path | None:
    """
    Try a few common places for the local file.
    """
    if not name:
        return None
    candidates = [
        Path(settings.BASE_DIR) / 'media' / name,
        Path('media') / name,
        Path(settings.BASE_DIR) / name,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


class Command(BaseCommand):
    help = "Upload local product images to Cloudinary and update Product.image names."

    def add_arguments(self, parser):
        parser.add_argument('--folder', default='cake-it-easy/products',
                            help="Cloudinary folder to place images (default: cake-it-easy/products)")
        parser.add_argument('--dry-run', action='store_true', help="Print what would happen without uploading.")
        parser.add_argument('--limit', type=int, default=0, help="Limit number of products processed.")

    @transaction.atomic
    def handle(self, *args, **opts):
        if cloudinary is None or cl_upload is None:
            self.stderr.write(self.style.ERROR("Cloudinary library not available. "
                                               "Install and configure CLOUDINARY_* env vars."))
            return

        # Ensure cloudinary is configured from env
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        )
        if not cloudinary.config().cloud_name:
            self.stderr.write(self.style.ERROR("Cloudinary not configured. "
                                               "Set CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET."))
            return

        folder = opts['folder'].strip('/')
        dry = opts['dry_run']
        limit = opts['limit']

        qs = Product.objects.all().order_by('id')
        count = 0
        uploaded = 0
        skipped = 0

        for product in qs:
            if limit and uploaded >= limit:
                break

            name = str(product.image.name or '').lstrip('/')
            local_path = _guess_local_path(name)

            if not local_path:
                # No local file found; skip (already on Cloudinary or blank)
                skipped += 1
                self.stdout.write(f"SKIP #{product.id} {product.name}: no local file for '{name}'")
                continue

            public_id_base = local_path.stem  # filename without extension
            public_id = f"{folder}/{public_id_base}"

            self.stdout.write(f"{'DRY ' if dry else ''}UPLOAD #{product.id} {product.name}: {local_path} -> {public_id}")

            if dry:
                continue

            # Upload the local file; use_filename keeps the original name; overwrite avoids duplicates
            res = cl_upload(
                str(local_path),
                folder=folder,
                use_filename=True,
                unique_filename=False,
                overwrite=True,
                resource_type='image',
            )
            # Cloudinary returns e.g. public_id='cake-it-easy/products/myfile', format='jpg'
            new_name = f"{res['public_id']}.{res['format']}"
            # Assigning the name is enough; CloudinaryStorage will build the URL from it
            product.image.name = new_name
            product.save(update_fields=['image'])
            uploaded += 1
            count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Uploaded: {uploaded}, Skipped: {skipped}, Total considered: {qs.count()}"
        ))
