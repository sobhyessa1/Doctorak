# Generated by Django 5.0.6 on 2024-05-23 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_Data', '0002_remove_medical_record_analysis_images_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disease',
            old_name='name',
            new_name='disease_name',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='end_date',
            new_name='recovery_date',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='start_date',
            new_name='treatment_start_date',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='test_images',
        ),
        migrations.AddField(
            model_name='disease',
            name='analysis_images',
            field=models.ImageField(blank=True, upload_to='analysis/%Y/%m/%d/'),
        ),
    ]
