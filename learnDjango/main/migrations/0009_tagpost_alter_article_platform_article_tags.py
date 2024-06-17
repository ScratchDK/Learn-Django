# Generated by Django 4.2.11 on 2024-05-22 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_article_cat_alter_platform_cat'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='main.platform'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='main.tagpost'),
        ),
    ]