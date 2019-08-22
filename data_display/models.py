from django.db import models
import data_display.utils.constants as constants

# Create your models here.
photo = models.ImageField(upload_to="gallery")


class Students(models.Model):
    student_id = models.IntegerField(default=-1)
    name = models.CharField(max_length=200, default='N/A')
    email = models.CharField(max_length=200, default='N/A')
    discipline = models.CharField(max_length=200, default='N/A')
    year = models.CharField(max_length=200, default='N/A')
    phone = models.CharField(max_length=200, default=-1)
    interview_offer = models.BooleanField(null=True, default=False)
    project_name = models.CharField(max_length=200, default='N/A')

    # clean data that might be a little different/wrong type, but semantically correct
    def transform_data(self):
        # Generally if someone did get an interview, the only 'Truthy' value that means false is 'No'.
        if not isinstance(self.interview_offer, bool):
            if self.interview_offer != 'No' and self.interview_offer:
                self.interview_offer = True
            elif self.interview_offer:
                self.interview_offer = False

    # make sure that clean is called before we save,
    # (clean is called in full_clean: https://stackoverflow.com/questions/7366363/adding-custom-django-model-validation)
    def save(self, *args, **kwargs):
        self.transform_data()
        super(Students, self).save(*args, **kwargs)


class Teams(models.Model):
    team_name = models.CharField(max_length=200)
    num_members = models.IntegerField()
    avg_yos = models.FloatField()
    most_common_discipline = models.CharField(max_length=200)


class Projects(models.Model):
    project_name = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    completion_rate = models.FloatField(max_length=200)
    project_type = models.CharField(max_length=200)


class NotForProfits(models.Model):
    nfp_name = models.CharField(max_length=200)
    years_w_veep = models.FloatField()
    num_projects = models.IntegerField()
    num_projects_completed = models.IntegerField()
    primary_email = models.CharField(max_length=200)


def get_model_from_name(model_name):
    return {
        constants.STUDENTS: Students,
        constants.TEAMS: Teams,
        constants.PROJECTS: Projects,
        constants.NFPS: NotForProfits
    }[model_name]
