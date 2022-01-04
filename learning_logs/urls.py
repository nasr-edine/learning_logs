
from django.contrib import admin
from django.urls import path
from .views import IndexView, TopicListView, TopicDetailView, TopicCreateView, TopicDeleteView, TopicUpdateView, EntryUpdateView, EntryDeleteView, EntryCreateView, upload_csv

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path("", IndexView.as_view(), name="index"),

    # Show all topics.
    path('topics/', TopicListView.as_view(), name='topics'),

    # Detail page for a single topic
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),

    path('topics/new/', TopicCreateView.as_view(), name='new_topic'),


    path('topics/delete/<int:pk>/', TopicDeleteView.as_view(), name='delete-topic'),

    path('topics/update/<int:pk>/', TopicUpdateView.as_view(), name='update-topic'),

    path('editentry/<int:pk>/', EntryUpdateView.as_view(), name='entry_edit'),
    path('deleteentry/<int:pk>', EntryDeleteView.as_view(), name='entry_delete'),
    path('topics/<int:pk>/addentry/', EntryCreateView.as_view(), name='entry_new'),

    path('upload/csv/', upload_csv, name='upload_csv'),


]
