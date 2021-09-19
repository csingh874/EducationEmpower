from django.contrib import admin
from .models import *
import nested_admin
# Register your models here.


class SubHeadingInline(nested_admin.NestedStackedInline):
    model = CourseSubHeading
    extra = 0


class HeadingInline(nested_admin.NestedStackedInline):
    model = CourseHeading
    extra = 0
    inlines = [SubHeadingInline]


class CourseDescriptionAdmin(nested_admin.NestedModelAdmin):
    inlines = [HeadingInline]
    list_display = ('id', 'title', 'short_description', 'price', )


admin.site.register(CourseDescription, CourseDescriptionAdmin)
admin.site.register(CourseHeading)
admin.site.register(CourseSubHeading)
admin.site.register(OrderDetails)
admin.site.site_header = "Learning Spot"
