from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Poll,Choice
from django.utils import timezone
class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_poll_list'

	def get_queryset(self):
		"""return latest five published polls"""
		return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
	model=Poll
	template_name='polls/detail.html'
	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())
class ResultView(generic.DetailView):
	model=Poll
	template_name='polls/result.html'


def vote(request,poll_id):
	p=get_object_or_404(Poll,pk=poll_id)
	try :
		select_choice=p.choice_set.get(pk=request.POST['choice'])
	except(KeyError,Choice.DoesNotExsit):
		return render(request,'polls/detail.html',{'poll':p,'error_message':"You didn\'t select a choice.",})
	else:
		select_choice.votes+=1
		select_choice.save()
		return HttpResponseRedirect(reverse("polls:results",args=(p.id,)))

