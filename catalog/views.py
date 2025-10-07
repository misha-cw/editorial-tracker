from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from catalog.models import Newspaper, Topic, Redactor
from catalog.forms import (
    RedactorCreateForm,
    RedactorUpdateForm, 
    NewspaperForm,
    NewspaperTitleSearchForm,
    RedactorUsernameSearchForm,
    TopicNameSearchForm,
)

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

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("name", "")
        context["search_form"] = TopicNameSearchForm(
            initial={"name": model}
        )
        return context
    
    def get_queryset(self):
        queryset = Topic.objects.all().order_by("name")
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("username", "")
        context["search_form"] = RedactorUsernameSearchForm(
            initial={"username": model}
        )
        return context
    
    def get_queryset(self):
        queryset = Redactor.objects.all().order_by("username")
        username = self.request.GET.get("username", "")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

class RedactorDetailView(generic.DetailView):
    model = Redactor
    template_name = "catalog/redactor_detail.html"
    context_object_name = "redactor"


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

    def get_context_data(self, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("title", "")
        context["search_form"] = NewspaperTitleSearchForm(
            initial={"title": model}
        )
        return context
    
    def get_queryset(self):
        queryset = Newspaper.objects.all().prefetch_related("topics", "publishers").order_by("-published_date")
        title = self.request.GET.get("title", "")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


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
    