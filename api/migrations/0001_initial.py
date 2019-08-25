# Generated by Django 2.2.4 on 2019-08-25 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('citizen_id', models.PositiveIntegerField()),
                ('town', models.CharField(max_length=256)),
                ('street', models.CharField(max_length=256)),
                ('building', models.CharField(max_length=256)),
                ('apartment', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=256)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=256)),
                ('enclosing_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizens', to='api.Import')),
                ('relatives', models.ManyToManyField(blank=True, related_name='_citizen_relatives_+', to='api.Citizen')),
            ],
        ),
    ]