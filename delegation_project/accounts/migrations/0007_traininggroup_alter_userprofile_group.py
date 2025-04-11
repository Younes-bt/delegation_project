# Generated by Django 5.2 on 2025-04-11 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_association_city_alter_center_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.center')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.training')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.traininggroup'),
        ),
    ]
