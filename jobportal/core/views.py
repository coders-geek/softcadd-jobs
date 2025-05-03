from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from jobs.models import Job


def home(request):
    featured_jobs = Job.objects.filter(status='active').order_by('-posted_date')[:6]
    return render(request, 'home.html', {'featured_jobs': featured_jobs})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def search(request):
    query = request.GET.get('q', '')
    jobs = []
    companies = []
    freelancers = []

    if query:
        jobs = Job.objects.filter(title__icontains=query, status='active')
        companies = request.user.business_profile.__class__.objects.filter(company_name__icontains=query,
                                                                           is_approved=True)
        freelancers = request.user.freelancer_profile.__class__.objects.filter(user__first_name__icontains=query) | \
                      request.user.freelancer_profile.__class__.objects.filter(user__last_name__icontains=query)

    return render(request, 'search.html', {
        'query': query,
        'jobs': jobs,
        'companies': companies,
        'freelancers': freelancers,
    })