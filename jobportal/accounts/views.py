from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    JobSeekerRegistrationForm,
    BusinessRegistrationForm,
    FreelancerRegistrationForm,
    JobSeekerProfileForm,
    BusinessProfileForm,
    FreelancerProfileForm
)
from .models import CustomUser, JobSeekerProfile, BusinessProfile, FreelancerProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_job_seeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('job_seeker_profile')
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'accounts/register_job_seeker.html', {'form': form})


def register_business(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('business_profile')
    else:
        form = BusinessRegistrationForm()
    return render(request, 'accounts/register_business.html', {'form': form})


def register_freelancer(request):
    if request.method == 'POST':
        form = FreelancerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('freelancer_profile')
    else:
        form = FreelancerRegistrationForm()
    return render(request, 'accounts/register_freelancer.html', {'form': form})


@login_required
def job_seeker_profile(request):
    try:
        profile = request.user.job_seeker_profile
    except JobSeekerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('job_seeker_profile')
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, 'accounts/job_seeker_profile.html', {'form': form})


@login_required
def business_profile(request):
    try:
        profile = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('business_profile')
    else:
        form = BusinessProfileForm(instance=profile)

    return render(request, 'accounts/business_profile.html', {'form': form})


@login_required
def freelancer_profile(request):
    try:
        profile = request.user.freelancer_profile
    except FreelancerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('freelancer_profile')
    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, 'accounts/freelancer_profile.html', {'form': form})