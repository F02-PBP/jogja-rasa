from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Comment
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, CommentForm
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone


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
            comment.created_at = timezone.now()
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
            topic.created_at = timezone.now()
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
            comment.created_at = timezone.now()
            comment.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = CommentForm()
    return render(request, 'forum/add_comment.html', {'form': form, 'topic': topic})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('forum:topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'forum/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        raise PermissionDenied

    topic.delete()
    return redirect('forum:forum_home')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum:topic_detail', topic_id=comment.topic.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        raise PermissionDenied

    topic_id = comment.topic.id
    comment.delete()
    return redirect('forum:topic_detail', topic_id=topic_id)


def show_user_topics_json(request):
    # Filter topics created by the logged-in user
    data = Topic.objects.filter(author=request.user)
    # Return data serialized as JSON
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_user_comments_json(request):
    # Filter comments created by the logged-in user
    data = Comment.objects.filter(author=request.user)
    # Return data serialized as JSON
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fetch new topics created after a given timestamp
def fetch_new_topics(request, last_timestamp):
    last_timestamp = timezone.make_aware(timezone.datetime.fromtimestamp(float(last_timestamp)))
    topics = Topic.objects.filter(created_at__gt=last_timestamp).order_by('-created_at')
    data = serializers.serialize("json", topics)
    return JsonResponse(data, safe=False)

# Fetch new comments for a specific topic after a given timestamp
def fetch_new_comments(request, topic_id, last_timestamp):
    last_timestamp = timezone.datetime.fromtimestamp(float(last_timestamp))
    topic = Topic.objects.get(id=topic_id)
    comments = topic.comments.filter(created_at__gt=last_timestamp).order_by('-created_at')
    data = serializers.serialize("json", comments)
    return JsonResponse(data, safe=False)
