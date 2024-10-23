from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Comment
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, CommentForm

def forum_home(request):
    topics = Topic.objects.all()
    return render(request, 'forum/forum_home.html', {'topics': topics})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = topic.comments.all()  # fetch related comments
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user  # set the comment author to the logged-in user
            comment.save()
            return redirect('forum:topic_detail', topic_id=topic_id)

    return render(request, 'forum/topic_detail.html', {'topic': topic, 'comments': comments, 'form': form})

@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum:forum_home')
    else:
        form = TopicForm()
    return render(request, 'forum/add_topic.html', {'form': form})

@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = CommentForm()
    return render(request, 'forum/add_comment.html', {'form': form, 'topic': topic})
