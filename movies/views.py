from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from movies.utils import notify_seat_change


def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
    return render(request,'movies/movie_list.html',{'movies':movies})

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_Seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theaters, 'seats': seats,
                'error': "No seat selected"
            })
        successful = []
        for seat_id in selected_Seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked = True
                seat.save()
                successful.append({'id': seat.id, 'is_booked': True})
            except IntegrityError:
                error_seats.append(seat.seat_number)

        # Notify clients about booked seats
        if successful:
            notify_seat_change(theaters.id, successful)

        if error_seats:
            return render(request, 'movies/seat_selection.html', {
                'theater': theaters, 'seats': seats,
                'error': f"These seats were already booked: {', '.join(error_seats)}"
            })

        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {
        'theater': theaters, 'seats': seats
    })
