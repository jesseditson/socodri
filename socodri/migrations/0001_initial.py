# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AdsObject',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Funnel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('view_window', models.CharField(max_length=32, null=True)),
                ('view_multiplier', models.FloatField(default=1.0)),
                ('click_window', models.CharField(max_length=32, null=True)),
                ('click_multiplier', models.FloatField(default=1.0)),
                ('action_total_type', models.CharField(default=b'total_actions', max_length=32)),
                ('revenue_source', models.CharField(default=b'Facebook', max_length=32)),
                ('label_fn', models.CharField(max_length=32, null=True)),
                ('adaccount', models.ForeignKey(related_name='funnel', to='socodri.AdsObject')),
                ('campaigns', models.ManyToManyField(related_name='funnels', to='socodri.AdsObject')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=32)),
                ('text', models.CharField(max_length=255)),
                ('object_type', models.CharField(max_length=32)),
                ('object_id', models.CharField(max_length=32)),
                ('platform', models.CharField(max_length=32)),
                ('funnel', models.ForeignKey(to='socodri.Funnel')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('number', models.PositiveIntegerField()),
                ('actions', models.ManyToManyField(to='socodri.Action')),
                ('funnel', models.ForeignKey(to='socodri.Funnel')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='pixel',
            field=models.ForeignKey(to='socodri.AdsObject'),
        ),
    ]
