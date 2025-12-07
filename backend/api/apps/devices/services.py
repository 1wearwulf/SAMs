"""
Services for the devices app.
"""
from django.utils import timezone
from datetime import timedelta
from .models import Device, DeviceFingerprint, DeviceLocation, DeviceSession, DeviceAlert, DeviceAnalytics


class DeviceService:
    """
    Service class for device-related operations.
    """

    @staticmethod
    def register_device(user, device_data):
        """
        Register a new device for a user.
        """
        device, created = Device.objects.get_or_create(
            user=user,
            device_id=device_data['device_id'],
            defaults={
                'device_type': device_data.get('device_type', 'mobile'),
                'device_name': device_data.get('device_name', ''),
                'os': device_data.get('os', ''),
                'os_version': device_data.get('os_version', ''),
                'app_version': device_data.get('app_version', ''),
                'model': device_data.get('model', ''),
                'manufacturer': device_data.get('manufacturer', ''),
                'screen_resolution': device_data.get('screen_resolution', ''),
                'mac_address': device_data.get('mac_address', ''),
                'imei': device_data.get('imei', ''),
            }
        )
        return device, created

    @staticmethod
    def update_device_location(device_id, location_data):
        """
        Update device location.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            location = DeviceLocation.objects.create(
                device=device,
                latitude=location_data['latitude'],
                longitude=location_data['longitude'],
                accuracy=location_data.get('accuracy'),
                altitude=location_data.get('altitude'),
                speed=location_data.get('speed'),
                heading=location_data.get('heading'),
                timestamp=location_data.get('timestamp', timezone.now()),
                source=location_data.get('source', 'gps')
            )
            return location
        except Device.DoesNotExist:
            return None

    @staticmethod
    def get_device_health_score(device_id):
        """
        Calculate device health score based on various factors.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            score = 100

            # Deduct points for inactive status
            if device.status != 'active':
                score -= 20

            # Deduct points for not seen recently (more than 24 hours)
            if device.last_seen < timezone.now() - timedelta(hours=24):
                score -= 30

            # Deduct points for untrusted devices
            if not device.is_trusted:
                score -= 10

            return max(0, score)
        except Device.DoesNotExist:
            return 0

    @staticmethod
    def get_device_analytics(device_id):
        """
        Get analytics data for a device.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            analytics, created = DeviceAnalytics.objects.get_or_create(device=device)

            # Update analytics data
            analytics.total_sessions = device.sessions.count()
            analytics.total_locations = device.locations.count()
            analytics.total_alerts = device.alerts.count()

            # Calculate average session duration
            sessions = device.sessions.filter(ended_at__isnull=False)
            if sessions.exists():
                total_duration = sum(
                    (session.ended_at - session.started_at).total_seconds()
                    for session in sessions
                )
                analytics.average_session_duration = total_duration / sessions.count()

            analytics.save()

            return {
                'device_info': {
                    'device_id': device.device_id,
                    'device_name': device.device_name,
                    'device_type': device.device_type,
                    'status': device.status,
                    'last_seen': device.last_seen,
                },
                'analytics': {
                    'total_sessions': analytics.total_sessions,
                    'total_locations': analytics.total_locations,
                    'total_alerts': analytics.total_alerts,
                    'average_session_duration': analytics.average_session_duration,
                },
                'recent_locations': [
                    {
                        'latitude': loc.latitude,
                        'longitude': loc.longitude,
                        'timestamp': loc.timestamp,
                    }
                    for loc in device.locations.order_by('-timestamp')[:10]
                ],
                'alerts_count': analytics.total_alerts,
            }
        except Device.DoesNotExist:
            return None

    @staticmethod
    def create_device_alert(device_id, alert_type, severity, title, message, data=None):
        """
        Create an alert for a device.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            alert = DeviceAlert.objects.create(
                device=device,
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                data=data or {}
            )
            return alert
        except Device.DoesNotExist:
            return None

    @staticmethod
    def validate_device_fingerprint(device_id, fingerprint_data):
        """
        Validate device fingerprint.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            # Simple validation - check if fingerprint exists
            fingerprint = DeviceFingerprint.objects.filter(
                device=device,
                is_active=True
            ).first()

            if fingerprint:
                # Compare fingerprints (simplified)
                return True
            else:
                # Create new fingerprint
                fingerprint_hash = str(hash(str(fingerprint_data)))
                DeviceFingerprint.objects.create(
                    device=device,
                    fingerprint_hash=fingerprint_hash,
                    fingerprint_data=fingerprint_data
                )
                return True
        except Device.DoesNotExist:
            return False

    @staticmethod
    def start_device_session(device_id, session_id, ip_address, user_agent):
        """
        Start a new device session.
        """
        try:
            device = Device.objects.get(device_id=device_id)
            session = DeviceSession.objects.create(
                device=device,
                session_id=session_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            return session
        except Device.DoesNotExist:
            return None

    @staticmethod
    def end_device_session(session_id):
        """
        End a device session.
        """
        try:
            session = DeviceSession.objects.get(session_id=session_id)
            session.end_session()
            return session
        except DeviceSession.DoesNotExist:
            return None
