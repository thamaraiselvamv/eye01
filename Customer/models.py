from django.db import models
from django.utils import timezone
# Create your models here.
class customer(models.Model):
    name=models.CharField(max_length=50)
    email_id=models.EmailField()
    password=models.CharField(max_length=18)

    def __str__(self):
        return self.email_id
    
class SenderMail(models.Model):
    send_Id = models.ForeignKey(customer, on_delete=models.CASCADE)
    sender = models.EmailField()
    receiver = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_time = models.DateTimeField()

    def __str__(self):
        return self.sender

    def save(self, *args, **kwargs):
        if not self.sent_time:
            # Set the sent_time to the current time in the Indian time zone
            self.sent_time = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(330))
        super().save(*args, **kwargs)

class ReceiverMail(models.Model):
    inbox_Id = models.ForeignKey(customer, on_delete=models.CASCADE)
    sender = models.EmailField()
    receiver = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    received_time = models.DateTimeField()

    def __str__(self):
        return self.sender

    def save(self, *args, **kwargs):
        if not self.received_time:
            # Set the received_time to the current time in the Indian time zone
            self.received_time = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(330))
        super().save(*args, **kwargs)