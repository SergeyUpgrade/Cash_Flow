from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecordListView.as_view(), name='index'),
    path('record/create/', views.record_create, name='record_create'),
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('reference/', views.reference_management, name='reference_management'),
    path('status/<int:pk>/delete/', views.delete_status, name='delete_status'),
    path('type/<int:pk>/delete/', views.delete_type, name='delete_type'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('subcategory/<int:pk>/delete/', views.delete_subcategory, name='delete_subcategory'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]