from django.urls import path
from . import views

urlpatterns = [
	path('', views.post_list, name='blog-home'),
	path('user/<str:username>/', views.user_post_list, name='user-posts'),
	path('post/<int:pk>/', views.post_detail_view, name='post-detail'),
	path('post/<int:pk>/update/', views.post_update, name='post-update'),
	path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
	path('about/', views.about, name='blog-about'),
	path('grid_view/', views.grid_view, name='blog-grid_view'),
	path('post/new/', views.post_create, name='post-create'),
	path('search/', views.search, name='search'),
	path('autosuggest/', views.autosuggest, name='autosuggest'),

]