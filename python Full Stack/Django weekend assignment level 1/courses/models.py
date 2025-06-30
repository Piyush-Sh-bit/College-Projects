from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.title
