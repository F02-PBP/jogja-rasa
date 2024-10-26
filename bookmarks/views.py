from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Bookmark
from restaurants.models import Restaurant

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'bookmarks/bookmark_list.html', {'bookmarks': bookmarks})

@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, restaurant=restaurant)
        
        if not created:
            # Bookmark sudah ada, jadi hapus
            bookmark.delete()
            is_bookmarked = False
        else:
            # Bookmark baru dibuat
            is_bookmarked = True

        return JsonResponse({'is_bookmarked': is_bookmarked})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
