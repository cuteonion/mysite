from django.test import TestCase
import datetime
from polls.models import Poll
from django.utils import timezone
from django.core.urlresolvers import reverse

class PollMethodTests(TestCase):
	def test_was_published_recently_with_future_poll(self):
		future_poll=Poll(pub_date=timezone.now()+datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(),False)
	def test_was_published_recently_with_old_poll(self):
		old_poll=Poll(pub_date=timezone.now()-datetime.timedelta(days=30))
		self.assertEqual(old_poll.was_published_recently(),False)
	def test_was_published_recently_with_recent_poll(self):
		recent_poll=Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(),True)
def create_poll(question,days):
	return Poll.objects.create(question=question,pub_date=timezone.now()+datetime.timedelta(days=days))

class PollIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_poll(self):
		future_poll=create_poll(question='asdfghjk',days=5)
		response=self.client.get(reverse('polls:detail',args=(future_poll.id,)))
		self.assertEqual(response.status_code,404)
	def test_detail_view_with_a_past_poll(self):
		past_poll=create_poll(question='past__pollllll',days=-30)
		response=self.client.get(reverse('polls:detail',args=(past_poll.id,)))
		self.assertContains(response,past_poll.question,status_code=200)
