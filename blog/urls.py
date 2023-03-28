from django.urls import path
from .views import *

urlpatterns = [
    path('post/<int:pk>', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', post_list, name='index'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path('category/<int:category_id>/', post_list_by_category, name='post_list_by_category'),
]
