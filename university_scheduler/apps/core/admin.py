from django.contrib import admin

from .models import Course, Module, Specialization, Teacher


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('number',)
    ordering = ('number',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country', 'specializations')
    search_fields = ('name',)
    filter_horizontal = ('specializations', 'available_modules')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'level', 'teacher', 'is_core')
    list_filter = ('specialization', 'level', 'is_core', 'teacher')
    search_fields = ('name',)
    filter_horizontal = ('prerequisites',)
