# Generated by Django 3.1.7 on 2021-03-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cert',
            fields=[
                ('cert_id', models.AutoField(primary_key=True, serialize=False)),
                ('cert_imgurl', models.CharField(max_length=255)),
                ('cert_name', models.CharField(max_length=50)),
                ('cert_userx', models.IntegerField()),
                ('cert_usery', models.IntegerField()),
                ('cert_levelx', models.IntegerField()),
                ('cert_levely', models.IntegerField()),
                ('cert_qrcodex', models.IntegerField()),
                ('cert_qrcodey', models.IntegerField()),
                ('cert_teachx', models.IntegerField()),
                ('cert_teachy', models.IntegerField()),
            ],
            options={
                'db_table': 'tt_cert',
                'managed': True,
            },
        ),
    ]
