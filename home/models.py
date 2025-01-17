from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="Manzil nomi")
    description = models.TextField(verbose_name="Manzil haqida ma'lumot")
    image = models.ImageField(upload_to='destinations/', verbose_name="Manzil rasmi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"

class TourPackage(models.Model):
    TRANSPORT_CHOICES = [
        ('BUS', 'Avtobus'),
        ('TRAIN', 'Poyezd'),
        ('PLANE', 'Samolyot'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tur paketi nomi")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Manzil")
    description = models.TextField(verbose_name="Tur haqida ma'lumot")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Narxi"
    )
    duration_days = models.PositiveIntegerField(verbose_name="Davomiyligi (kunlarda)")
    max_people = models.PositiveIntegerField(verbose_name="Maksimal odamlar soni")
    transport_type = models.CharField(
        max_length=5,
        choices=TRANSPORT_CHOICES,
        verbose_name="Transport turi"
    )
    includes_hotel = models.BooleanField(default=True, verbose_name="Mehmonxona kiradi")
    includes_food = models.BooleanField(default=True, verbose_name="Ovqat kiradi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tur paketi"
        verbose_name_plural = "Tur paketlari"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Kutilmoqda'),
        ('CONFIRMED', 'Tasdiqlangan'),
        ('CANCELLED', 'Bekor qilingan'),
    ]
    
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, verbose_name="Tur paketi")
    first_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, verbose_name="Telefon raqami")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Holat"
    )

    booking_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumotlar")
    active = models.BooleanField(default=True, verbose_name="Tur paketi aktivmi?")
    def __str__(self):
        return f"{self.tour_package.name}"
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"