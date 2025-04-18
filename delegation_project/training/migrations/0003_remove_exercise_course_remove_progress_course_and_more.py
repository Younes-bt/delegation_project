# Generated by Django 5.2 on 2025-04-14 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_room'),
        ('training', '0002_attendance_mark'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='course',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='course',
        ),
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='exercise',
            name='answer_options',
            field=models.JSONField(blank=True, help_text='Options for QCM exercises', null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='correct_answer',
            field=models.TextField(blank=True, help_text='Correct answer for the exercise', null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Medium', max_length=10),
        ),
        migrations.AddField(
            model_name='exercise',
            name='estimated_time',
            field=models.PositiveIntegerField(blank=True, help_text='Estimated time in minutes', null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.CharField(choices=[('QCM', 'Multiple Choice Question'), ('Simple', 'Simple Exercise'), ('Project', 'Project Exercise'), ('Quiz', 'Quiz')], default='Simple', max_length=10),
        ),
        migrations.AddField(
            model_name='exercise',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='exercise_images/'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='points',
            field=models.PositiveIntegerField(blank=True, help_text='Points allocated for this exercise in the control', null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='question',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='AnnualDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('week', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annual_distributions', to=settings.AUTH_USER_MODEL)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annual_distributions', to='accounts.training')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='annual_distribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='training.annualdistribution'),
        ),
        migrations.AddField(
            model_name='progress',
            name='annual_distribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.annualdistribution'),
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('control_type', models.CharField(choices=[('Midterm', 'Midterm Exam'), ('Final', 'Final Exam'), ('Quiz', 'Quiz'), ('Project', 'Project')], default='Quiz', max_length=20)),
                ('total_points', models.PositiveIntegerField(default=20)),
                ('passing_score', models.PositiveIntegerField(default=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('annual_distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='training.annualdistribution')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='accounts.center')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='accounts.traininggroup')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to=settings.AUTH_USER_MODEL)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='accounts.training')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='exercise',
            name='control',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='training.control'),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
