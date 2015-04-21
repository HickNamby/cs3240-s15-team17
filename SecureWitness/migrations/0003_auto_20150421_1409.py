# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0002_auto_20150421_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.TextField(default=''),
        ),
    ]
