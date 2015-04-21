# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0003_auto_20150421_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.TextField(default='report'),
        ),
    ]
