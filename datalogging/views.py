from utils import render_with_context
from django.conf import settings
from django.shortcuts import render_to_response
from datalogging.models import Timeseries
from datalogging import to_matlab, export_csv, processing
from datetime import datetime
from datalogging.forms import TimeseriesDataForm, UnauthTimeseriesDataForm
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Q
import os

def ajax_timeseries_data(request):
    num_samples=request.GET.get('num_samples')
    #convert to an integer if it exists
    if num_samples:
        num_samples=int(num_samples)

    start_time=request.GET.get('start_time')
    end_time=request.GET.get('end_time')
    if not request.user.is_authenticated():
        form=UnauthTimeseriesDataForm
    else:
        form=TimeseriesDataForm
    
    if request.GET:
        form=form(request.GET)
        if form.is_valid():
            num_samples=form.cleaned_data['number_of_samples']
            start_time=form.cleaned_data['start_time']
            end_time=form.cleaned_data['end_time']
            number_of_samples=form.cleaned_data['number_of_samples']
            ts=form.cleaned_data['timeseries']
            if form.cleaned_data['action']=='JSON':
                #ts=Timeseries.objects.get(pk=ts_pk)
                data=ts.data_cropped_resampled(num_samples=num_samples, time_range_crop=(start_time, end_time), style='flot')
                return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
            elif form.cleaned_data['action']=='stats':
                #ts=Timeseries.objects.get(pk=ts_pk)
                start_time, end_time=ts.auto_date_range()
                num_samples=ts.datapoint_set.count()
                return HttpResponse(simplejson.dumps({'ts':ts.pk,'start_time':str(start_time), 'end_time':str(end_time), 'number_of_samples':num_samples}), mimetype="application/javascript")
            elif form.cleaned_data['action']=='csv':
                response=HttpResponse()
                export_csv.export_to_csv(response, (start_time, end_time), (ts,)) #it expects a set of timeseries, not just one so we trick it
                response['Content-Disposition']='attachment; filename=%s%s.csv' % ('erebus_caves_ts_',ts.pk)
                return response

            elif form.cleaned_data['action']=='matlab':
                # note: does not chop dates yet
                response=HttpResponse()
                response['Content-Disposition']='attachment; filename=%s%s.mat' % ('erebus_caves_ts_',ts.pk)
                to_matlab.make_mat(response,ts_pk_list=[ts.pk],samples_per_ts=num_samples)
                return response
            elif form.cleaned_data['action']=='newpage':
                return render_with_context(request,'timeseries_browser.html',{'ts_form':form,'auto_click_submit':True})

  
        elif form.is_bound:
            return render_with_context(request,'timeseries_browser.html',{'ts_form':form,})
    else:
        form = form()
        return render_with_context(request,'timeseries_browser.html',{'ts_form':form,})
        
def monthly_stats(request, data_type):
    tses=Timeseries.objects.filter(data_type=data_type)
    template_file='timeseries_stats.html'
    if request.GET:
        pk_list=request.GET.getlist('ts')
        tses=tses.filter(logbook_entry__cave__slug__in=pk_list)
        if 'overall' in request.GET:
            overall_stats=processing.monthly_stats_multiple(pk_list, data_type=data_type)
        else:
            overall_stats=None
        if 'plot' in request.GET:
            template_file='timeseries_stats_plot.html'
            
    return render_with_context(request,template_file,{'timeseries': tses,'overall_stats':overall_stats})
