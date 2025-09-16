from django.urls import path
from .views import (
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
)

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),  # Home page
    path("topics/", TopicListView.as_view(), name="topic-list"),  # Topics list
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),  # Create new topic
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),  # Update topic
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),  # Delete topic
]
