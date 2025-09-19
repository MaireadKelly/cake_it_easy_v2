# products/management/commands/generate_image_map.py
"""
Build a CSV mapping (sku,filename) for products missing image files.

Scans one or more media roots for common image extensions and tries to match by
SKU and by a slug of the product name. It writes a CSV you can edit and then
pass to `push_images_to_cloudinary --mapping <file.csv>`.

Usage:
  python manage.py generate_image_map --out products_image_map.csv --media-root <PATH> [--media-root <PATH2>]
"""
import csv
from pathlib import Path
from typing import Dict, List, Tuple

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from products.models import Product

IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def find_media_files(roots: List[Path]) -> List[Path]:
    files = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMG_EXTS:
                files.append(p.resolve())
    return files

def score_match(stem: str, sku: str, name_slug: str) -> int:
    """Simple scoring: exact > contains > partial."""
    s = stem.lower()
    best = 0
    if sku:
        sk = sku.lower()
        if s == sk:
            best = max(best, 100)
        elif sk in s:
            best = max(best, 60)
    if name_slug:
        ns = name_slug.lower()
        if s == ns:
            best = max(best, 90)
        elif ns.replace("-", "_") == s or ns.replace("-", "") == s:
            best = max(best, 85)
        elif ns in s:
            best = max(best, 55)
    return best

class Command(BaseCommand):
    help = "Generate a CSV mapping sku -> filename by scanning media roots and heuristically matching."

    def add_arguments(self, parser):
        parser.add_argument("--out", default="products_image_map.csv", help="Output CSV path")
        parser.add_argument(
            "--media-root",
            action="append",
            default=[],
            help="One or more media root directories to scan. "
                 "If omitted, uses settings.MEDIA_ROOT and ./media",
        )

    def handle(self, *args, **opts):
        out_path = Path(opts["out"])

        # Build list of roots
        roots = [Path(r) for r in opts["media_root"]] or []
        default_media = getattr(settings, "MEDIA_ROOT", None)
        if default_media:
            roots.append(Path(default_media))
        roots.append(Path("media"))

        # uniquify + only existing
        uniq_roots: List[Path] = []
        seen = set()
        for r in roots:
            rp = r.resolve()
            if rp not in seen and rp.exists():
                seen.add(rp)
                uniq_roots.append(rp)
        if not uniq_roots:
            self.stderr.write(self.style.ERROR("No media roots found. Use --media-root to point at your images."))
            return

        self.stdout.write(f"Scanning media roots: {', '.join(str(r) for r in uniq_roots)}")
        files = find_media_files(uniq_roots)
        self.stdout.write(f"Found {len(files)} image files.")

        # index by stem
        candidates: Dict[str, List[Path]] = {}
        for f in files:
            candidates.setdefault(f.stem.lower(), []).append(f)

        # helper: relative path for CSV (relative to first matching root)
        def relpath(p: Path) -> str:
            for root in uniq_roots:
                try:
                    return str(p.relative_to(root)).replace("\\", "/")
                except Exception:
                    continue
            return str(p).replace("\\", "/")

        rows: List[Tuple[str, str, str]] = []  # sku, filename, note

        for prod in Product.objects.all().order_by("id"):
            sku = (prod.sku or "").strip()
            name_slug = slugify(prod.name or "")
            existing = (str(prod.image.name) or "").strip()

            if existing:
                rows.append((sku, existing, "already-set"))
                continue

            # Try exact stem by sku/name first
            stems = set()
            if sku:
                stems.add(sku.lower())
            if name_slug:
                stems.update({name_slug, name_slug.replace("-", "_"), name_slug.replace("-", "")})

            best_file = None
            best_score = 0

            for stem in stems:
                if stem in candidates:
                    best_file = candidates[stem][0]
                    best_score = 100 if stem == (sku or "").lower() else 90
                    break

            if not best_file:
                # heuristic scan
                for fstem, plist in candidates.items():
                    sc = score_match(fstem, sku, name_slug)
                    if sc > best_score:
                        best_file = plist[0]
                        best_score = sc

            if best_file and best_score >= 55:
                rows.append((sku, relpath(best_file), f"suggested:{best_score}"))
            else:
                rows.append((sku, "", "no-suggestion"))

        # write CSV
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["sku", "filename", "note"])
            for sku, fn, note in rows:
                w.writerow([sku, fn, note])

        self.stdout.write(self.style.SUCCESS(f"Wrote mapping CSV: {out_path}"))
        self.stdout.write("Edit blank/incorrect 'filename' cells, then run:")
        self.stdout.write("  python manage.py push_images_to_cloudinary --mapping products_image_map.csv")
