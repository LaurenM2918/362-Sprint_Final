# Generated by Django 3.1.7 on 2021-05-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210415_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewsList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='userlogin',
            old_name='email',
            new_name='username',
        ),
    ]