# Generated by Django 3.1.3 on 2021-08-16 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0006_auto_20210816_0659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hadithexplanationreference',
            name='hadith',
        ),
        migrations.AddField(
            model_name='hadithexplanationreference',
            name='hadithexplain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scrape.hadithexplanation'),
        ),
    ]
