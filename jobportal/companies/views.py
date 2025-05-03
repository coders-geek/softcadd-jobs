from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm


@login_required
def company_dashboard(request):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    context = {
        'company': request.user.business_profile,
    }
    return render(request, 'companies/dashboard.html', context)


@login_required
def event_list(request):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    events = Event.objects.filter(company=request.user.business_profile).order_by('-start_date')
    context = {
        'events': events,
    }
    return render(request, 'companies/event_list.html', context)


@login_required
def event_create(request):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.company = request.user.business_profile
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()

    context = {
        'form': form,
    }
    return render(request, 'companies/event_form.html', context)


@login_required
def event_update(request, pk):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    event = get_object_or_404(Event, pk=pk, company=request.user.business_profile)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'companies/event_form.html', context)


@login_required
def event_delete(request, pk):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    event = get_object_or_404(Event, pk=pk, company=request.user.business_profile)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('event_list')