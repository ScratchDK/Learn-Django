# Generated by Django 4.2.11 on 2024-05-14 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_article_cat_platform_article_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.category'),
        ),
    ]