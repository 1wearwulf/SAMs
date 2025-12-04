"""
Services for the notifications app.
"""
import logging
from typing import List, Optional, Dict, Any
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from firebase_admin import messaging
from twilio.rest import Client
from .models import Notification, PushNotificationToken, NotificationLog, NotificationPreference

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for handling notifications across different channels.
    """

    @staticmethod
    def send_push_notification(
        token: str,
        title: str,
        message: str,
        data: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Send a push notification via FCM.

        Args:
            token: FCM token
            title: Notification title
            message: Notification message
            data: Additional data payload

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            message_obj = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=token,
                data=data or {},
            )

            response = messaging.send(message_obj)
            logger.info(f"Push notification sent successfully: {response}")
            return True

        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False

    @staticmethod
    def send_email_notification(
        recipient_email: str,
        subject: str,
        message: str,
        html_message: Optional[str] = None
    ) -> bool:
        """
        Send an email notification.

        Args:
            recipient_email: Recipient email address
            subject: Email subject
            message: Plain text message
            html_message: HTML message (optional)

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
            )
            logger.info(f"Email notification sent to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False

    @staticmethod
    def send_sms_notification(
        phone_number: str,
        message: str
    ) -> bool:
        """
        Send an SMS notification via Twilio.

        Args:
            phone_number: Recipient phone number
            message: SMS message

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message_obj = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            logger.info(f"SMS notification sent: {message_obj.sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False

    @staticmethod
    def send_bulk_notification(
        title: str,
        message: str,
        notification_type: str,
        recipient_ids: List[int],
        sender_id: int,
        course_id: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Send a notification to multiple recipients via all enabled channels.

        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            recipient_ids: List of recipient user IDs
            sender_id: Sender user ID
            course_id: Course ID (optional)

        Returns:
            Dictionary with success/failure counts
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Create notification record
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            sender_id=sender_id,
            course_id=course_id,
            is_sent=True,
            sent_at=timezone.now()
        )

        # Add recipients
        recipients = User.objects.filter(id__in=recipient_ids)
        notification.recipients.set(recipients)

        success_count = 0
        failure_count = 0

        for recipient in recipients:
            if NotificationService._send_to_user(notification, recipient):
                success_count += 1
            else:
                failure_count += 1

        return {
            'success': success_count,
            'failure': failure_count,
            'total': len(recipient_ids)
        }

    @staticmethod
    def _send_to_user(notification: Notification, user) -> bool:
        """
        Send notification to a specific user via all enabled channels.

        Args:
            notification: Notification instance
            user: User instance

        Returns:
            True if at least one channel succeeded, False otherwise
        """
        success = False

        # Get user preferences
        preferences = NotificationPreference.objects.filter(user=user).first()
        if not preferences:
            # Create default preferences
            preferences = NotificationPreference.objects.create(user=user)

        # Send push notification
        if NotificationService._should_send_push(notification.notification_type, preferences):
            push_tokens = PushNotificationToken.objects.filter(
                user=user,
                is_active=True
            )

            for token_obj in push_tokens:
                data = {
                    'notification_id': str(notification.id),
                    'type': notification.notification_type,
                    'course_id': str(notification.course.id) if notification.course else '',
                }

                if NotificationService.send_push_notification(
                    token_obj.token,
                    notification.title,
                    notification.message,
                    data
                ):
                    NotificationLog.objects.create(
                        notification=notification,
                        recipient=user,
                        delivery_method='push',
                        status='sent',
                        sent_at=timezone.now()
                    )
                    success = True

        # Send email notification
        if NotificationService._should_send_email(notification.notification_type, preferences):
            html_message = render_to_string('notification_email.html', {
                'notification': notification,
                'user': user,
            })

            if NotificationService.send_email_notification(
                user.email,
                notification.title,
                notification.message,
                html_message
            ):
                NotificationLog.objects.create(
                    notification=notification,
                    recipient=user,
                    delivery_method='email',
                    status='sent',
                    sent_at=timezone.now()
                )
                success = True

        # Send SMS notification (for urgent notifications only)
        if (NotificationService._should_send_sms(notification.notification_type, preferences) and
            user.phone):
            if NotificationService.send_sms_notification(
                user.phone,
                f"{notification.title}: {notification.message}"
            ):
                NotificationLog.objects.create(
                    notification=notification,
                    recipient=user,
                    delivery_method='sms',
                    status='sent',
                    sent_at=timezone.now()
                )
                success = True

        return success

    @staticmethod
    def _should_send_push(notification_type: str, preferences: NotificationPreference) -> bool:
        """
        Check if push notification should be sent based on type and preferences.
        """
        type_mapping = {
            'announcement': preferences.push_course_announcements,
            'reminder': preferences.push_attendance_reminders,
            'alert': preferences.push_system_notifications,
            'system': preferences.push_system_notifications,
        }
        return type_mapping.get(notification_type, True)

    @staticmethod
    def _should_send_email(notification_type: str, preferences: NotificationPreference) -> bool:
        """
        Check if email notification should be sent based on type and preferences.
        """
        type_mapping = {
            'announcement': preferences.email_course_announcements,
            'reminder': preferences.email_attendance_reminders,
            'alert': preferences.email_system_notifications,
            'system': preferences.email_system_notifications,
        }
        return type_mapping.get(notification_type, True)

    @staticmethod
    def _should_send_sms(notification_type: str, preferences: NotificationPreference) -> bool:
        """
        Check if SMS notification should be sent based on type and preferences.
        """
        type_mapping = {
            'alert': preferences.sms_urgent_notifications,
            'reminder': preferences.sms_attendance_alerts,
        }
        return type_mapping.get(notification_type, False)

    @staticmethod
    def register_push_token(
        user_id: int,
        token: str,
        device_type: str,
        device_name: str = ""
    ) -> PushNotificationToken:
        """
        Register a push notification token for a user.

        Args:
            user_id: User ID
            token: FCM token
            device_type: Type of device (android/ios/web)
            device_name: Optional device name

        Returns:
            PushNotificationToken instance
        """
        token_obj, created = PushNotificationToken.objects.get_or_create(
            token=token,
            defaults={
                'user_id': user_id,
                'device_type': device_type,
                'device_name': device_name,
                'is_active': True
            }
        )

        if not created:
            # Update existing token
            token_obj.user_id = user_id
            token_obj.device_type = device_type
            token_obj.device_name = device_name
            token_obj.is_active = True
            token_obj.save()

        return token_obj

    @staticmethod
    def unregister_push_token(token: str) -> bool:
        """
        Unregister a push notification token.

        Args:
            token: FCM token to unregister

        Returns:
            True if token was found and deactivated, False otherwise
        """
        try:
            token_obj = PushNotificationToken.objects.get(token=token)
            token_obj.is_active = False
            token_obj.save()
            return True
        except PushNotificationToken.DoesNotExist:
            return False

    @staticmethod
    def get_user_notification_stats(user_id: int) -> Dict[str, int]:
        """
        Get notification statistics for a user.

        Args:
            user_id: User ID

        Returns:
            Dictionary with notification counts
        """
        logs = NotificationLog.objects.filter(recipient_id=user_id)

        return {
            'total_sent': logs.count(),
            'delivered': logs.filter(status='delivered').count(),
            'read': logs.filter(status='read').count(),
            'failed': logs.filter(status='failed').count(),
        }

    @staticmethod
    def mark_notification_read(notification_id: int, user_id: int) -> bool:
        """
        Mark a notification as read for a user.

        Args:
            notification_id: Notification ID
            user_id: User ID

        Returns:
            True if marked successfully, False otherwise
        """
        try:
            log = NotificationLog.objects.get(
                notification_id=notification_id,
                recipient_id=user_id
            )
            log.status = 'read'
            log.read_at = timezone.now()
            log.save()
            return True
        except NotificationLog.DoesNotExist:
            return False
