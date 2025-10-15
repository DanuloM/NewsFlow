from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (
    RedactorCreationForm,
    RedactorUpdateNewspapersForm,
)
from agency.models import Newspaper, Topic, Redactor


@login_required
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


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 10


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("publishers").select_related("topic")


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "agency/newspaper_confirm_delete.html"
    success_url = reverse_lazy("agency:newspaper-list")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 10


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "agency/topic_confirm_delete.html"
    success_url = reverse_lazy("agency:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 10


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateNewspapersForm
    success_url = reverse_lazy("agency:redactor-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.newspapers.clear()
        for newspaper in form.cleaned_data["newspapers"]:
            newspaper.publishers.add(self.object)
        return response


class RedactorDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Redactor
    template_name = "agency/redactor_confirm_delete.html"
    success_url = reverse_lazy("agency:redactor-list")
