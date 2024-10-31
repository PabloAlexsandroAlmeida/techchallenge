# Generated by Django 5.1.1 on 2024-10-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vitivinicultura", "0003_remove_exportacao_ano_producao_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comercio",
            name="pais",
            field=models.CharField(default="desconhecido", max_length=100),
        ),
        migrations.AddField(
            model_name="exportacao",
            name="pais",
            field=models.CharField(default="desconhecido", max_length=100),
        ),
        migrations.AddField(
            model_name="importacao",
            name="pais",
            field=models.CharField(default="desconhecido", max_length=100),
        ),
        migrations.AddField(
            model_name="processamento",
            name="pais",
            field=models.CharField(default="desconhecido", max_length=100),
        ),
        migrations.AddField(
            model_name="producao",
            name="pais",
            field=models.CharField(default="desconhecido", max_length=100),
        ),
    ]