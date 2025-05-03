from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication, JobCategory
from .forms import JobForm, JobApplicationForm
from accounts.models import JobSeekerProfile


def job_list(request):
    jobs = Job.objects.filter(status='active').order_by('-posted_date')
    categories = JobCategory.objects.all()

    # Filtering
    category = request.GET.get('category')
    if category:
        jobs = jobs.filter(category__name=category)

    search_query = request.GET.get('q')
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    context = {
        'jobs': jobs,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query or '',
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False

    if request.user.is_authenticated and request.user.user_type == 'job_seeker':
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()

    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_application(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('job_detail', pk=pk)

    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)

    try:
        profile = request.user.job_seeker_profile
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile before applying for jobs.')
        return redirect('job_seeker_profile')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = JobApplicationForm()

    context = {
        'job': job,
        'form': form,
        'profile': profile,
    }
    return render(request, 'jobs/job_application.html', context)


@login_required
def job_post(request):
    if request.user.user_type != 'business' or not request.user.is_approved:
        messages.error(request, 'Only approved businesses can post jobs.')
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.business_profile
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('business_job_list')
    else:
        form = JobForm()

    context = {
        'form': form,
    }
    return render(request, 'jobs/job_post.html', context)


@login_required
def business_job_list(request):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    jobs = Job.objects.filter(company=request.user.business_profile).order_by('-posted_date')
    context = {
        'jobs': jobs,
    }
    return render(request, 'jobs/business_job_list.html', context)


@login_required
def business_applications(request):
    if request.user.user_type != 'business':
        messages.error(request, 'Only businesses can access this page.')
        return redirect('home')

    applications = JobApplication.objects.filter(job__company=request.user.business_profile).select_related('job',
                                                                                                            'applicant')
    context = {
        'applications': applications,
    }
    return render(request, 'jobs/business_applications.html', context)


@login_required
def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.user.user_type != 'business' or application.job.company != request.user.business_profile:
        messages.error(request, 'You are not authorized to view this application.')
        return redirect('home')

    if request.method == 'POST':
        status = request.POST.get('status')
        comments = request.POST.get('comments')
        application.status = status
        application.comments = comments
        application.save()
        messages.success(request, 'Application status updated successfully!')
        return redirect('application_detail', pk=pk)

    context = {
        'application': application,
    }
    return render(request, 'jobs/application_detail.html', context)