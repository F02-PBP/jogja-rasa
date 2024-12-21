from django.urls import path
from forum.views import add_comment_flutter, add_topic_flutter, forum_home, get_user_name, get_user_name_by_id, show_all_topics_json, topic_detail, add_topic, add_comment, edit_comment, edit_topic, delete_topic, delete_comment, edit_topic_flutter, delete_topic_flutter, edit_comment_flutter, delete_comment_flutter, get_topic_comments_json
from forum.views import show_user_comments_json, show_user_topics_json, fetch_new_comments, fetch_new_topics

app_name = 'forum'

urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('get-user-name/', get_user_name, name='get_user_name'),
    path('get-user-name-by-id/<int:user_id>/', get_user_name_by_id, name='get_user_name_by_id'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('topic/add/', add_topic, name='add_topic'),
    path('topic/add-flutter/', add_topic_flutter, name='add_topic_flutter'),
    path('topic/add-comment-flutter/', add_comment_flutter, name='add_comment_flutter'),
    path('topic/<int:topic_id>/comment/', add_comment, name='add_comment'),
    path('topic/<int:topic_id>/edit/', edit_topic, name='edit_topic'),
    path('topic/<int:topic_id>/delete/', delete_topic, name='delete_topic'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('json/user/topics/', show_user_topics_json, name='user_topics_json'),
    path('json/user/comments/', show_user_comments_json, name='user_comments_json'),
    path('json/all/topics/', show_all_topics_json, name='all_topics_json'),
    path('api/fetch_new_topics/<str:last_timestamp>/', fetch_new_topics, name='fetch_new_topics'),
    path('api/fetch_new_comments/<int:topic_id>/<str:last_timestamp>/', fetch_new_comments, name='fetch_new_comments'),
    path('topic/<int:topic_id>/edit-flutter/', edit_topic_flutter, name='edit_topic_flutter'),
    path('topic/<int:topic_id>/delete-flutter/', delete_topic_flutter, name='delete_topic_flutter'),
    path('comment/<int:id>/edit-flutter/', edit_comment_flutter, name='edit_comment_flutter'),
    path('comment/<int:id>/delete-flutter/', delete_comment_flutter, name='delete_comment_flutter'),
    path('json/topic/<int:topic_id>/comments/', get_topic_comments_json, name='topic_comments_json'),
]
