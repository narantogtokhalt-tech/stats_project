from django.db import migrations


def load_initial_data(apps, schema_editor):
    from django.core.management import call_command

    CustomMonthlyRaw = apps.get_model("api", "CustomMonthlyRaw")

    # Local DB дээр аль хэдийн өгөгдөл байвал Render дээр биш гэдгийг ашиглаж байна
    if CustomMonthlyRaw.objects.exists():
        return

    call_command("loaddata", "initial_customs")


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]