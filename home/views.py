from .models import buslist,journey
from django.shortcuts import render, get_object_or_404,redirect
from logsign.models import sign
from .forms import bookingform
from django.utils.crypto import get_random_string
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def homeview(request,person):
    person = sign.objects.filter(name = person).first()
    data = buslist.objects.all()
    context = {'data': enumerate(data,start=1),
               'person':person}
    return render(request,'home.html',context)

def seatbookview(request,bus):
    busid = buslist.objects.filter(id = bus)
    bus_seat = get_object_or_404(buslist,id = bus)
    error = ''
    if request.method == 'POST':
        form = bookingform(request.POST)
        if form.is_valid():
            pick = form.cleaned_data['pick']
            drop = form.cleaned_data['drop']
            seat = form.cleaned_data['seat']
            date = form.cleaned_data['date']
            passanger_name = form.cleaned_data['passanger_name']
            email_id = form.cleaned_data['email_id']
            phone_no = form.cleaned_data['phone_no']
            if seat > bus_seat.count_of_seats:
                error = 'not enough seats available'
            else: 
                booking = journey.objects.create(pick = pick,drop = drop,seat = seat,date = date,passanger_name = passanger_name,email_id = email_id ,phone_no = phone_no,bus = bus_seat)
                bus_seat.count_of_seats -= seat
                bus_seat.save()
            return render(request,"tickets.html",{'ticket':booking})
    form = bookingform()
    return render(request,"seatbook.html",{'bus':bus_seat,'form':form ,'error':error})

def cancelview(request, journey_id):
    ticket = get_object_or_404(journey, id=journey_id)
    if request.method == 'POST':
        bus = ticket.bus
        bus.count_of_seats += ticket.seat 
        bus.save()
        person = ticket.passanger_name
        ticket.delete()
        return redirect('home',person = person)  
    return render(request,"cancel.html", {'ticket': ticket})

def cancelticket(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        try:
            ticket = journey.objects.get(ticket_number=ticket_number)
            bus = ticket.bus
            bus.count_of_seats += ticket.seat
            bus.save()
            ticket.delete()
            messages.success(request, f'Ticket {ticket_number} has been successfully cancelled.')
            return redirect('cancelticket') 
        except journey.DoesNotExist:
            messages.error(request, 'Invalid ticket number.')
    return render(request, 'cancelticket.html')

def viewticket(request):
    ticket_data = None
    error = None
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        try:
            ticket_data = journey.objects.get(ticket_number=ticket_number)
        except journey.DoesNotExist:
            error = "Invalid ticket number. Please try again."
    return render(request, 'viewticket.html', {'ticket': ticket_data, 'error': error})

def recoverticket(request):
    tickets = None
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_str = request.POST.get('date')
        try:
            journey_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            journey_date = None
            error = "Invalid date format."
        if email and phone and journey_date:
            tickets = journey.objects.filter(
                email_id=email,
                phone_no=phone,
                date=journey_date
            )
            if not tickets.exists():
                error = "No tickets found with the provided details."
                tickets = None
    return render(request, 'recoverticket.html', {'tickets': tickets, 'error': error})




def downloadticket(request, ticket_id):
    ticket = get_object_or_404(journey, id=ticket_id)
    template_path = 'pdf.html'

    context = {'ticket': ticket}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_number}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
