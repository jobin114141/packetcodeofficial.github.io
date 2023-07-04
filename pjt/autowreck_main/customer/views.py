
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.db.models import F, Max
from home.models import NewUser,car,auction,closed_deals, crain_completed,sold_cars,crain
import datetime
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
now1 = datetime.date.today()

def c_mainpage(request):
    car1 = car.objects.filter(display_or_not=0,is_active=1)
    start_time = datetime.time(9, 0)   # 9:00 AM
    end_time = datetime.time(23, 0)   # 5:00 PM
    now = datetime.datetime.now().time()


    if start_time <= now <= end_time:
        for bid in auction.objects.values('car_id').annotate(max_bid=Max('bid_amount')):
            try:
                previous_highest_bid = auction.objects.get(car_id=bid['car_id'], largest_bid=True)
                if previous_highest_bid.bid_amount < bid['max_bid']:
                    previous_highest_bid.largest_bid = False
                    previous_highest_bid.save()
            except auction.DoesNotExist:
                pass
            
            auctions = auction.objects.filter(car_id=bid['car_id'], bid_amount=bid['max_bid'])
            if auctions:
                auction_to_update = auctions.first()
                if not auction_to_update.largest_bid:
                    auction_to_update.largest_bid = True
                    auction_to_update.save()
 
        return render(request, 'customer/c_mainpage.html', {'car1': car1})
    else:
        all_objects = auction.objects.all()
        all_objects.delete() 
           
        return render(request, 'customer/c_mainpage.html')


def c_view_details(request, car_id):
    car1 = get_object_or_404(car, pk=car_id)
    car_name=car1.car_name
    
    highest_bid = auction.objects.filter(car_id=car_id ).order_by('-bid_amount').first()
    highest_bid_amount = highest_bid.bid_amount if highest_bid else 0
    if request.method == 'POST':
        bid_amount1 = int(request.POST.get('bid_amount'))
        userid=request.user.id
        user_name=request.user.username
        phone=request.user.phone
        print(phone)
        print("+++++++++++++++++++")
        existing_bid = auction.objects.filter(user_id=userid, car_id=car_id)               
        if existing_bid.exists(): 
            temp1= auction.objects.get(user_id=userid, car_id=car_id) 
            table_price=int(temp1.bid_amount)
            if bid_amount1 > table_price:
                existing_bid.update(bid_amount=bid_amount1)
                return redirect('c_mainpage')
        else:
            auction.objects.create(user_id=userid, car_id=car_id, bid_amount=bid_amount1,car_name=car_name,user_name=user_name,phone=phone) 
            return redirect('c_mainpage')
    return render(request,'customer/c_view_details.html',{"car1": car1, "highest_bid_amount": highest_bid_amount}) 


def dash_board(request):
    userid=request.user.id
    lists=auction.objects.filter(user_id=userid,sold_or_no=0)
    print(lists)
    
    return render(request,'customer/dash_board.html',{"lists":lists})


def My_history(request):
    userid=request.user.id
    """ lists=auction.objects.filter(user_id=userid,sold_or_no=1,largest_bid=1) """
    lists=sold_cars.objects.filter(user_id=userid)
    
    return render(request,'customer/My_history.html',{"lists":lists})




def generate_pdf(request, car_id):
    # Get the data for the car
    details = sold_cars.objects.get(car_id=car_id)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Set the page size to A4
    p.setPageSize((700.27, 900.89))

    # Write the data to the PDF
    p.drawString(300, 800, "Contract Terms")
    p.drawString(30, 765, "This Contract for Car Selling Services is entered into between Autowreck Auction, located at kottayam, and {}".format(details.user_name))
    
    p.drawString(30, 715, "Services to be Provided:")
    p.drawString(30, 700, "Seller agrees to sell the car described as follows: {}, to the Buyer for the bid amount of {}".format(details.car_name, details.bid_amount))
    p.drawString(30, 650, "Payment Terms:")
    p.drawString(30, 635, "The Buyer shall pay the Seller the full bid amount of {} for the car prior to the transfer of ownership".format(details.bid_amount ) )
    p.drawString(30, 620,"Payment shall be made by online, and the Buyer have provide his phone number, {} for confirmation of payment.".format(details.phone))
    p.drawString(30, 575, "Transfer of Ownership:")
    p.drawString(30, 560, "The Seller shall transfer the ownership of the Car to the Buyer upon receipt of the full bid amount.")
    p.drawString(30, 500, "Condition of Car:")
    p.drawString(30, 485, "The Buyer acknowledges that the Car is sold 'as is' and that the Seller makes no representations or warranties")
    p.drawString(30, 470, "as to the condition of the Car.")
    p.drawString(30, 425, "Liability:")
    p.drawString(30, 410, "The Seller shall not be liable for any loss or damage to the Car or its contents that may occur after the transfer of ownership.")
    p.drawString(30, 350, "Governing Law:")
    p.drawString(30, 335, "This Contract shall be governed by and construed in accordance with the laws of the State of kerala, and any legal")
    p.drawString(30, 320,"action arising under this Contract shall be brought in the courts of kerala")
    p.drawString(30, 275, "Entire Agreement:")
    p.drawString(30, 260, "This Contract constitutes the entire agreement between the parties and supersedes all prior agreements and") 
    p.drawString(30, 245, "understandings, whether written or oral, relating to the subject matter of this Contract.")
    p.drawString(30, 200, "IN WITNESS WHEREOF, the parties have executed this Contract on {}.".format(now1))
    p.drawString(30, 185, "Seller: Autowreck Auction")
    p.drawString(30, 170, "Buyer: {}".format(details.user_name))
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='car_sales_contract.pdf')


def sail_closee(request, car_id):
    dtails = sold_cars.objects.get(car_id=car_id)
    return render(request, 'customer/sail_closee.html', {'dtails': dtails})


def crain_page(request):
    userid=request.user.id
    ph= request.user.phone
    lists=sold_cars.objects.filter(user_id=userid,crain_status=0)

    if request.method == 'POST':
        id = request.POST.get('id')
        sold_cars_the_car=sold_cars.objects.get(id=id)
        car_id=sold_cars_the_car.car_id

        thecar=car.objects.get(id=car_id)
        car_name=thecar.car_name
        car_yard_name=thecar.yard_name
        drop_out_location = request.POST.get('drop_out_location')

        print("+++++++++")
        print("+++++++++")
        print("+++++++++")
        print("+++++++++")
        print(drop_out_location)
        print("+++++++++")
        print("+++++++++")
        print("+++++++++")
        print("+++++++++")
        print("+++++++++")


        Crain =crain(car_name=car_name,yard_name=car_yard_name,drop_out_location=drop_out_location,user_id=userid,contact_number=ph,car_id=car_id)
        Crain.save() 

        sold_cars_the_car.crain_status=1
        sold_cars_the_car.save()
        
    return render(request,'customer/crain_page.html',{"lists":lists})



def crain_booking(request):

    return render(request,'customer/crain_booking.html')


def crain_status(request):
    user_id=request.user.id
    all_details = crain.objects.filter(user_id=user_id,on_going=0)
    started=crain.objects.filter(user_id=user_id,on_going=1)
    completed=crain_completed.objects.filter(user_id=user_id)
    return render(request, 'customer/crain_status.html',{"all_details":all_details,"started":started,"completed":completed})

def completed_crain(request):
    user_id=request.user.id
    complt=crain_completed.objects.filter(user_id=user_id)
    return render(request,'customer/completed_crain.html',{"complt":complt})



