from django.db import models

# Create your models here.

# class Projects(models.Model):
#     project_name = models.CharField(max_length=200, primary_key = True)
#     not_for_profit_name = models.ForeignKey(notForProfit, on_delete=models.CASCADE)

class Students(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    discipline = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)
    interview_offer = models.BooleanField(null=True, default=None)
    project_name = models.CharField(max_length = 200)

# class notForProfit(models.Model):
#     not_for_profit_name.CharField(max_length=200, primary_key = True)
#     email = models.CharField(max_length=200)
#     project_name = models.ForeignKey(Projects, on_delete=models.CASCADE)S

# class Teams(models.Model):
#     team_member_id = models.IntegerField(primary_key = True)
#     project_name = models.ForeignKey(Projects, on_delete = CASCADE)
#     student_id = models.ForeignKey(Students, on_delete = CASCADE)