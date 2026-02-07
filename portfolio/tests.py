from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from .models import Artwork, Message, Profile
from .forms import ContactForm

class ModelTests(TestCase):
    def test_artwork_slug_generation(self):
        """Test that artwork slug is automatically generated from title."""
        art = Artwork.objects.create(title="My Masterpiece", image="artwork/test.jpg")
        self.assertEqual(art.slug, "my-masterpiece")

    def test_message_creation(self):
        """Test that a message can be created."""
        msg = Message.objects.create(
            name="John Doe", 
            email="john@example.com", 
            subject="Hello", 
            message="Test message"
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(str(msg), "Message from John Doe - Hello")

class FormTests(TestCase):
    def test_contact_form_valid(self):
        """Test contact form with valid data and empty honeypot."""
        form_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Commission',
            'message': 'I want a painting.',
            'honeypot': '' # Empty is correct
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_honeypot_spam(self):
        """Test that filling the honeypot field triggers validation error."""
        form_data = {
            'name': 'Spam Bot',
            'email': 'spam@bot.com',
            'subject': 'Spam',
            'message': 'Buy this!',
            'honeypot': 'I am a bot' # Filled honeypot
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Spam detected.", form.non_field_errors())

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(name="Artist", email="artist@example.com")
        self.art = Artwork.objects.create(title="Test Art", image="artwork/test.jpg")

    def test_index_page_loads(self):
        """Test that homepage loads successfully."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_artwork_detail_page(self):
        """Test artwork detail page for existing and non-existing art."""
        # Existing
        url = reverse('artwork_detail', args=[self.art.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Non-existing
        url_404 = reverse('artwork_detail', args=['non-existent-slug'])
        response = self.client.get(url_404)
        self.assertEqual(response.status_code, 404)

    def test_contact_form_submission_success(self):
        """Test valid contact form submission via view."""
        form_data = {
            'name': 'Real User',
            'email': 'user@example.com',
            'subject': 'Hi',
            'message': 'Nice work!',
            'honeypot': ''
        }
        response = self.client.post(reverse('index'), form_data, follow=True)
        self.assertRedirects(response, reverse('index'))
        
        # Check message stored in DB
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().name, 'Real User')
        
        # Check success message in response
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Message received! I'll get back to you soon.")

    def test_contact_form_submission_spam(self):
        """Test spam contact form submission via view."""
        form_data = {
            'name': 'Spam Bot',
            'email': 'spam@bot.com',
            'subject': 'Spam',
            'message': 'Spam',
            'honeypot': 'Filled'
        }
        response = self.client.post(reverse('index'), form_data)
        
        # Should re-render page with form errors (not redirect)
        self.assertEqual(response.status_code, 200)
        
        # Check message NOT stored in DB
        self.assertEqual(Message.objects.count(), 0)

