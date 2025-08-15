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
        self.book = Book.objects.create(title="Test Book", author=self.author, isbn='fake_isbn')
        self.member = Member.objects.create(user=self.member)

        self.overdue_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() - timezone.timedelta(days=1),
            is_returned=False,
        )
        self.returned_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() - timezone.timedelta(days=1),
            is_returned=True,
        )
        self.active_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() + timezone.timedelta(days=1),
            is_returned=False,
        )

    @patch("library.tasks.send_mail")
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_check_overdue_loans(self, send_mail_mock):
        check_overdue_loans.delay()

        self.assertTrue(send_mail_mock.called)

# Create your tests here.
