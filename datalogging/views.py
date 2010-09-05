from utils import render_with_context
from django.conf import settings
from django.shortcuts import render_to_response
from datalogging.models import Timeseries
from datetime import datetime
from datalogging.forms import TimeseriesDataForm
from django.http import HttpResponse
from django.utils import simplejson

def ajax_timeseries_data(request):
    num_samples=request.GET.get('num_samples')
    #convert to an integer if it exists
    if num_samples:
        num_samples=int(num_samples)

    start_time=request.GET.get('start_time')
    end_time=request.GET.get('end_time')

    
    if request.GET:
        form=TimeseriesDataForm(request.GET)
        if form.is_valid():
            num_samples=form.cleaned_data['number_of_samples']
            start_time=form.cleaned_data['start_time']
            end_time=form.cleaned_data['end_time']
            number_of_samples=form.cleaned_data['number_of_samples']

            if form.cleaned_data['action']=='JSON':
                ts=Timeseries.objects.get(pk=request.GET.get('timeseries'))
                data=ts.data_cropped_resampled(num_samples=num_samples, time_range_crop=(start_time, end_time), style='flot')
                return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
            elif form.cleaned_data['action']=='stats':
                ts=Timeseries.objects.get(pk=request.GET.get('timeseries'))
                start_time, end_time=ts.auto_date_range()
                num_samples=ts.datapoint_set.count()
                return HttpResponse(simplejson.dumps({'ts':ts.pk,'start_time':str(start_time), 'end_time':str(end_time), 'number_of_samples':num_samples}), mimetype="application/javascript")
            elif form.cleaned_data['action']=='CSV':
                return HttpResponse("CSV not implemented yet")
            elif form.cleaned_data['action']=='matlab':
                return HttpResponse("Matlab export not implemented yet")
            elif form.cleaned_data['action']=='newpage':
                return render_with_context(request,'timeseries_browser.html',{'ts_form':form,'auto_click_submit':True})

  
        elif form.is_bound:
            return render_with_context(request,'timeseries_browser.html',{'ts_form':form,})
    else:
        form = TimeseriesDataForm()
        return render_with_context(request,'timeseries_browser.html',{'ts_form':form,})


