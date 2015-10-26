# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'IPR', max_length=3, choices=[(b'IPR', b'Execution in progress'), (b'RTE', b'Runtime Error'), (b'TMO', b'Timed out'), (b'WA', b'Wrong Answer')])),
                ('program', models.TextField()),
                ('plang', models.CharField(default=b'PYT', max_length=3, choices=[(b'PYT', b'Python'), (b'CPP', b'C++'), (b'JAV', b'Java')])),
            ],
        ),
    ]
