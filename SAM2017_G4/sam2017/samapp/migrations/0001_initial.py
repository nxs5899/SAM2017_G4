# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 19:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadlineType', models.CharField(choices=[('paperSubmission', 'paperSubmission'), ('paperSelection', 'paperSelection'), ('paperAssign', 'paperAssign'), ('paperReview', 'paperReview'), ('paperRate', 'paperRate')], max_length=500)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('message', models.CharField(max_length=500)),
                ('viewed', models.BooleanField(default=False, verbose_name='Viewd?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipient', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('paperSubmitted', 'paperSubmitted'), ('selectpaper', 'selectpaper'), ('assigntoReview', 'assigntoReview'), ('startReview', 'startReview'), ('reviewComplete', 'reviewComplete'), ('paperRate', 'paperRate')], max_length=500)),
                ('message', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitter', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('version', models.FloatField()),
                ('formats', models.CharField(choices=[('PDF', 'PDF'), ('Word', 'Word')], max_length=5)),
                ('document', models.FileField(upload_to='')),
                ('rate', models.FloatField(default=None, null=True)),
                ('sub_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned', models.NullBooleanField(default=False)),
                ('contact_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samapp.Author')),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='PCC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PCM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(null=True)),
                ('comments', models.TextField()),
                ('submissiondate', models.DateTimeField(auto_now_add=True)),
                ('submissionDeadline', models.DateTimeField(auto_now_add=True)),
                ('paperId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samapp.Paper')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samapp.PCM')),
            ],
        ),
        migrations.CreateModel(
            name='Samadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PCM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samapp.PCM')),
                ('selected_papers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samapp.Paper')),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pcm1', to='samapp.PCM'),
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pcm2', to='samapp.PCM'),
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pcm3', to='samapp.PCM'),
        ),
    ]
