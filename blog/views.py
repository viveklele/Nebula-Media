from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Post
from users.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required

def post_list(request):
	all_posts = Post.objects.all().order_by('-date_posted')
	paginator = Paginator(all_posts, 5)
	page_number = request.GET.get('page')
	final_page = paginator.get_page(page_number)
	context = {
		"posts" : final_page
	}	
	return render(request, 'blog/home.html', context)

# class UserPostListView(ListView):
# 	model = Post
# 	template_name = 'blog/user_posts.html' # '<app>/<model>_<viewtype>.html'
# 	context_object_name = 'posts'
# 	paginate_by = 5
	
# 	def get_queryset(self):
# 		user = get_object_or_404(User, username=self.kwargs.get('username'))
# 		return Post.objects.filter(author=user).order_by('date_posted')
		
def user_post_list(request, username):
	user = User.objects.get(username=username)
	post = Post.objects.filter(author=user).order_by('-date_posted')
	# Pagination 	
	paginator = Paginator(post, 5)
	page_number = request.GET.get('page')
	final_page = paginator.get_page(page_number)
	context={
		"posts": final_page
	}	
	return render(request, "blog/user_posts.html", context)

def post_detail_view(request, pk):
	data = get_object_or_404(Post, pk=pk)
	context = {
		"post" : data
	}
	
	return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')	
		content = request.POST.get('content')
		blog_image = request.FILES['blog_image']	
		audio = request.FILES['audio']
		video = request.FILES['video']
		keywords = request.POST.get('keywords')
		form = Post(title=title, content=content, blog_image=blog_image, audio=audio, video=video, keywords=keywords)
		form.author = request.user
		form.save()

		return redirect('blog-home')
	return render(request, "blog/post_create.html")
		

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
	model = Post
	fields = ['title', 'content', 'blog_image', 'audio', 'video', 'keywords']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def grid_view(request):
	posts = Post.objects.all().order_by('-date_posted')
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	final_page = paginator.get_page(page_number)
	context = {
		"posts" : final_page
	}	
	return render(request, 'blog/gridview.html', context)

# return search query

def search(request):
	query = request.GET['query']

	if len(query) > 20:
		allPosts = Post.objects.none()
		user = Profile.objects.none()
	else:
		allPosts = Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | 
		Q(keywords__icontains=query))

	paras = {
		'allPosts': allPosts, 'query': query
	}
	
	return render(request, 'blog/search.html', paras)

# show suggetions in search bar

# def search_address(request):
# 	title = request.GET.get('title')
# 	payload = []
# 	if title:
# 		fake_address_objs = Post.objects.filter(Q(author__username__icontains=title))
# 		# fake_address_objs = Post.objects.filter(Q(author__username__icontains=title) | Q(title__icontains=title) |
#  		# Q(keywords__icontains=title))

# 		for fake_address_obj in fake_address_objs:
# 			payload.append(fake_address_obj.title)
	
# 	return JsonResponse({
# 		'status': 200,
# 		'data': payload
# 	})