from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Skill, Artwork, Message
from .forms import ContactForm

def index(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    # Fetch content - Default ordering specified in Model Meta class
    featured_artworks = Artwork.objects.filter(is_featured=True)
    all_artworks = Artwork.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Message from {name} ({email}):\n\n{message}"
            
            # Send email to admin (Graceful failure)
            try:
                admin_email = profile.email if profile and profile.email else settings.EMAIL_HOST_USER
                send_mail(
                    f"Portfolio Contact: {subject}",
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error silently, message is already saved in DB
                print(f"Email sending failed: {e}")

            messages.success(request, "Message received! I'll get back to you soon.")
            return redirect('index')
    else:
        form = ContactForm()

    context = {
        'profile': profile,
        'skills': skills,
        'featured_artworks': featured_artworks,
        'all_artworks': all_artworks,
        'form': form,
    }
    return render(request, 'index.html', context)

def artwork_detail(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    profile = Profile.objects.first() # For navbar name
    context = {
        'artwork': artwork,
        'profile': profile,
    }
    return render(request, 'artwork_detail.html', context)

def dashboard_callback(request, context):
    """
    Callback for django-unfold dashboard.
    Adds custom context to the admin dashboard.
    """
    context.update({
        "total_artworks": Artwork.objects.count(),
        "latest_artworks": Artwork.objects.all()[:5],
        "unread_messages": Message.objects.filter(is_read=False).count(),
        "latest_messages": Message.objects.order_by('-created_at')[:5],
    })
    return context
