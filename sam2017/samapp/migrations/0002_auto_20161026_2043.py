# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-27 00:43
from __future__ import unicode_literals
from django.db import models, migrations
from django.contrib.auth.models import Group
from samapp.models import Paper
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def add_group_permissions(samapp, schemaeditor):
    #admin
    PCC, created = Group.objects.get_or_create(name='PCC')
    if created:
        content_type = ContentType.objects.get_for_model(Paper)
        permission = Permission.objects.create(
            codename='can_read',
            name='Can see paper submissions',
            content_type=content_type,
        )
        PCC.permissions.add(permission)

    PCM, created = Group.objects.get_or_create(name='PCM')
    if created:
        content_type1 = ContentType.objects.get_for_model(Paper)
        permission = Permission.objects.create(
            codename = "can_view",
            name = "Can View Paper Submissions",
            content_type = content_type1,
        )
        PCM.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ('samapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
    ]
