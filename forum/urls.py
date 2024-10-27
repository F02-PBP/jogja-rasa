from django.urls import path
from forum.views import forum_home, topic_detail, add_topic, add_comment, edit_comment, edit_topic, delete_topic, delete_comment
from forum.views import show_user_comments_json, show_user_topics_json, fetch_new_comments, fetch_new_topics

app_name = 'forum'

urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('topic/add/', add_topic, name='add_topic'),
    path('topic/<int:topic_id>/comment/', add_comment, name='add_comment'),
    path('topic/<int:topic_id>/edit/', edit_topic, name='edit_topic'),
    path('topic/<int:topic_id>/delete/', delete_topic, name='delete_topic'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('json/user/topics/', show_user_topics_json, name='user_topics_json'),
    path('json/user/comments/', show_user_comments_json, name='user_comments_json'),
    path('api/fetch_new_topics/<str:last_timestamp>/', fetch_new_topics, name='fetch_new_topics'),
    path('api/fetch_new_comments/<int:topic_id>/<str:last_timestamp>/', fetch_new_comments, name='fetch_new_comments'),
]
