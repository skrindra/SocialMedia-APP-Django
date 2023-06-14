from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post
from users.models import Profile
# Create your views here.

@login_required
def post_create(request):
    if request.method=="POST":
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            print("Post created successfully")  # Debug statement
    else:
        form = PostCreateForm()
    return render(request,'posts/create.html',{'form':form})


def feed(request):
    if request.method=="POST":
        comment_form = CommentForm(request.POST)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        new_comment = comment_form.save(commit=False)
        commented_by = request.user
        
        # link the post to the new comment
        new_comment.post = post
        new_comment.user = commented_by
        new_comment.save()

    else:
        comment_form = CommentForm()

    posts = Post.objects.all()
    logged_user = request.user
    return render(request,'posts/feed.html',
                  {'posts':posts,'logged_user':logged_user, 'comment_form': comment_form})



def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,id=post_id)
    # if the user has already liked the post (unlike the post)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('feed')

