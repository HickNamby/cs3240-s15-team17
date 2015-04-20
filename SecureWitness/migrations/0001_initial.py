# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('docfile', models.FileField(upload_to='documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('ofolder', models.ManyToManyField(to='SecureWitness.Folder', related_name='ofolder_rel_+')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('short_des', models.CharField(max_length=50)),
                ('long_des', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('incident_date', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('public', models.BooleanField(default=True)),
                ('folder', models.ManyToManyField(to='SecureWitness.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('email', models.EmailField(unique=True, max_length=225)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin_user', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False),
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False),
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(to='SecureWitness.Report'),
        ),
    ]
