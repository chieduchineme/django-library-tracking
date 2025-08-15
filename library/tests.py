from django.test import TestCase, override_settings
from unit.test_mock import patch
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Loan, Book, Member, User, Author
from .tasks import check_overdue_loans

class LibraryTrackingTests(TestCase):
    def setUp(self):
        self.client = APIClient
        self.author = Author.objects.create(first_name="dika", last_name="Chiedu")
        self.member = User.objects.create(user_name="Chiedu")
        self.book = Book.objects.create(first_name="dika", last_name="Chiedu")
        # self.author = Author.objects.create(first_name="dika", last_name="Chiedu")

# Create your tests here.
