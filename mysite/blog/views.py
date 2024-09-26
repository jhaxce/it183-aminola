# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from .models import Post

# # Create your views here.

# def blog_list(request):
#     post = Post.objects.all()
#     context = {
#         'blog_list': post
#     }
#     return render(request, 'blog/blog_list.html', context)

# def blog_detail(request, id):
#     each_post = Post.objects.get(id=id)
#     context = {
#         'blog_detail': each_post
#     }
#     return render(request, 'blog/blog_detail.html', context)

# def blog_delete(request, id):
#     each_post = Post.objects.get(id=id)
#     each_post.delete()
#     return HttpResponseRedirect('/posts/')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def blog_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/blog_form.html', {'form': form})

def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form})

def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})
