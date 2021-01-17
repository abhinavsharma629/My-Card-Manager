# Generated by Django 3.1.4 on 2021-01-17 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('website', models.URLField(blank=True, max_length=1000, null=True)),
                ('logo', models.FileField(blank=True, upload_to='company_logos')),
                ('contact_person_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('contact_person_email', models.EmailField(blank=True, max_length=1000, null=True)),
                ('addresss', models.TextField(blank=True, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=1000, null=True)),
                ('company_type', models.CharField(choices=[('COMPANY', 'COMPANY'), ('CONSULTANT', 'CONSULTANT')], max_length=1000)),
                ('company_status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], max_length=1000)),
                ('is_company_active', models.BooleanField(default=False)),
            ],
        ),
    ]
