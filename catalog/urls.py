from django.urls import path
from .views import (
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    RedactorListView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
)

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),  # Home page
    path("topics/", TopicListView.as_view(), name="topic-list"),  # Topics list
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),  # Create new topic
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),  # Update topic
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),  # Delete topic
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),  # Redactors list
    path("redactors/create/", RedactorCreateView.as_view(), name="redactor-create"),  # Create new redactor
    path("redactors/<int:pk>/update/", RedactorUpdateView.as_view(), name="redactor-update"),  # Update redactor
    path("redactors/<int:pk>/delete/", RedactorDeleteView.as_view(), name="redactor-delete"),  # Delete redactor
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),  # Newspapers list
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),  # Newspaper detail
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),  # Create new newspaper
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),  # Update newspaper
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),  # Delete newspaper
]
