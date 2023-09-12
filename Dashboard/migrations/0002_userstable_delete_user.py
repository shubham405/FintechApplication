# Generated by Django 4.2.3 on 2023-07-29 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=150, null=True)),
                ('password', models.CharField(max_length=300)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_table',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
