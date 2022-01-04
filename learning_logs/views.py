from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Topic
from .models import Entry

from .forms import EntryForm
from django.views.generic import FormView
from django.shortcuts import render
from django.http import HttpResponseRedirect

import logging
from django.contrib import messages
from django.urls import reverse


class IndexView(TemplateView):
    template_name = "learning_logs/index.html"


class TopicListView(ListView):
    model = Topic
    template_name = "learning_logs/topics.html"

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(owner=user)


class TopicDetailView(DetailView):
    model = Topic
    template_name = "learning_logs/topic.html"


class TopicCreateView(CreateView):
    model = Topic
    template_name = "learning_logs/topic_new.html"
    fields = ['text']
    success_url = '/topics'

    def form_valid(self, form):
        print('form_valid')
        self.object = form.save(commit=False)
        print(self.request.user)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TopicDeleteView(DeleteView):
    model = Topic
    template_name = "learning_logs/topic_delete.html"
    success_url = '/topics'


class TopicUpdateView(UpdateView):
    model = Topic
    fields = ['text']
    template_name = "learning_logs/update.html"
    success_url = '/topics'


class EntryUpdateView(UpdateView):
    model = Entry
    fields = ['text', 'page_number', 'chapter_number', 'status']
    template_name = "learning_logs/update_entry.html"
    success_url = '/topics'


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = "learning_logs/delete_entry.html"
    success_url = '/topics'


class EntryCreateView(FormView):

    model = Entry
    template_name = "learning_logs/add_entry.html"
    success_url = '/topics'
    form_class = EntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        print(context['pk'])
        return context

    def form_valid(self, form):
        text = form.cleaned_data['text']
        page_number = form.cleaned_data['page_number']
        chapter_number = form.cleaned_data['chapter_number']
        topic = Topic.objects.get(pk=self.kwargs['pk'])
        entry = Entry(text=text, page_number=page_number,
                      chapter_number=chapter_number, topic=topic)
        entry.save()
        return super().form_valid(form)


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "learning_logs/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("learning_logs:upload_csv"))
        file_data = csv_file.read().decode("utf-8")
        # print(file_data)
        lines = file_data.split("\n")
        # Topic.objects.create(lines[0]['book_title'])
        print(lines[1])
        fields = lines[1].split(",")
        t = Topic(text=fields[2])
        t.save()
        lines.pop(0)
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["chapter_number"] = fields[0]
            data_dict["chapter_title"] = fields[1]
            data_dict["book_title"] = fields[2]
            entry = Entry(text=data_dict["chapter_title"],
                          topic=t, chapter_number=int(data_dict["chapter_number"]))
            entry.save()

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("learning_logs:upload_csv"))
