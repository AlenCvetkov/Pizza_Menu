from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    CATEGORY_CHOICES = [
        ('classic', 'Класична'),
        ('spicy', 'Пикантна'),
        ('vege', 'Вегетаријанска'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='classic')
    toppings = models.ManyToManyField(Topping)
    image = models.ImageField(upload_to='pizzas/',null=True, blank=True)
    orders_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Закажана'),
        ('in_progress', 'Во подготовка'),
        ('completed', 'Завршена'),
    ]

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    chef = models.ForeignKey(User, on_delete=models.CASCADE,related_name='chef_orders')
    assistants=models.ManyToManyField(User, related_name='assistants_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    order_time=models.DateTimeField()
    note = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Нарачка за {self.pizza.name} - {self.status}"


    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.order_time > timezone.now():
            self.status = 'scheduled'
        elif self.status == 'scheduled' and self.order_time < timezone.now():
            self.status = 'completed'


        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if old_order.status == 'in_progress' and self.status == 'completed':
                self.pizza.orders_count += 1
                self.pizza.save()

        super().save(*args, **kwargs)