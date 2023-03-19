# Generated by Django 4.1.7 on 2023-03-19 20:29

import ddam.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_asset_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='file',
            field=models.FileField(upload_to='assets', validators=[ddam.core.validators.validate_fileextension, ddam.core.validators.validate_filetype, ddam.core.validators.validate_filesize]),
        ),
    ]
