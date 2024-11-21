from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from apps.main.models import Book
import logging

logger = logging.getLogger(__name__)

def get_recipient_list():
    """Получить список email активных пользователей."""
    return [user.email for user in User.objects.filter(is_active=True) if user.email]


@shared_task
def notify_new_books():
    """
    Отправить уведомление о новых книгах, добавленных за последние 24 часа.
    """

    yesterday = datetime.now() - timedelta(days=1)
    new_books = Book.objects.filter(publication_date__gte=yesterday)

    if not new_books.exists():
        logger.info("Нет новых книг за последние 24 часа.")
        return
    
    book_titles = '\n'.join(book.title for book in new_books) # Название книг из базы
    recipient_list = get_recipient_list()

    try:
        send_mail(
            subject="Новые книги",
            message=f"Новые книги, добавленные за последние 24 часа:\n{book_titles}",
            from_email="library@example.com",
            recipient_list=recipient_list,
        )
        logger.info(f"Письма о новых книгах ({len(new_books)}) успешно отправлены {len(recipient_list)} получателям.")
    except Exception as e:
        logger.error(f"Ошибка отправки писем о новых книгах: {e}")

@shared_task
def notify_anniversary_books():
    """
    Отправить уведомление о юбилейных книгах.
    """
    today = datetime.now()
    anniversary_years = {5,10,20,50}

    anniversary_books = Book.objects.filter(
        publication_date__month=today.month,
        publication_date__day=today.day,
        publication_date__year__in=[today.year - year for year in anniversary_years],
    )


    if not anniversary_books.exists():
        logger.info("Нет юбилейных книг за последние 24 часа.")
        return
    
    book_titles = '\n'.join(book.title for book in anniversary_books)
    recipient_list = get_recipient_list()

    try:
        send_mail(
            subject="Юбилейные книги",
            message=f"Юбилейные книги за последние 24 часа:\n{book_titles}",
            from_email="library@example.com",
            recipient_list=recipient_list,
        )
        logger.info(f"Письма о юбилейных книгах ({len(anniversary_books)}) успешно отправлены {len(recipient_list)} получателям.")
    except Exception as e:
        logger.error(f"Ошибка отправки писем о юбилейных книгах: {e}")