# Generated by Django 5.2.3 on 2025-06-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_createt_at_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
