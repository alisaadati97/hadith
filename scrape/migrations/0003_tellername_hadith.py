# Generated by Django 3.1.3 on 2021-07-10 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0002_tellername'),
    ]

    operations = [
        migrations.AddField(
            model_name='tellername',
            name='hadith',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scrape.hadith'),
        ),
    ]
