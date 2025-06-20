# Generated by Django 3.2.14 on 2025-06-14 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('PROCESSING', 'En cours'), ('COMPLETED', 'Terminé'), ('FAILED', 'Échoué')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True)),
                ('retry_count', models.IntegerField(default=0)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='IndexingStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('total_documents', models.IntegerField(default=0)),
                ('indexed_documents', models.IntegerField(default=0)),
                ('failed_documents', models.IntegerField(default=0)),
                ('processing_time_avg', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('date',)},
            },
        ),
        migrations.CreateModel(
            name='IndexingJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(choices=[('OCR', 'OCR'), ('THUMBNAIL', 'Miniature'), ('METADATA', 'Métadonnées'), ('FULL_TEXT', 'Texte intégral')], max_length=20)),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('PROCESSING', 'En cours'), ('COMPLETED', 'Terminé'), ('FAILED', 'Échoué')], default='PENDING', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('result_data', models.JSONField(blank=True, default=dict)),
                ('error_message', models.TextField(blank=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
            options={
                'unique_together': {('document', 'job_type')},
            },
        ),
    ]
