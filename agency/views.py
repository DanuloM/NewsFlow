from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.models import Newspaper, Topic, Redactor


def index(request):
    num_of_newspapers = Newspaper.objects.count()
    num_of_topics = Topic.objects.count()
    num_of_redactors = Redactor.objects.count()
    context = {
        "num_of_newspapers": num_of_newspapers,
        "num_of_topics": num_of_topics,
        "num_of_redactors": num_of_redactors,
    }
    return render(request, "agency/index.html", context)


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 10



class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("publishers").select_related("topic")


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency:newspaper-list")

class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency:newspaper-list")


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 10



class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 10



class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers")
