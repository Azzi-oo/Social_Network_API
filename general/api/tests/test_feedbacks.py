from rest_framework.test import APITestCase
from general.factories import FeedbackFactory
from general.api.serializers import FeedbackSerializer
from general.models import Feedback
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class FeedbackTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_feedback_serializer(self):
        feedback = FeedbackFactory()

        serializer = FeedbackSerializer(feedback)

        self.assertEqual(serializer.data['user'], feedback.user.id)
        self.assertEqual(serializer.data['message'], feedback.message)

    def test_create_feedback(self):
        feedback_data = FeedbackFactory.build()

        response = self.client.post(reverse('feedback'), data=feedback_data.__dict__)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        feedback_exists = Feedback.objects.filter(id=response.data['id']).exists()
        self.assertTrue(feedback_exists)
