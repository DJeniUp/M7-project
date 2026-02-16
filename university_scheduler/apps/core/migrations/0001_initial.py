from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True)),
            ],
            options={'ordering': ['number']},
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('country', models.CharField(max_length=100)),
                (
                    'available_modules',
                    models.ManyToManyField(blank=True, related_name='available_teachers', to='core.module'),
                ),
                (
                    'specializations',
                    models.ManyToManyField(blank=True, related_name='teachers', to='core.specialization'),
                ),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('level', models.PositiveIntegerField()),
                ('is_core', models.BooleanField(default=True)),
                ('prerequisites', models.ManyToManyField(blank=True, symmetrical=False, to='core.course')),
                (
                    'specialization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='courses',
                        to='core.specialization',
                    ),
                ),
                (
                    'teacher',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='courses',
                        to='core.teacher',
                    ),
                ),
            ],
            options={'ordering': ['name']},
        ),
    ]

