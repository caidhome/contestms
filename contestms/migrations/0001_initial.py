# Generated by Django 3.1.5 on 2021-01-20 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certms', '0001_initial'),
        ('userms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('con_id', models.AutoField(primary_key=True, serialize=False)),
                ('con_name', models.CharField(max_length=255)),
                ('con_time', models.DateTimeField()),
                ('con_signtime', models.DateTimeField()),
                ('con_endtime', models.DateTimeField()),
                ('con_place', models.CharField(max_length=255)),
                ('con_rule', models.CharField(max_length=255)),
                ('con_environ', models.CharField(blank=True, max_length=255, null=True)),
                ('con_lang', models.CharField(blank=True, max_length=255, null=True)),
                ('con_level', models.IntegerField()),
                ('con_signlink', models.CharField(blank=True, max_length=255, null=True)),
                ('con_certid', models.ForeignKey(db_column='con_certid', on_delete=django.db.models.deletion.DO_NOTHING, to='certms.cert')),
                ('con_createrid', models.ForeignKey(db_column='con_createrid', on_delete=django.db.models.deletion.DO_NOTHING, to='userms.admin')),
            ],
            options={
                'db_table': 'tt_contest',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('sign_id', models.IntegerField(primary_key=True, serialize=False)),
                ('sign_lang', models.CharField(blank=True, max_length=255, null=True)),
                ('sign_state', models.IntegerField()),
                ('sign_certpath', models.CharField(blank=True, max_length=255, null=True)),
                ('sign_total', models.IntegerField(blank=True, null=True)),
                ('sign_detial', models.CharField(blank=True, max_length=255, null=True)),
                ('sign_level', models.CharField(blank=True, max_length=255, null=True)),
                ('sign_teach', models.CharField(blank=True, max_length=50, null=True)),
                ('sign_conid', models.ForeignKey(db_column='sign_conid', on_delete=django.db.models.deletion.DO_NOTHING, to='contestms.contest')),
                ('sign_stuid', models.ForeignKey(db_column='sign_stuid', on_delete=django.db.models.deletion.DO_NOTHING, to='userms.student')),
            ],
            options={
                'db_table': 'tt_sign',
                'managed': True,
            },
        ),
    ]