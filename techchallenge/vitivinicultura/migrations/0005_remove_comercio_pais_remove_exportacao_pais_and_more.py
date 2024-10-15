# Generated by Django 5.1.1 on 2024-10-08 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "vitivinicultura",
            "0004_comercio_pais_exportacao_pais_importacao_pais_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comercio",
            name="pais",
        ),
        migrations.RemoveField(
            model_name="exportacao",
            name="pais",
        ),
        migrations.RemoveField(
            model_name="importacao",
            name="pais",
        ),
        migrations.RemoveField(
            model_name="processamento",
            name="pais",
        ),
        migrations.RemoveField(
            model_name="producao",
            name="pais",
        ),
    ]