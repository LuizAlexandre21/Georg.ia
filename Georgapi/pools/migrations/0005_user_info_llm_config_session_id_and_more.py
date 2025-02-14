# Generated by Django 5.1.5 on 2025-02-14 20:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pools', '0004_alter_llm_request_session_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User Info',
                'verbose_name_plural': 'User Infos',
            },
        ),
        migrations.AddField(
            model_name='llm_config',
            name='session_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pools.llm_session'),
        ),
        migrations.AddField(
            model_name='llm_session',
            name='name_model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='llm_config',
            name='model_url',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='llm_interaction_log',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='llm_request',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='llm_request',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.llm_session'),
        ),
        migrations.AlterField(
            model_name='llm_session',
            name='started_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='llm_interaction_log',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.user_info'),
        ),
        migrations.AlterField(
            model_name='llm_request',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.user_info'),
        ),
        migrations.AlterField(
            model_name='llm_session',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.user_info'),
        ),
    ]
