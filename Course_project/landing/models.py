from django.db import models

class Subscribers(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

# Create your models here.
    def __str__(self):
            return "%s %s %s" % (self.id,self.email,self.name)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
