from django.shortcuts import render
from django.views.generic import TemplateView


class FrontView(TemplateView):
    template_name = "front/index.html"