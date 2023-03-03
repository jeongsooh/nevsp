# Generated by Django 4.1.7 on 2023-03-02 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ocpp16',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpnumber', models.CharField(max_length=128, verbose_name='충전기번호')),
                ('msg_direction', models.IntegerField(verbose_name='메시지오리진')),
                ('msg_name', models.CharField(max_length=128, verbose_name='메시지이름')),
                ('msg_content', models.TextField(verbose_name='메시지본문')),
                ('connection_id', models.CharField(max_length=128, verbose_name='커넥션아이디')),
                ('register_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록일시')),
            ],
            options={
                'verbose_name': '메시지정보',
                'verbose_name_plural': '메시지정보',
                'db_table': 'nevsp_ocpp16',
            },
        ),
    ]
