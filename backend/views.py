import os
import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django.conf import settings

from backend.models import Field


class IndexView(TemplateView):
    template_name = 'frontend/index.html'

    def get(self, request):
        if request.is_ajax():
            return self.ajax_response(request)

        field = Field.objects.first()
        analysis_data = field.analysis.order_by('-year').first()
        result_data = analysis_data.get_results()
        context = {
            'field': field,
            'data': analysis_data,
            'results': result_data,
            'measurements': analysis_data.monitoring_set.all()
        }
        return render(request, self.template_name, context)

    def ajax_response(self, request):
        field = Field.objects.get(name=request.GET['field'])
        year = int(request.GET['year'])
        analysis_data = field.analysis.get(year=year)
        result_data = analysis_data.get_results()

        analysis_html = render_to_string('frontend/field_analysis.html', {
            'data': analysis_data
        })
        result_html = render_to_string('frontend/results.html', {
            'results': result_data
        })
        measurements_html = render_to_string('frontend/soil-report.html', {
            'measurements': analysis_data.monitoring_set.all()
        })

        return JsonResponse({
            'analysis': analysis_html,
            'results': result_html,
            'measurements': measurements_html
        })
