from pathlib import Path
from django.core.management.base import BaseCommand
from django.core import serializers

from api.models import (
    CustomMonthlyExport,
    CustomMonthlyImport,
    CustomMonthlyImportCustom,
    CustomMonthlyImportSum,
    CustomMonthlyRaw,
    ExportDaily,
)


class Command(BaseCommand):
    help = "Export customs-related models to api/fixtures/initial_customs.json"

    def handle(self, *args, **options):
        # 1) Collect objects
        objects = (
            list(CustomMonthlyExport.objects.all()) +
            list(CustomMonthlyImport.objects.all()) +
            list(CustomMonthlyImportCustom.objects.all()) +
            list(CustomMonthlyImportSum.objects.all()) +
            list(CustomMonthlyRaw.objects.all()) +
            list(ExportDaily.objects.all())
        )

        # 2) Serialize to JSON string
        data = serializers.serialize(
            "json",
            objects,
            indent=2,
        )

        # 3) Write file as UTF-8
        fixtures_dir = Path("api") / "fixtures"
        fixtures_dir.mkdir(exist_ok=True)

        out_file = fixtures_dir / "initial_customs.json"
        out_file.write_text(data, encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(
            f"Exported {len(objects)} records → {out_file}"
        ))