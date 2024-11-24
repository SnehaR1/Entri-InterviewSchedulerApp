from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

"""CustomUser model store informations of interviewer,candidate and manager.
   Availability model stores the user's id,date,start_time and end time within whihc they will be available.Somehting to be noted here is that users cannot provide/add multiple availability for a single day
"""


class CustomUser(AbstractUser):

    RoleChoices = [
        ("user", "user"),
        ("interviewer", "interviewer"),
        ("manager", "manager"),
    ]
    role = models.CharField(null=False, blank=False, choices=RoleChoices)

    def __str__(self):
        return self.username


class Availability(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="availabilities"
    )
    interview_date = models.DateField(default="2024-11-23")
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)

    class Meta:
        unique_together = ("interview_date", "user")
