# Generated by Django 4.1.7 on 2023-03-09 21:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('url', models.URLField(blank=True, help_text='URL of official licence text.', null=True, unique=True, verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True, help_text='E.g. usage information, URLs')),
                ('media', models.CharField(choices=[('WEB', 'Web'), ('PRT', 'Print')], max_length=3)),
            ],
            options={
                'verbose_name': 'Usage tag',
                'verbose_name_plural': 'Usage tags',
            },
        ),
        migrations.CreateModel(
            name='UsageRestriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.EmailField(blank=True, max_length=254)),
                ('updated_by', models.EmailField(blank=True, max_length=254)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('file', models.FileField(upload_to='assets/')),
                ('description', models.TextField(blank=True)),
                ('copyright_statement', models.CharField(blank=True, help_text='Appropriate credit/Licence holder (if required by license)', max_length=255)),
                ('licence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.licence')),
                ('usage', models.ManyToManyField(blank=True, to='core.usage', verbose_name='Usage tag')),
                ('usage_restriction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.usagerestriction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]