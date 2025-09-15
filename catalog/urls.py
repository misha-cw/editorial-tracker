from django.urls import path
from .views import (
    index,
    TopicListView,
)

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),  # Home page
    path("topics/", TopicListView.as_view(), name="topic-list"),  # Topics list
]
