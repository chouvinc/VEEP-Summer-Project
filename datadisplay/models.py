from django.db import models

# Create your models here.


class Students(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    discipline = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)
    interview_offer = models.BooleanField(null=True, default=None)
    project_name = models.CharField(max_length=200)


