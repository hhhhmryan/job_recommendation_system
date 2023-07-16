# Generated by Django 4.2.1 on 2023-05-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_resume_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="skills",
            field=models.CharField(
                choices=[
                    ("1", "Python"),
                    ("2", "CPP"),
                    ("3", "C#"),
                    ("4", "Java"),
                    ("5", "GO"),
                    ("6", "Ruby"),
                ],
                default="CPP",
                max_length=255,
            ),
        ),
    ]