from django.db import models
from django.utils.timezone import now


class Import(models.Model):
    pass


class Citizen(models.Model):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    enclosing_import = models.ForeignKey(Import, related_name='citizens', on_delete=models.CASCADE)
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    building = models.CharField(max_length=256)
    apartment = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    birth_date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=256)
    relatives = models.ManyToManyField("self", blank=True)

    @property
    def age(self):
        today = now()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
