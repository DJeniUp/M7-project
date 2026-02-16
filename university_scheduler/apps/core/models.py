from django.db import models


class Specialization(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    number = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['number']

    def __str__(self) -> str:
        return f'Module {self.number}'


class Teacher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    specializations = models.ManyToManyField(Specialization, related_name='teachers', blank=True)
    available_modules = models.ManyToManyField(Module, related_name='available_teachers', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, related_name='courses')
    level = models.PositiveIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='courses')
    is_core = models.BooleanField(default=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
