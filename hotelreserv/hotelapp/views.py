from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from collections import deque
from datetime import datetime

# Initialize data structures
current_reservations = deque()  # Queue for current reservations
waiting_list = deque()         # Queue for waiting list
reservation_history = []       # Stack for reservation history

class Reservation:
    def __init__(self, name, contact, room_number, floor, bedrooms, check_in, check_out):
        self.name = name
        self.contact = contact
        self.room_number = room_number
        self.floor = floor
        self.bedrooms = bedrooms
        self.check_in = check_in
        self.check_out = check_out

def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        bedrooms = int(request.POST['rooms'])
        indate = request.POST['indate']
        outdate = request.POST['outdate']
        
        # Check room availability
        available_rooms = Room.objects.filter(is_available=True, bedrooms=bedrooms)
        if available_rooms.exists():
            room = available_rooms.first()
            
            # Create reservation object
            reservation = Reservation(
                name=name,
                contact=contact,
                room_number=room.number,
                floor=room.floor,
                bedrooms=bedrooms,
                check_in=indate,
                check_out=outdate
            )
            
            # Add to current reservations queue
            current_reservations.append(reservation)
            
            # Add to reservation history stack
            reservation_history.append(reservation)
            
            # Update room availability
            room.is_available = False
            room.save()
            
            return redirect('final')
        else:
            # Add to waiting list queue
            waiting_reservation = Reservation(
                name=name,
                contact=contact,
                room_number=None,
                floor=None,
                bedrooms=bedrooms,
                check_in=indate,
                check_out=outdate
            )
            waiting_list.append(waiting_reservation)
            return render(request, 'error.html')
    return render(request, 'home.html')

def final(request):
    if reservation_history:
        result = reservation_history[-1]  # Get last item from stack
    else:
        result = None
    return render(request, 'final.html', {'result': result})

def availableroom(request):
    rooms = Room.objects.all()
    
    # Create a set of reserved room numbers (convert to strings for comparison)
    reserved_rooms = {str(res.room_number) for res in current_reservations}
    
    # Create a list to hold room data with updated availability
    room_list = []
    for room in rooms:
        # Create a temporary dictionary with room data
        room_data = {
            'number': room.number,
            'floor': room.floor,
            'bedrooms': room.bedrooms,
            'is_available': str(room.number) not in reserved_rooms
        }
        room_list.append(room_data)
        
        # Also update the database
        room.is_available = str(room.number) not in reserved_rooms
        room.save()
    
    return render(request, 'availableroom.html', {'rooms': room_list})

def checkout(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        room_number = request.POST['rooms']
        
        try:
            # Find and remove reservation
            temp_queue = deque()
            found_reservation = None
            
            while current_reservations:
                res = current_reservations.popleft()
                if res.name == name and res.contact == contact and str(res.room_number) == room_number:
                    found_reservation = res
                else:
                    temp_queue.append(res)
            
            # Restore other reservations
            current_reservations.extend(temp_queue)
            
            if found_reservation:
                # Update room availability
                room = Room.objects.get(number=room_number)
                room.is_available = True
                room.save()
                
                # Remove from reservation history
                for i, res in enumerate(reservation_history):
                    if res.name == name and str(res.room_number) == room_number:
                        reservation_history.pop(i)
                        break
                
                # Check waiting list
                if waiting_list:
                    next_guest = waiting_list.popleft()
                    if next_guest.bedrooms == found_reservation.bedrooms:
                        next_guest.room_number = room_number
                        next_guest.floor = room.floor
                        current_reservations.append(next_guest)
                        reservation_history.append(next_guest)
                        room.is_available = False
                        room.save()
                
                return redirect('checkedout')
            else:
                return render(request, 'checkout.html', {'error': 'Reservation not found'})
                
        except Exception as e:
            print(f"Checkout error: {str(e)}")
            return render(request, 'checkout.html', {'error': 'An error occurred during checkout'})
            
    return render(request, 'checkout.html')

def checkreservation(request):
    reservation = None
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        
        # Search through the queue
        temp_queue = deque()
        
        while current_reservations:
            res = current_reservations.popleft()
            if res.name == name and res.contact == contact:
                reservation = res
            temp_queue.append(res)
            
        # Restore the queue
        while temp_queue:
            current_reservations.append(temp_queue.popleft())

    return render(request, 'checkreservation.html', {'reservation': reservation})

def checkedout(request):
    return render(request, 'finalcheckout.html')

def contact(request):
    return render(request, 'contact.html')