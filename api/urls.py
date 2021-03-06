from django.urls import path, include
from . import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', views.user_register, name="register"),
    path('users/verification', views.user_verification, name="verification"),
    path('authorization', views.user_login, name="user-login"),
    path('users/details', views.user_details, name="public-user-detail"),
    path('users/password', views.user_password, name="user-detail-password"),
    path('navigations', views.navigations, name="navigations"),
    path('navigations/stalls/<int:stallID>', views.navigations_stall, name="navigations-stall"),
    path('canteens/<int:canteenID>', views.canteens, name="canteens"),
    path('stalls', views.recommendstall, name="recommend-stalls"),
    path('stalls/<int:stallID>', views.stalls, name="stalls"),
    path('reviews', views.reviews, name="review"),
    path('reviews/<int:reviewID>', views.deletereviews, name="delete-review"),
    path('reviews/like/<int:reviewID>', views.reviewslike, name="review-like"),
    path('dishes/<int:dishID>', views.dishes, name="dishes"),
    path('dishes', views.recommenddish, name="recommend-dishes"),
    path('notice', views.getnotice, name='get-notice'),
]