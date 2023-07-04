from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from home.models import NewUser,car



def i_reg(request):
    if request.method=='POST':        
        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        district=request.POST['district']
        is_active = 1        
        type='inspection_team'
        nw=NewUser.objects.create_user(username=username,password=password,email=email,phone=phone,type=type,address=address,is_active=is_active,district=district)        
        nw.save()
        return render(request,'home.html')
    else:
        return render(request,'inspection_team/i_reg.html')


def i_mainpage(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        instance = NewUser.objects.get(id=user_id)
        loc=instance.district
        if loc=='kottayam' or loc=='idikki' or loc=='thodupuzha':
            cars= car.objects.filter( (Q(yard_name='kottayam') | Q(yard_name='idikki')| Q(yard_name='thodupuzha')) & Q(is_active=0) )
            return render(request,'inspection_team/i_mainpage.html',{'cars':cars})
        elif loc=='alapuzha' or loc=='ekm' or loc=='thrissure':
                    cars= car.objects.filter( (Q(yard_name='alapuzha') | Q(yard_name='ekm')| Q(yard_name='thrissure')) & Q(is_active=0) )
                    return render(request,'inspection_team/i_mainpage.html',{'cars': cars})
        elif loc=='kozhikode' or loc=='malapuram' or loc=='kasargod':
                    cars= car.objects.filter( (Q(yard_name='kozhikode') | Q(yard_name='malapuram')| Q(yard_name='kasargod')) & Q(is_active=0) )
                    return render(request,'inspection_team/i_mainpage.html',{'cars': cars})
    else:
        print("fail")   
    return render(request,'inspection_team/i_mainpage.html')



def inspect_car(request, car_id):
    sum=0
    car1 = get_object_or_404(car, pk=car_id )
    if request.method == 'POST':
        clutch = request.POST.get('clutch') == 'on'
        hood = request.POST.get('hood') == 'on'
        door = request.POST.get('door') == 'on'
        battery = request.POST.get('battery') == 'on'
        front_bumber = request.POST.get('front_bumber') == 'on'
        head_lights = request.POST.get('head_lights') == 'on'
        wind_shield = request.POST.get('wind_shield') == 'on'
        pillars = request.POST.get('pillars') == 'on'
        engine_room = request.POST.get('engine_room') == 'on'
        apron = request.POST.get('apron') == 'on'
        gerabox = request.POST.get('gerabox') == 'on'
        steering_box = request.POST.get('steering_box') == 'on'
        air_bag = request.POST.get('air_bag') == 'on'

        car_image = request.FILES.get('front')
        car_image2 = request.FILES.get('back')

        car_image3 = request.FILES.get('left_side')
        car_image4 = request.FILES.get('right_side')
        car_image5 = request.FILES.get('inside')
        print("________________--")

        if car_image is None:
            print("is empty")  
        else:
            sum=sum+1  

        if car_image2 is None:
            print("is empty 2")  
        else:
            sum=sum+1  

        if car_image is None:
            print("is empty 3")  
        else:
            sum=sum+1  

        if car_image is None:
            print("is empty 4")  
        else:
            sum=sum+1  

        if car_image is None:
            print("is empty 5")  
        else:
            sum=sum+1  



        
        car1.battery=battery
        car1.front_bumber=front_bumber
        car1.head_lights=head_lights
        car1.wind_shield=wind_shield
        car1.pillars=pillars
        car1.engine_room=engine_room
        car1.gerabox=gerabox
        car1.apron=apron
        car1.door=door
        car1.air_bag=air_bag
        car1.steering_box=steering_box
        car1.clutch=clutch
        car1.hood=hood

        car1.image = car_image
        car1.image2 = car_image2
        car1.image3 = car_image3
        car1.image4 = car_image4
        car1.image5 = car_image5
        
        if sum ==5:
            car1.is_active=1
            car1.save()
        

    return render(request,'inspection_team/inspect_car.html', {'car1': car1})
