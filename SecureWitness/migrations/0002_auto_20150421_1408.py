# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('SecureWitness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='groupviewers',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='report',
            name='keywords',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='userviewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='userviewers'),
        ),
        migrations.AlterField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='owner', editable=False),
        ),
    ]
