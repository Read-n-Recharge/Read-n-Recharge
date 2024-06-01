from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def profile(self):
        profile = Profile.objects.get(user=self)  # Return the profile instance


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


# study preference
class StudyPrefernce(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ChronoChoice = [("early_bird", "Early Bird"), ("night_owl", "Night Owl")]
    chronotype = models.CharField(max_length=20, choices=ChronoChoice)

    ConcentrationLevel = [("low", "Low"), ("normal", "Normal"), ("high", "High")]
    concentration = models.CharField(max_length=20, choices=ConcentrationLevel)

    StudyingStyle = [("group", "Group Study"), ("solo", "Solo Study")]
    studying_style = models.CharField(max_length=10, choices=StudyingStyle)

    procrastination = models.BooleanField()
    physical_activity = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.chronotype} - {self.studying_style}"
