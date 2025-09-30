from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from catalog.models import Newspaper, Topic, Redactor
from catalog.forms import RedactorCreateForm , RedactorUpdateForm, NewspaperForm

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
    ordering = ["name"]


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = ["name"]
    template_name = "catalog/topic_form.html"
    success_url = reverse_lazy("catalog:topic-list")


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = ["name"]
    template_name = "catalog/topic_form.html"
    success_url = reverse_lazy("catalog:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    template_name = "catalog/topic_confirm_delete.html"
    success_url = reverse_lazy("catalog:topic-list")


class RedactorListView(generic.ListView):
    model = Redactor
    template_name = "catalog/redactor_list.html"
    context_object_name = "redactors"
    paginate_by = 15
    ordering = ["username"]


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreateForm
    template_name = "catalog/redactor_form.html"
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    template_name = "catalog/redactor_form.html"
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    template_name = "catalog/redactor_confirm_delete.html"
    success_url = reverse_lazy("catalog:redactor-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "catalog/newspaper_list.html"
    context_object_name = "newspapers"
    paginate_by = 9
    ordering = ["-published_date"]


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    template_name = "catalog/newspaper_detail.html"
    context_object_name = "newspaper"


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "catalog/newspaper_form.html"
    success_url = reverse_lazy("catalog:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "catalog/newspaper_form.html"
    success_url = reverse_lazy("catalog:newspaper-list")


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    template_name = "catalog/newspaper_confirm_delete.html"
    success_url = reverse_lazy("catalog:newspaper-list")
    