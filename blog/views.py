from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Media
from users.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from os import remove

def post_list(request):
	all_posts = Post.objects.all().order_by('-date_posted')
	paginator = Paginator(all_posts, 5)
	page_number = request.GET.get('page')
	final_page = paginator.get_page(page_number)
	context = {
		"posts" : final_page
	}	
	return render(request, 'blog/home.html', context)
		
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
	posts = get_object_or_404(Post, pk=pk)
	media = Media.objects.filter(post=posts)
	context = {
		"post" : posts,
		"images" : media
	}
	
	return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')	
		content = request.POST.get('content')
		audio = request.FILES['audio']
		video = request.FILES['video']
		keywords = request.POST.get('keywords')
		form = Post(title=title, content=content, audio=audio, video=video, keywords=keywords, author=request.user)
		form.save()
		for image in request.FILES.getlist('blog_image'):
			media = Media.objects.create(post=form, blog_image=image)
			media.save()
		return redirect('blog-home')
	return render(request, "blog/post_create.html")
	
@login_required
def post_update(request, pk):
	form = get_object_or_404(Post, pk=pk)
	media = Media.objects.filter(post=pk)
	if request.method == 'POST':
		form.title = request.POST.get('title')
		form.content = request.POST.get('content')

		if 'audio' in request.FILES:
			form.audio = request.FILES['audio']
		
		if 'video' in request.FILES:
			form.video = request.FILES['video']

		form.keywords = request.POST.get('keywords')
		form.author=request.user
		form.save()
		if 'blog_image' in request.FILES:
			for image in media:
				storage, path = image.blog_image.storage, image.blog_image.path
				storage.delete(path)
				image.delete()
			for image in request.FILES.getlist('blog_image'):
				new_media = Media(post=form, blog_image=image)
				new_media.save()

		messages.success(request, "Your Post update sucessfully!")
		return redirect('/')
	context = {
		'form': form,
		'images': media
	}
	return render(request, 'blog/post_update.html', context)

@login_required
def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	media = Media.objects.filter(post=pk)
	context= {'post': post}
	if request.method == 'POST':
		# To delete media files from server
		for image in media:
			if image.blog_image:
				storage, path = image.blog_image.storage, image.blog_image.path
				storage.delete(path)
				image.delete()
			
		if post.audio:
			storage, path = post.audio.storage, post.audio.path
			storage.delete(path)
		if post.video:
			storage, path = post.video.storage, post.video.path
			storage.delete(path)
		post.delete()	
		return HttpResponseRedirect('/')
	return render(request, 'blog/post_delete.html', context)

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

def search(request):
	query = request.GET['query']

	if len(query) > 20:
		allPosts = Post.objects.none()
		user = Profile.objects.none()
	else:
		allPosts = Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | 
		Q(keywords__icontains=query)).order_by('-date_posted')

	paras = {
		'allPosts': allPosts, 'query': query
	}
	return render(request, 'blog/search.html', paras)

