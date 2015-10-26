# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='question_answered',
            field=models.ForeignKey(default=None, to='main.Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='submitter',
            field=models.ForeignKey(default=None, to='main.Participant'),
            preserve_default=False,
        ),
    ]
