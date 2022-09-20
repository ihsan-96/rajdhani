"""Email notifications on bookings.
"""
from . import config
import smtplib
from email.message import EmailMessage

def send_booking_confirmation_email(booking):
    """Sends a confirmation email on successful booking.

    The argument `booking` is a row in the database that contains the following fields:

        id, name, email, train_number, train_name, ticket_class, date
    """
    email = EmailMessage()
    email['Subject'] = 'Train Ticket Booking Successful!'
    email['From'] = 'Rajdhani Travel <rajdhani@example.com>'
    email['To'] = f'{booking["passenger_name"]} <{booking["passenger_email"]}>'
    email.set_content(f"""Hello {booking["passenger_name"]},
    Your ticket booking is successful

    Yours very truly,
    Team Rajdhani
    """)

    smtp = smtplib.SMTP(f'{config.smtp_hostname[0]}:{config.smtp_port[0]}')
    try:
        smtp.send_message(email)
    finally:
        smtp.quit()
