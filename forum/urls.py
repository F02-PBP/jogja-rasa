from django.urls import path
from forum.views import forum_home, topic_detail, add_topic, add_comment

app_name = 'forum'

urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('topic/add/', add_topic, name='add_topic'),
    path('topic/<int:topic_id>/comment/', add_comment, name='add_comment'),
]
