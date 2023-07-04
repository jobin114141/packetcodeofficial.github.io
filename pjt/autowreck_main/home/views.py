from io import BytesIO
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from flask import get_template_attribute
from home.models import NewUser,car,closed_deals,auction, crain_completed,sold_cars
from django.db.models import Q

from xhtml2pdf import pisa

def home(request):
    return render(request,'home.html')

from django.contrib import messages

def c_reg(request):
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        district = request.POST['district']
        is_active = 1        
        user_type = 'customer'
        
        # Check if the username already exists
        if NewUser.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken.')
            return render(request, 'c_reg.html')
        
        nw = NewUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            type=user_type,
            address=address,
            is_active=is_active,
            district=district
        )
        nw.save()
        return render(request, 'home.html')
    else:
        return render(request, 'c_reg.html')





def main_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("login")
            type = user.type
            loc=user.district
            is_superuser=user.is_superuser
            
            if type=="customer":                
                return redirect('c_mainpage')
            elif type=='manager':
                return render(request, 'm_page.html')
            elif type=='inspection_team':
                return redirect('i_mainpage')
            elif type=='crain':
                return redirect('crain_main')                    
            elif is_superuser == 1:
                return redirect('main_admin')
                
        else:
            print("not possible")
            messages.info(request, 'Invalid username or password')  # Add error message
            return render(request, 'main_login.html')

    return render(request, 'main_login.html')



def m_reg(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        district=request.POST['district']
        type='manager'
        is_active = 1
        nw=NewUser.objects.create_user(username=username,password=password,email=email,phone=phone,type=type,address=address,is_active=is_active,district=district)        
        nw.save();
        return render(request,'home.html')
    else:
        return render(request,'m_reg.html')

def main_admin(request):
    return render(request,'main_admin.html')

def inactive(request):
    customers = NewUser.objects.filter(is_active=0)
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = NewUser.objects.get(id=customer_id)
        customer.is_active = 1
        customer.save()
        return redirect('inactive')
    return render(request, 'inactive.html', {'customers': customers})


def admin_car_upload(request):
    cars = car.objects.exclude(is_active=1)
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_model = request.POST.get('car_model')
        yard_name = request.POST.get('yard_location')
        min_amount = request.POST.get('min_amount')
        Car = car(car_name=car_name, car_model=car_model, yard_name=yard_name, min_amount=min_amount)
        Car.save() 
                          
        # Car_id = request.POST.get('car_id')
        # print(Car_id)
        # print("+++++++++++++")
        # Car = car.objects.get(id=Car_id)
        # car.objects.filter(id=Car_id).delete()
        # Car.delete()
        # return render(request,'admin_car_upload.html', {'cars': cars})
    return render(request,'admin_car_upload.html', {'cars': cars})
        
def manager_admin_viewpage(request):
    # set1= NewUser.objects.filter(Q(district='kottayam') | Q(district='idikki')| Q(district='thodupuzha'))
    # set2= NewUser.objects.filter(Q(district='alapuzha') | Q(district='ekm')| Q(district='thrissure'))
    # set3= NewUser.objects.filter(Q(district='kozhikode') | Q(district='malapuram')| Q(district='kasargod'))

    # dests=car.objects.all()
    # context = {'set1': set1, 'set2': set2, 'set3': set3,'dests':dests}
    
    c_user=NewUser.objects.filter(type="customer")
    i_user=NewUser.objects.filter(type="inspection_team")
    crain=NewUser.objects.filter(type="crain")

    context = {'c_user': c_user,'i_user': i_user,"crain":crain}
    alluser=NewUser.objects.all()
    userid=request.POST.get("user_id")
    print(userid)
    if request.method == 'POST':
        temp = NewUser.objects.get(id=userid)
        NewUser.objects.filter(id=userid).delete()
        temp.delete()
        return render(request,'manager_admin_viewpage.html', context)
    return render(request,'manager_admin_viewpage.html',context )







def admin_sail_details(request):
    todays_lists= auction.objects.filter(largest_bid=1,sold_or_no=0)
    return render(request,'admin_sail_details.html',{'todays_lists':todays_lists})


def sail_close(request, list_id):
    auction_dtails=auction.objects.get(id=list_id)
    if request.method == 'POST':
        auction_dtails.sold_or_no=1
        auction_dtails.save()

        car_id=auction_dtails.car_id
        car_name=auction_dtails.car_name
        user_id=auction_dtails.user_id
        user_name=auction_dtails.user_name
        price=auction_dtails.bid_amount
        phone=auction_dtails.phone

        car_table=car.objects.get(id=car_id)
        car_table.display_or_not=1
        car_table.save() 

        sold_carss=sold_cars(car_id=car_id,car_name=car_name,user_id=user_id,user_name=user_name,bid_amount=price,phone=phone)
        sold_carss.save()

        todays_lists= auction.objects.filter(largest_bid=1,sold_or_no=0)
        return render(request,'admin_sail_details.html',{'todays_lists':todays_lists})

        
        
    return render(request,'sail_close.html',{"auction_dtails":auction_dtails})


def All_bids(request):
    all=auction.objects.filter()
    
    return render(request,'All_bids.html',{"all":all})

def closed_deals(request):
    all=auction.objects.filter(sold_or_no=1)
    
    return render(request,'closed_deals.html',{"all":all})

def remove_car(request):
    cars=car.objects.filter(display_or_not=0)
    Car_id = request.POST.get('car_id')
    if request.method == 'POST':
        
        print(Car_id)
        print("+++++++++++++")
        Car = car.objects.get(id=Car_id)
        car.objects.filter(id=Car_id).delete()
        Car.delete()
        return render(request,'remove_car.html', {'cars': cars})
    return render(request,'remove_car.html', {'cars': cars})
    


def crain_delliverd(request):
    all=crain_completed.objects.filter()
    return render(request,'crain_delliverd.html',{"all":all})
