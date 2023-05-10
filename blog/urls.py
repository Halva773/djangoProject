from django.urls import path

from .views import *

urlpatterns = [
    path('post/<int:pk>', BlogDetailView.as_view(), name='post_detail'),
    path('about/', aboutPageView, name='about'),
    path('', post_list, name='index'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path('category/<int:category_id>/', post_list_by_category, name='post_list_by_category'),
    path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginUserForm),
         name='login'),
    path('profile', profile_view, name="profile"),
    path('register', RegisterUser.as_view(), name='registration'),
    path("signup/", signup, name="signup"),
]
