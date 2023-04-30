from django.urls import path
from .views import PostDeleteView #PostUpdateView #UserPostListView #,PostCreateView PostDetailView, PostListView
from . import views

urlpatterns = [
	# path('', PostListView.as_view(), name='blog-home'),
	path('', views.post_list, name='blog-home'),
	# path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
	path('user/<str:username>/', views.user_post_list, name='user-posts'),
	# path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/<int:pk>/', views.post_detail_view, name='post-detail'),
	# path('postform/', PostCreateView.as_view(), name='post-create'),
	# path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/update/', views.post_update, name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('about/', views.about, name='blog-about'),
	path('grid_view/', views.grid_view, name='blog-grid_view'),
	# path('Grid_view/', PostGridView.as_view(), name='blog-grid'),
	path('search/', views.search, name='search'),
	# path('post_create_title', views.post_create_title, name='create-post')
	path('post/new/', views.post_create, name='post-create')
	# path('search/', views.search_address, name='search')  # for suggetions in search bar
	
	
]