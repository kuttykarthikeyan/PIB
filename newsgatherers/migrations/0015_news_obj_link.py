# Generated by Django 4.2.5 on 2023-12-11 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsgatherers', '0014_news_obj_delete_news_delete_news_cluster_obj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news_obj',
            name='link',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]