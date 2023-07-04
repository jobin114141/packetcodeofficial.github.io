from django.shortcuts import redirect, render
from home.models import NewUser, crain, crain_completed, sold_cars

def crain_main(request):
    booking=crain.objects.filter(on_going=0)
    userid=request.user.id
    craindriver_phone=request.user.phone
    craindriver_name=request.user.username
    busy=crain.objects.filter(craindriver=userid,on_going=1)
    

    if request.method == 'POST':
        id = request.POST.get('id')
        staring_km=request.POST.get('staring_km')
        print(staring_km)

        startt = crain.objects.get(id=id)
        startt.on_going = 1
        startt.craindriver=userid

        startt.craindriver_phonenumber=craindriver_phone
        startt.craindriver_name=craindriver_name

        startt.staring_km=staring_km
        startt.save()
        return render(request,'crain_service/crain_main.html',{'booking': booking,"busy" : busy})
    return render(request,'crain_service/crain_main.html',{'booking': booking,"busy": busy})

def Start(request):
    userid=request.user.id
    temp1=crain.objects.get(craindriver=userid,on_going=1)
    car_name=temp1.car_name
    c_user_id=temp1.user_id
    sold_car_id=sold_cars.objects.get(user_id=c_user_id,car_name=car_name)
    s_id=sold_car_id.id
    if request.method == 'POST':
        
        end_km=request.POST.get('end_km')
        
        
        int_end_km=int(end_km)
        total_km =int_end_km - temp1.staring_km 
        price=total_km*7.5

        temp1.end_km=int_end_km
        temp1.total_km=total_km
        temp1.price=price
        temp1.save()

        sold_car=sold_cars.objects.get(id=s_id)
        sold_car.crain_deliverd=1
        sold_car.save()



        return render(request,'crain_service/Start.html',{"temp1" : temp1 ,"total_km" : total_km ,"int_end_km" : int_end_km,"price":price})
    return render(request,'crain_service/Start.html',{"temp1" : temp1 })


def payment(request):
    userid=request.user.id
    temp1=crain.objects.get(craindriver=userid,on_going=1)
    temp1.completed=1
    temp1.save()  

    all=crain.objects.get(craindriver=userid,on_going=1,completed=1)
    car_name=all.car_name
    car_number=all.car_number
    contact_number=all.contact_number
    yard_name=all.yard_name
    drop_out_location=all.drop_out_location
    user_id=all.user_id
    craindriver=all.craindriver
    total_km=all.total_km
    price=all.price

    Crain =crain_completed(car_name=car_name,car_number=car_number,price=price,craindriver=craindriver,total_km=total_km,yard_name=yard_name,drop_out_location=drop_out_location,user_id=user_id,contact_number=contact_number)
    Crain.save() 

    to_delete=crain.objects.get(craindriver=userid,on_going=1,completed=1)
    to_delete.delete()

    booking=crain.objects.filter(on_going=0)  
    busy=crain.objects.filter(craindriver=userid,on_going=1)
    return redirect('crain_main')



def craindriver_reg(request):
    if request.method=='POST':        
        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        district=request.POST['district']
        is_active = 1        
        type='crain'
        nw=NewUser.objects.create_user(username=username,password=password,email=email,phone=phone,type=type,address=address,is_active=is_active,district=district)        
        nw.save()
        return render(request,'home.html')
    else:
        return render(request,'crain_service/craindriver_reg.html')