# products/management/commands/push_images_to_cloudinary.py
import csv
import os
from pathlib import Path
from typing import Optional, Dict, List

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify
from products.models import Product

try:
    import cloudinary
    from cloudinary.uploader import upload as cl_upload
except Exception:
    cloudinary = None
    cl_upload = None

IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def _media_candidates(extra_roots: List[str]) -> List[Path]:
    roots = [Path(r) for r in extra_roots if r]
    # defaults
    default_media = getattr(settings, "MEDIA_ROOT", None)
    if default_media:
        roots.append(Path(default_media))
    roots.append(Path("media"))
    # de-dup existing
    out = []
    seen = set()
    for r in roots:
        rp = Path(r).resolve()
        if rp.exists() and rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out

def _find_file_for_product(p: Product, media_roots: List[Path], mapping: Dict[str, str]) -> Optional[Path]:
    sku = (p.sku or "").strip()

    # mapping by SKU first
    if sku:
        key = sku.lower()
        if key in mapping:
            for root in media_roots:
                f = (root / mapping[key].lstrip("/\\")).resolve()
                if f.exists():
                    return f

    # if product.image already set locally, try that path
    name = (str(p.image.name) or "").lstrip("/\\")
    if name:
        for root in media_roots:
            f = (root / name).resolve()
            if f.exists():
                return f

    # guess by SKU or slug(name)
    stems = []
    if sku:
        stems.append(sku.lower())
    nslug = slugify(p.name or "")
    if nslug:
        stems.extend([nslug, nslug.replace("-", "_"), nslug.replace("-", "")])

    folders = ["products", "product", "img/products", "images/products", ""]
    for root in media_roots:
        for folder in folders:
            base = (root / folder) if folder else root
            if not base.exists():
                continue
            for child in base.iterdir():
                if child.is_file() and child.suffix.lower() in IMG_EXTS:
                    low = child.stem.lower()
                    if any(stem and stem in low for stem in stems):
                        return child.resolve()
    return None

class Command(BaseCommand):
    help = "Upload local product images to Cloudinary and update Product.image names."

    def add_arguments(self, parser):
        parser.add_argument('--folder', default='cake-it-easy/products',
                            help="Cloudinary folder (default: cake-it-easy/products)")
        parser.add_argument('--dry-run', action='store_true', help="Print actions without uploading.")
        parser.add_argument('--limit', type=int, default=0, help="Limit number of products to process.")
        parser.add_argument('--mapping', type=str, default='',
                            help="Optional CSV with columns: sku,filename (relative to media root)")
        parser.add_argument('--media-root', action='append', default=[],
                            help="Additional media root(s) to scan (e.g., C:/Users/you/project/media)")

    @transaction.atomic
    def handle(self, *args, **opts):
        if cloudinary is None or cl_upload is None:
            self.stderr.write(self.style.ERROR("Cloudinary library not available."))
            return

        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        )
        if not cloudinary.config().cloud_name:
            self.stderr.write(self.style.ERROR("Cloudinary not configured (CLOUDINARY_* missing)."))
            return

        folder = opts['folder'].strip('/')
        dry = opts['dry_run']
        limit = opts['limit']
        mapping_csv = opts['mapping']
        media_roots = _media_candidates(opts['media_root'])
        if not media_roots:
            self.stderr.write(self.style.ERROR("No media roots found. Use --media-root to point at your images."))
            return

        mapping: Dict[str, str] = {}
        if mapping_csv:
            p = Path(mapping_csv)
            if p.exists():
                with p.open(newline='', encoding='utf-8') as fh:
                    rdr = csv.DictReader(fh)
                    for row in rdr:
                        sku = (row.get('sku') or '').strip().lower()
                        fn = (row.get('filename') or '').strip()
                        if sku and fn:
                            mapping[sku] = fn

        qs = Product.objects.all().order_by('id')
        uploaded = 0
        skipped = 0

        self.stdout.write(f"Scanning media roots: {', '.join(str(r) for r in media_roots)}")

        for product in qs:
            if limit and uploaded >= limit:
                break

            local_file = _find_file_for_product(product, media_roots, mapping)
            if not local_file:
                self.stdout.write(f"SKIP #{product.id} {product.sku or ''} {product.name}: no local image found")
                skipped += 1
                continue

            public_id = f"{folder}/{local_file.stem}"
            self.stdout.write(f"{'DRY ' if dry else ''}UPLOAD #{product.id} {product.sku or ''} {product.name}: "
                              f"{local_file} -> {public_id}")

            if dry:
                continue

            res = cl_upload(
                str(local_file),
                folder=folder,
                use_filename=True,
                unique_filename=False,
                overwrite=True,
                resource_type='image',
            )
            new_name = f"{res['public_id']}.{res['format']}"
            product.image.name = new_name
            product.save(update_fields=['image'])
            uploaded += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Uploaded: {uploaded}, Skipped: {skipped}, Total: {qs.count()}"))
