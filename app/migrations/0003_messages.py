# Generated by Django 5.0.7 on 2024-09-20 15:51

import django.db.models.deletion
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_alter_chats_options_alter_chatsmembers_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Messages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True, null=True)),
                ("img_url", models.URLField(blank=True, null=True)),
                (
                    "youtube_video_id",
                    models.CharField(blank=True, max_length=11, null=True),
                ),
                ("file_url", models.URLField(blank=True, null=True)),
                (
                    "mixcloud_key",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'chat',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='app.chats'
                    )
                )
            ],
            options={
                "verbose_name_plural": "messages",
            },
        ),
    ]
