from django.db import models
import uuid


# Create your models here.

class buslist(models.Model):
    bus_name =  models.CharField()
    route_no = models.CharField()
    bus_start_loc = models.CharField()
    bus_end_loc = models.CharField()
    service_start_time = models.TimeField()
    service_reached_time = models.TimeField()
    count_of_seats =models.IntegerField()
    price = models.PositiveSmallIntegerField()







class journey(models.Model):
    pick = models.CharField()
    drop = models.CharField()
    seat = models.IntegerField()
    date = models.DateField()
    passanger_name = models.CharField()
    email_id = models.EmailField()
    phone_no = models.CharField()
    bus = models.ForeignKey(buslist, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = str(uuid.uuid4())[:8].upper()  # auto generate 8-char ticket ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.passanger_name}"
