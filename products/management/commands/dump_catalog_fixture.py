# products/management/commands/dump_catalog_fixture.py
"""
Dump categories + products to products/fixtures/catalog.json (pretty indented).
Usage:
  python manage.py dump_catalog_fixture
"""
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "Dump categories + products to products/fixtures/catalog.json"

    def handle(self, *args, **kwargs):
        fixtures_dir = Path(settings.BASE_DIR) / 'products' / 'fixtures'
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        out_path = fixtures_dir / 'catalog.json'
        self.stdout.write(f"Writing fixture to {out_path} ...")
        call_command(
            'dumpdata',
            'products.category',
            'products.product',
            indent=2,
            output=str(out_path),
        )
        self.stdout.write(self.style.SUCCESS("Fixture written."))
