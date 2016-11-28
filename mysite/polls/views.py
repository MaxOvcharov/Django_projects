#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from .models import Question
from django.shortcuts import render, get_object_or_404


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # Более длинная версия
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question doesn't exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question,
                                                 "question_id": question_id})


def results(request, question_id):
    response = "<b>You are looking at the result of question {0}</b>"
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse("<b>You are voting on question {0}</b>".format(question_id))