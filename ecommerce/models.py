from django.db import models
import uuid
from PIL import Image
from ckeditor.fields import RichTextField
# Create your models here.


class CourseDescription(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Course Title",
                             help_text="Main Title of the Course  (Max characters allowed 100)")
    short_description = models.CharField(max_length=250, null=False, blank=False, verbose_name="Course Description",
                                         help_text="Short Description of the course (Max characters allowed 250)")
    image = models.ImageField(upload_to="courses", help_text="Course Image", verbose_name="Upload Image")
    price = models.PositiveIntegerField(blank=False, null=False, help_text="What is the price of the course",
                                        verbose_name="Price")
    description = RichTextField(blank=True, null=True)
    idx = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class CourseHeading(models.Model):
    course = models.ForeignKey(CourseDescription, on_delete=models.CASCADE, verbose_name="Course")
    heading = models.CharField(max_length=100, null=False, blank=False, verbose_name="Heading",
                               help_text="Max characters allowed 100")

    def __str__(self):
        return self.heading


class CourseSubHeading(models.Model):
    headings = models.ForeignKey(CourseHeading, on_delete=models.CASCADE, verbose_name="Course Heading")
    sub_heading = models.CharField(max_length=100, null=False, blank=False, verbose_name=" Sub Heading",
                                   help_text="Max characters allowed 100")
    duration = models.CharField(max_length=10, blank=False, null=False, verbose_name="Duration",
                                help_text="Duration of the recording")
    url = models.TextField(blank=True, null=True)
    display = models.BooleanField(default=False, verbose_name="Display Recording",
                                  help_text="Click on checkbox if you wish to display recording to unauthorized user")

    def __str__(self):
        return self.sub_heading

