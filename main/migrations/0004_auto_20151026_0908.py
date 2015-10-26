# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151026_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'IPR', max_length=3, choices=[(b'IPR', b'Execution in progress'), (b'RTE', b'Runtime Error'), (b'TMO', b'Timed out'), (b'WA', b'Wrong Answer'), (b'AC', b'Correct Answer')]),
        ),
    ]
