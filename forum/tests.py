from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Comment
from django.utils import timezone
from django.core.exceptions import PermissionDenied
import json

class ForumTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test topic",
            author=self.user1,
            created_at=timezone.now()
        )
        self.comment = Comment.objects.create(
            topic=self.topic,
            comment="This is a test comment",
            author=self.user1,
            created_at=timezone.now()
        )

    def test_forum_home(self):
        response = self.client.get(reverse('forum:forum_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_home.html')

    def test_topic_detail_get(self):
        response = self.client.get(reverse('forum:topic_detail', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_detail.html')

    def test_topic_detail_post_comment(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:topic_detail', args=[self.topic.id]), {
            'comment': 'New test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(comment="New test comment").exists())

    def test_add_topic_get(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse('forum:add_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/add_topic.html')

    def test_add_topic_post(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:add_topic'), {
            'title': 'Another Test Topic',
            'description': 'Description of test topic'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(title="Another Test Topic").exists())

    def test_edit_topic(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:edit_topic', args=[self.topic.id]), {
            'title': 'Updated Topic Title',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, "Updated Topic Title")

    def test_delete_topic(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:delete_topic', args=[self.topic.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())

    def test_edit_comment(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:edit_comment', args=[self.comment.id]), {
            'comment': 'Updated Comment Text'
        })
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment, "Updated Comment Text")

    def test_delete_comment(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse('forum:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_show_user_topics_json(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse('forum:user_topics_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_show_user_comments_json(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse('forum:user_comments_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_fetch_new_topics(self):
        self.client.login(username="user1", password="password")
        timestamp = timezone.now().timestamp() - 60  # 1 minute ago
        response = self.client.get(reverse('forum:fetch_new_topics', args=[timestamp]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) >= 1)  # Should return at least the existing topic

    def test_fetch_new_comments(self):
        self.client.login(username="user1", password="password")
        timestamp = timezone.now().timestamp() - 60  # 1 minute ago
        response = self.client.get(reverse('forum:fetch_new_comments', args=[self.topic.id, timestamp]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) >= 1)  # Should return at least the existing comment
