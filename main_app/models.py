from django.db import models
# Import the reverse function
from django.urls import reverse
from datetime import date

FUNCTION = (
    ('Drivetrain', 'Drivetrain'),
    ('Braking', 'Braking'),
    ('Other', 'Other')
)

class Component(models.Model):
    type = models.CharField(max_length=50)
    functionality = models.CharField(
        max_length=15,
        choices=FUNCTION,
        default=FUNCTION[0][0]
    )
    
    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('components_detail', kwargs={'pk': self.id})

# Create your models here.
class Bike(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    condition = models.CharField(max_length=100)
    # Add the M:M relationship
    components = models.ManyToManyField(Component)

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('detail', kwargs={'bike_id': self.id})

class Order(models.Model):
    date = models.DateField('Order Date')
    items = models.CharField(max_length=100)
    total = models.IntegerField()

    # Create a bike_id FK
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.total} on {self.date}"

    # This will change the default sort order
    class Meta:
        ordering = ['-date']