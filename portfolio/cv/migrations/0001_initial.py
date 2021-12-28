# Generated by Django 3.2.4 on 2021-12-26 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CVS',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('data', models.BinaryField(unique=True)),
                ('active', models.BooleanField()),
            ],
        ),
    ]