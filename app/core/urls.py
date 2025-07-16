from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home/Dashboard
    path('', views.home, name='home'),
    
    # Book URLs
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    
    # Branch URLs
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/add/', views.branch_create, name='branch_create'),
    path('branches/<int:branch_id>/', views.branch_detail, name='branch_detail'),
    path('branches/<int:branch_id>/edit/', views.branch_edit, name='branch_edit'),
    path('branches/<int:branch_id>/delete/', views.branch_delete, name='branch_delete'),
    
    
    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:inventory_id>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:inventory_id>/delete/', views.inventory_delete, name='inventory_delete'),
    path('inventory/branch/<int:branch_id>/', views.inventory_by_branch, name='inventory_by_branch'),
]
