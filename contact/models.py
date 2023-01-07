from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    message = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.name} / {self.email}'
