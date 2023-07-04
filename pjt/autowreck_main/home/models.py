from django.db import models
from django.contrib.auth.models import AbstractUser

class NewUser(AbstractUser):
    phone= models.IntegerField(null=True)
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

class car(models.Model):
    car_name=models.CharField(max_length=55,null=True)
    car_model=models.IntegerField(null=True)
    yard_name=models.CharField(max_length=255,null=True)
    min_amount=models.IntegerField(null=True)

    image = models.ImageField(upload_to='car_images/')
    image2 = models.ImageField(upload_to='car_images/')
    image3 = models.ImageField(upload_to='car_images/')
    image4 = models.ImageField(upload_to='car_images/')
    image5 = models.ImageField(upload_to='car_images/')

    battery = models.BooleanField(default=False)
    door = models.BooleanField(default=False)
    hood = models.BooleanField(default=False)
    front_bumber = models.BooleanField(default=False)
    head_lights = models.BooleanField(default=False)
    wind_shield = models.BooleanField(default=False)
    pillars = models.BooleanField(default=False)
    engine_room = models.BooleanField(default=False)
    apron = models.BooleanField(default=False)
    clutch = models.BooleanField(default=False)
    gerabox = models.BooleanField(default=False)
    steering_box = models.BooleanField(default=False)
    air_bag = models.BooleanField(default=False)

    is_active=models.BooleanField(default=0)

    display_or_not=models.BooleanField(default=0)

class auction(models.Model):
    car_id=models.IntegerField()
    car_name=models.CharField(max_length=25)
    user_id=models.IntegerField()
    user_name=models.CharField(max_length=25)
    bid_amount=models.IntegerField()
    phone=models.IntegerField()
    largest_bid=models.IntegerField(default=False)
    sold_or_no=models.IntegerField(default=False)
    
class closed_deals(models.Model):
    car_id=models.IntegerField()
    car_name=models.CharField(max_length=25)
    user_id=models.IntegerField()
    user_name=models.CharField(max_length=25)
    bid_amount=models.IntegerField()
    phone=models.IntegerField()
    deal_closed=models.IntegerField(default=False)

class sold_cars(models.Model):
    car_id=models.IntegerField()
    car_name=models.CharField(max_length=25)
    user_id=models.IntegerField()
    user_name=models.CharField(max_length=25)
    bid_amount=models.IntegerField()
    phone=models.IntegerField()
    crain_deliverd=models.IntegerField(default=0)
    crain_status=models.IntegerField(default=0)

class crain(models.Model):
    car_id=models.IntegerField(default=0)
    car_name=models.CharField(max_length=25)
    car_number=models.CharField(max_length=25,default=False)
    contact_number=models.IntegerField()
    yard_name=models.CharField(max_length=25)
    drop_out_location=models.CharField(max_length=25)
    user_id=models.IntegerField()
    on_going=models.IntegerField(default=0)
    craindriver=models.IntegerField(default=0)
    
    craindriver_name=models.CharField(max_length=25,default=False)
    craindriver_phonenumber=models.IntegerField(default=0)

    staring_km=models.IntegerField(default=0)
    end_km=models.IntegerField(default=0)
    total_km=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    completed=models.IntegerField(default=0)

class crain_completed(models.Model):
    car_name=models.CharField(max_length=25)
    car_number=models.CharField(max_length=25)
    contact_number=models.IntegerField()
    yard_name=models.CharField(max_length=25)
    drop_out_location=models.CharField(max_length=25)
    user_id=models.IntegerField()
    craindriver=models.IntegerField(default=0)

    total_km=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
  