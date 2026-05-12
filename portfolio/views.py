from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .models import *
from .forms import ContactForm


# Create your views here.
def index(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    details = DetailItem.objects.all()
    experiences = Experience.objects.order_by("-featured", "-id")
    educations = Education.objects.order_by("year_range")
    # only display root-level services (categories) on the homepage
    # prefetch children to avoid N+1 queries
    services = (
        Service.objects.filter(parent__isnull=True)
        .order_by("-featured")
        .prefetch_related("subservices")
    )
    portfolio_items = PortfolioItem.objects.all()

    # handle contact form submission
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # attempt to send an email notification as well
            subject = contact.subject
            # include sender info in body so we can reply
            body = (
                f"You have a new message from {contact.name} <{contact.email}>\n\n"
                f"{contact.message}"
            )
            recipient_list = []
            # use PROFILE email if available, otherwise fall back to settings
            profile = Profile.objects.first()
            if profile and profile.email:
                recipient_list.append(profile.email)
            elif hasattr(settings, "EMAIL_HOST_USER"):
                recipient_list.append(settings.EMAIL_HOST_USER)

            if recipient_list:
                try:
                    send_mail(subject, body, contact.email, recipient_list, fail_silently=False)
                except Exception:
                    # don't crash the view; just log or ignore
                    pass

            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("index")
    else:
        form = ContactForm()

    context = {
        "profile": profile,
        "skills": skills,
        "details": details,
        "experiences": experiences,
        "educations": educations,
        "services": services,
        "portfolio_items": portfolio_items,
        "contact_form": form,
    }
    return render(request, "index.html", context)



def services_details(request, services_id):
    # retrieve the selected service and any child services (sub-services)
    service = Service.objects.get(id=services_id)
    tech = Tech_tools.objects.filter(tech_tools=service)
    customer = customerServices.objects.filter(customer_services=service)
    profile = Profile.objects.first()

    context = {
        "service": service, 
        "tech": tech,
        "customer": customer,
        "profile": profile,
        }
    return render(request, "service-details.html", context)