from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register_request, name="register"),
    path('', views.home, name = "home"),
    path('list_items/', views.list_items, name = "list_items"),
    path('add_items/', views.add_items, name = "add_item"),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name = "delete_items" ),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path ('issue_items/<str:pk>/', views.issue_items, name = "issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name = "receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('list_history/', views.list_history, name = "list_history"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name= "logout"),
]

