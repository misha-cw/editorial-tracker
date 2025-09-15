from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Newspaper, Topic, Redactor

def index(request):

    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()
    num_redactors = Redactor.objects.count()

    context = {
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_redactors": num_redactors,
    }

    return render(request, "catalog/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    template_name = "catalog/topic_list.html"
    context_object_name = "topics"
    paginate_by = 15
    