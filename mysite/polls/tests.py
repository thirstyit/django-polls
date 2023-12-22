import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Past question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

class QuestionDetailsViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text='Future question: ', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response =self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question: ', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response =self.client.get(url)
        self.assertContains(response, past_question.question_text)

    # def test_no_question(self):
    #     response = self.client.get(reverse('polls:detail'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "No polls are available.")
    #     self.assertQuerysetEqual(response.context['latest_question_list'], [])

