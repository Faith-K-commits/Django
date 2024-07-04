from django.test import TestCase
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_form(self):
        form = LoginForm(data={'username': self.username, 'password': self.password})
        self.assertTrue(form.is_valid())

    def test_successful_login(self):
        response = self.client.post(reverse('account:login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:home'))

    def test_invalid_login(self):
        response = self.client.post(reverse('account:login'), {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password. Please try again later.')


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'newuser',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'Test',
            'email': 'newuser@example.com'
        }

    def test_registration_form(self):
        form = RegistrationForm(data=self.valid_user_data)
        self.assertTrue(form.is_valid())

    def test_successful_registration(self):
        response = self.client.post(reverse('account:register'), data=self.valid_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login'))

        # Check if user was created
        user = User.objects.get(username=self.valid_user_data['username'])
        self.assertIsNotNone(user)

        # Verify that the password is hashed
        self.assertNotEqual(user.password, self.valid_user_data['password'])
        self.assertTrue(user.check_password(self.valid_user_data['password']))

    def test_invalid_registration_password_mismatch(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        response = self.client.post(reverse('account:register'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match.')

        # Ensure no user was created
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=invalid_data['username'])

    def test_invalid_registration_duplicate_email(self):
        # Create user with the same email first
        User.objects.create_user(username='existinguser', email=self.valid_user_data['email'], password='password123')
        response = self.client.post(reverse('account:register'), self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already registered.')

        # Ensure no additional user was created
        user_count = User.objects.filter(email=self.valid_user_data['email']).count()
        self.assertEqual(user_count, 1)