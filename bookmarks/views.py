from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Bookmark
from restaurants.models import Restaurant
import json
import uuid
from django.db import IntegrityError


def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmarks/bookmark_list.html', {'bookmarks': bookmarks})

@login_required
@require_POST
def toggle_bookmark(request):
    try:
        restaurant_id = request.POST.get('restaurant_id')
        
        if not restaurant_id and request.body:
            try:
                data = json.loads(request.body)
                restaurant_id = data.get('restaurant_id')
            except json.JSONDecodeError:
                return JsonResponse({
                    'error': 'Invalid JSON data'
                }, status=400)
        
        if not restaurant_id:
            return JsonResponse({
                'error': 'No restaurant ID provided.'
            }, status=400)

        try:
            if not isinstance(restaurant_id, uuid.UUID):
                restaurant_id = uuid.UUID(str(restaurant_id))
        except ValueError:
            return JsonResponse({
                'error': 'Invalid restaurant ID format'
            }, status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({
                'error': 'Restaurant not found'
            }, status=404)

        try:
            bookmark = Bookmark.objects.get(
                user=request.user,
                restaurant=restaurant
            )
            bookmark.delete()
            is_bookmarked = False
            message = 'Bookmark removed successfully'
        except Bookmark.DoesNotExist:
            try:
                bookmark = Bookmark.objects.create(
                    id=uuid.uuid4(),
                    user=request.user,
                    restaurant=restaurant
                )
                is_bookmarked = True
                message = 'Restaurant bookmarked successfully'
            except IntegrityError:
                return JsonResponse({
                    'error': 'Bookmark already exists'
                }, status=400)

        return JsonResponse({
            'success': True,
            'is_bookmarked': is_bookmarked,
            'message': message,
            'bookmark_id': str(bookmark.id) if is_bookmarked else None
        })

    except Exception as e:
        print(f"Error in toggle_bookmark: {str(e)}")
        return JsonResponse({
            'error': str(e)
        }, status=500)