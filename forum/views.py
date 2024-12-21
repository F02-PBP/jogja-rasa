import json
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

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
@csrf_exempt
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
            return redirect('forum:topic_detail', topic_id=topic_id)
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

def show_all_topics_json(request):
    data = Topic.objects.all()
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

@csrf_exempt
def add_topic_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        topic = Topic(title=title, description=description, author=request.user)
        topic.save()
        return JsonResponse({'status': 'success', 'message': 'Topik berhasil dibuat'}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, safe=False)

@csrf_exempt
def add_comment_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic_id = data['topic_id']
        comment = data['comment']
        comment = Comment(topic_id=topic_id, comment=comment, author=request.user)
        comment.save()
        return JsonResponse({'status': 'success', 'message': 'Komentar berhasil ditambahkan'}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, safe=False)

def get_user_name(request):
    return JsonResponse({'username': request.user.username}, safe=False)

def get_user_name_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'username': user.username}, safe=False)

@csrf_exempt
def edit_topic_flutter(request, topic_id):
    if request.method == 'POST':
        try:
            topic = get_object_or_404(Topic, pk=topic_id)
            # Check if user is the author
            if request.user != topic.author:
                return JsonResponse({
                    "status": "error",
                    "message": "You can only edit your own topics"
                }, status=403)
                
            data = json.loads(request.body)
            topic.title = data['title']
            topic.description = data['description']
            topic.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Topic updated successfully!"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

@csrf_exempt
def delete_topic_flutter(request, topic_id):
    try:
        topic = get_object_or_404(Topic, pk=topic_id)
        # Check if user is the author
        if request.user != topic.author:
            return JsonResponse({
                "status": "error",
                "message": "You can only delete your own topics"
            }, status=403)
            
        topic.delete()
        return JsonResponse({
            "status": "success",
            "message": "Topic deleted successfully!"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

@csrf_exempt
def edit_comment_flutter(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment = Comment.objects.get(pk=id)
            if request.user.id == comment.author.id:
                comment.comment = data['comment']
                comment.save()
                return JsonResponse({"status": "success"})
            return JsonResponse({"status": "error", "message": "Unauthorized"})
        except Comment.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Comment not found"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def delete_comment_flutter(request, id):
    try:
        comment = Comment.objects.get(pk=id)
        if request.user.id == comment.author.id:
            comment.delete()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Unauthorized"})
    except Comment.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Comment not found"})

def get_topic_comments_json(request, topic_id):
    # Filter comments untuk topic tertentu
    topic = get_object_or_404(Topic, pk=topic_id)
    data = Comment.objects.filter(topic=topic)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")