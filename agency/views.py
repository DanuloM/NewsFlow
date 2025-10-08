from django.shortcuts import render

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
