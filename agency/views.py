from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (
    RedactorCreationForm,
    RedactorUpdateNewspapersForm,
    SearchForm,
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["query"])
        return queryset

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["query"])
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["query"])
        return queryset

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



class ToggleRedactorAssignmentView(LoginRequiredMixin, generic.View):
    def post(self, request, pk, *args, **kwargs):
        newspaper = Newspaper.objects.get(pk=pk)
        redactor = request.user

        if redactor.newspapers.filter(pk=newspaper.pk).exists():
            redactor.newspapers.remove(newspaper)
        else:
            redactor.newspapers.add(newspaper)

        return HttpResponseRedirect(
            reverse_lazy("agency:newspaper-detail", kwargs={"pk": pk})
        )
