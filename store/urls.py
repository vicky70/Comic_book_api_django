from django.urls import path
from . import views

urlpatterns = [
    path('api/listComics', views.getAllComics, name='AllComics'),
    path('api/comic_details/<int:pk_id>/', views.getOneComic, name='Comic_datials'),
    path('api/getCartItems/', views.getCartItems, name='cartItems'),
    path('api/addToCart/<int:comicID>/', views.addToCart, name='addToCart'),
    path('api/updateReview/<int:comicID>/', views.updateReview, name='updateReview'),
    
    # paypal payment paths
    path('api/create_payment/', views.create_payment, name='create_payment'),
    path('api/execute_payment/', views.execute_payment, name='execute_payment'),
    path('api/execute_success_payment/', views.execute_success_payment, name='execute_success_payment'),

    # review urls 
    path('api/comic_reviews/<int:comic_id>/', views.PostUserReview, name='Review'),


    # path('api/add_Comics', views.addProducts, name='addProducts'),
    # path('api/signup', views.user_singup, name='singup'),
    path('api/login/', views.user_login, name='login'),
]
