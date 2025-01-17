from django.urls import path

from .views import home, result, search, destination_autocomplete, book_tour

urlpatterns = [
    path("", home, name="home"),
    path("result/", result, name="result"),
    path("search/", search, name="search"),
    path('destination-autocomplete/', destination_autocomplete, name='destination-autocomplete'),
        path('book-tour/<int:id>', book_tour, name='book-tour')
]
