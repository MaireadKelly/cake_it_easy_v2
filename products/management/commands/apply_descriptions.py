import json

from django.core.management.base import BaseCommand, CommandError

from products.models import Product


class Command(BaseCommand):
    help = "Update Product.description from a JSON mapping of {name: description}."

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Path to descriptions_patch.json")
        parser.add_argument("--dry-run", action="store_true", help="Show changes without saving")

    def handle(self, *args, **opts):
        path = opts["json_path"]
        dry = opts["dry_run"]
        try:
            with open(path, "r", encoding="utf-8") as f:
                mapping = json.load(f)
        except Exception as e:
            raise CommandError(f"Failed to read JSON: {e}")

        updated = 0
        missing = []
        for name, desc in mapping.items():
            try:
                p = Product.objects.get(name=name)
            except Product.DoesNotExist:
                missing.append(name)
                continue

            if (p.description or "").strip() == desc.strip():
                continue

            self.stdout.write(f"- {name}: {'(dry-run) ' if dry else ''}updating description")
            if not dry:
                p.description = desc
                p.save(update_fields=["description"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated: {updated}"))
        if missing:
            self.stdout.write(self.style.WARNING(f"Missing products: {len(missing)}"))
            for m in missing:
                self.stdout.write(f"  • {m}")
