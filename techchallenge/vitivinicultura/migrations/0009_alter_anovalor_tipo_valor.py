# Generated by Django 5.1.1 on 2024-10-15 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vitivinicultura", "0008_anovalor_tipo_valor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anovalor",
            name="tipo_valor",
            field=models.CharField(default="valor", max_length=50),
        ),
    ]
