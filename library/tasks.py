from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(
        due_date_of_loan = timezone.now(), is_returned=False
    ).select_related("book", "member_user")

    for loan in overdue_loans :
        user = loan.member.user
        book_title = loan.book.title
        send_mail(
            subject='Notice that the loaned book is now overdue',
            message=f'Hello {user.username},\n\nYou have loaned a book beyond its due date "{book_title}".\nPlease return it immediately.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
