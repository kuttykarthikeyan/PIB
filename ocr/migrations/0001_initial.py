# Generated by Django 4.2.5 on 2023-12-15 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyOCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('json_result', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('ocr_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='ocr.dailyocr')),
            ],
        ),
        migrations.CreateModel(
            name='OCRResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('file', models.FileField(upload_to='ocr/')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='ocr.page')),
            ],
        ),
    ]