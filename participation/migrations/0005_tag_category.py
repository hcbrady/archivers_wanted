# Generated by Django 5.2.3 on 2025-07-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participation', '0004_remove_tagsubscription_tag_tagsubscription_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.CharField(choices=[('project', 'Project'), ('skill', 'Skill'), ('interest', 'Interest')], default='interest', max_length=20),
        ),
    ]
