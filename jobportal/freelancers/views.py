from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FreelancerService
from .forms import FreelancerServiceForm


@login_required
def freelancer_dashboard(request):
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can access this page.')
        return redirect('home')

    context = {
        'freelancer': request.user.freelancer_profile,
    }
    return render(request, 'freelancers/dashboard.html', context)


@login_required
def service_list(request):
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can access this page.')
        return redirect('home')

    services = FreelancerService.objects.filter(freelancer=request.user.freelancer_profile)
    context = {
        'services': services,
    }
    return render(request, 'freelancers/service_list.html', context)


@login_required
def service_create(request):
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can access this page.')
        return redirect('home')

    if request.method == 'POST':
        form = FreelancerServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer = request.user.freelancer_profile
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('service_list')
    else:
        form = FreelancerServiceForm()

    context = {
        'form': form,
    }
    return render(request, 'freelancers/service_form.html', context)


@login_required
def service_update(request, pk):
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can access this page.')
        return redirect('home')

    service = get_object_or_404(FreelancerService, pk=pk, freelancer=request.user.freelancer_profile)

    if request.method == 'POST':
        form = FreelancerServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('service_list')
    else:
        form = FreelancerServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'freelancers/service_form.html', context)


@login_required
def service_delete(request, pk):
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can access this page.')
        return redirect('home')

    service = get_object_or_404(FreelancerService, pk=pk, freelancer=request.user.freelancer_profile)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('service_list')