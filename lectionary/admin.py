from django.contrib import admin

from lectionary.models import Day, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


class DayAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


admin.site.register(Day, DayAdmin)
