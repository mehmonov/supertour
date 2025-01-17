from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime
from .models import TourPackage, Destination
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import TourPackage, Booking
from django.db.models import Count
from django.http import JsonResponse
def home(request):
    return render(request, "index.html")

def result(request):
    return render(request, "searchresult.html")
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import TourPackage, Destination

def search(request):
    if request.method != 'POST':
        return render(request, 'search.html')

    destination = request.POST.get('destination', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    travelers = request.POST.get('travelers', '')

    query = TourPackage.objects.all()
    exact_matches = []
    similar_matches = []

    try:
        travelers_count = int(travelers) if travelers else None
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None

        if destination:
            query = query.filter(destination__name__iexact=destination)
        if start_date_obj:
            query = query.filter(start_date__gte=start_date_obj)
        if end_date_obj:
            query = query.filter(end_date__lte=end_date_obj)
        if travelers_count:
            query = query.filter(max_people__gte=travelers_count)

        exact_matches = query.distinct()[:5]

        if len(exact_matches) < 5:
            similar_query = TourPackage.objects.exclude(
                id__in=[m.id for m in exact_matches]
            )

            if destination:
                similar_query = similar_query.filter(
                    Q(destination__name__icontains=destination) |
                    Q(name__icontains=destination)
                )
            
            if start_date_obj:
                date_range_start = start_date_obj - timedelta(days=5)
                date_range_end = start_date_obj + timedelta(days=5)
                similar_query = similar_query.filter(
                    start_date__range=[date_range_start, date_range_end]
                )

            if travelers_count:
                min_travelers = max(1, travelers_count - 2)
                max_travelers = travelers_count + 2
                similar_query = similar_query.filter(
                    max_people__range=[min_travelers, max_travelers]
                )

            similar_matches = similar_query.distinct()[:5]

    except (ValueError, TypeError) as e:
        print(f"Error in search: {e}")

    context = { 
        'exact_matches': exact_matches,
        'similar_matches': similar_matches,
        'search_params': {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'travelers': travelers,
            
        }
    }
    print(context)
    return render(request, 'searchresult.html', context)


from .models import Destination
def destination_autocomplete(request):
    query = request.GET.get('query', '')
    if len(query) >= 2:  
        destinations = Destination.objects.filter(
            Q(name__icontains=query)
        ).values('name', 'description')[:5]  
        return JsonResponse(list(destinations), safe=False)
    print(query)
    return JsonResponse([], safe=False)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TourPackage, Booking

def book_tour(request, id):
    # Handle GET request - show booking form
    if request.method == 'GET':
        tour_id = id
        if not tour_id:
            messages.error(request, "Tur ID si ko'rsatilmagan")
            return redirect('home')
            
        tour_package = get_object_or_404(TourPackage, id=tour_id)
        
        # Check if tour is already fully booked
        current_bookings = Booking.objects.filter(
            tour_package=tour_package,
            status='CONFIRMED'
        ).count()
        
        context = {
            'tour': tour_package,
            'is_available': current_bookings < tour_package.max_people
        }
        print(context)
        return render(request, 'book-tour.html', context)
    
    # Handle POST request - process booking
    elif request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        full_name = request.POST.get('fullname')
        phone = request.POST.get('phone')
        note = request.POST.get('note')
        
        # Validate required fields
        if not all([tour_id, full_name, phone]):
            messages.error(request, "Barcha maydonlarni to'ldiring")
            return redirect('book_tour')
        
        try:
            tour_package = get_object_or_404(TourPackage, id=tour_id)
            
            # Check tour availability
            current_bookings = Booking.objects.filter(
                tour_package=tour_package,
                status='CONFIRMED'
            ).count()
            
            if current_bookings >= tour_package.max_people:
                messages.error(request, "Kechirasiz, bu tur to'liq band qilingan")
                return redirect('tours_list')
            
            # Create booking
            booking = Booking.objects.create(
                tour_package=tour_package,
                first_name=full_name,
                phone_number=phone,
                notes=note,
                status='PENDING'
            )
            
            messages.success(request, "Buyurtmangiz qabul qilindi. Tez orada siz bilan bog'lanamiz")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, "Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring")
            return redirect('home')