"""
Services for the devices app.
"""
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from .models import Device, DeviceFingerprint, DeviceLocation, DeviceSession, DeviceAlert


class DeviceService:
    """
    Service for managing device operations.
    """

    @staticmethod
    def register_device(
        user_id: int,
        device_data: Dict[str, Any]
    ) -> Device:
        """
        Register a new device for a user.

        Args:
            user_id: User ID
            device_data: Device information dictionary

        Returns:
            Device instance
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.get(id=user_id)
        device_id = device_data.get('device_id')

        # Check if device already exists
        device, created = Device.objects.get_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'device_type': device_data.get('device_type', 'mobile'),
                'device_name': device_data.get('device_name', f"{device_data.get('manufacturer', 'Unknown')} {device_data.get('model', 'Device')}"),
                'os': device_data.get('os'),
                'os_version': device_data.get('os_version'),
                'app_version': device_data.get('app_version'),
                'model': device_data.get('model'),
                'manufacturer': device_data.get('manufacturer'),
                'screen_resolution': device_data.get('screen_resolution'),
                'ip_address': device_data.get('ip_address'),
                'mac_address': device_data.get('mac_address'),
                'imei': device_data.get('imei'),
                'is_trusted': False,  # New devices start as untrusted
            }
        )

        if created:
            # Create device fingerprint
            fingerprint_data = DeviceService._generate_device_fingerprint(device_data)
            DeviceFingerprint.objects.create(
                device=device,
                fingerprint_hash=fingerprint_data['hash'],
                fingerprint_data=fingerprint_data['data']
            )

            # Create device permissions (default to disabled)
            from .models import DevicePermission
            DevicePermission.objects.create(device=device)

        return device

    @staticmethod
    def _generate_device_fingerprint(device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a unique fingerprint for the device.

        Args:
            device_data: Device information

        Returns:
            Dictionary with hash and data
        """
        # Collect fingerprint components
        fingerprint_components = {
            'device_id': device_data.get('device_id', ''),
            'manufacturer': device_data.get('manufacturer', ''),
            'model': device_data.get('model', ''),
            'os': device_data.get('os', ''),
            'os_version': device_data.get('os_version', ''),
            'screen_resolution': device_data.get('screen_resolution', ''),
            'mac_address': device_data.get('mac_address', ''),
            'imei': device_data.get('imei', ''),
        }

        # Create fingerprint string
        fingerprint_string = json.dumps(fingerprint_components, sort_keys=True)

        # Generate hash
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()

        return {
            'hash': fingerprint_hash,
            'data': fingerprint_components
        }

    @staticmethod
    def update_device_location(
        device_id: str,
        location_data: Dict[str, Any]
    ) -> DeviceLocation:
        """
        Update device location.

        Args:
            device_id: Device ID
            location_data: Location information

        Returns:
            DeviceLocation instance
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

            # Update device's last seen
            device.last_seen = timezone.now()
            device.save(update_fields=['last_seen'])

            return location

        except Device.DoesNotExist:
            raise ValueError(f"Device {device_id} not found")

    @staticmethod
    def start_device_session(
        device_id: str,
        session_data: Dict[str, Any]
    ) -> DeviceSession:
        """
        Start a new device session.

        Args:
            device_id: Device ID
            session_data: Session information

        Returns:
            DeviceSession instance
        """
        import uuid

        device = Device.objects.get(device_id=device_id)

        # End any existing active sessions for this device
        DeviceSession.objects.filter(
            device=device,
            is_active=True
        ).update(
            is_active=False,
            ended_at=timezone.now()
        )

        session = DeviceSession.objects.create(
            device=device,
            session_id=str(uuid.uuid4()),
            ip_address=session_data.get('ip_address'),
            user_agent=session_data.get('user_agent'),
            is_active=True
        )

        return session

    @staticmethod
    def end_device_session(session_id: str) -> None:
        """
        End a device session.

        Args:
            session_id: Session ID
        """
        try:
            session = DeviceSession.objects.get(session_id=session_id)
            session.end_session()
        except DeviceSession.DoesNotExist:
            pass

    @staticmethod
    def validate_device_fingerprint(
        device_id: str,
        fingerprint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate device fingerprint for security.

        Args:
            device_id: Device ID
            fingerprint_data: Current fingerprint data

        Returns:
            Validation result
        """
        try:
            device = Device.objects.get(device_id=device_id)
            stored_fingerprint = device.fingerprint

            if not stored_fingerprint or not stored_fingerprint.is_active:
                return {
                    'is_valid': False,
                    'reason': 'No stored fingerprint found'
                }

            # Generate current fingerprint
            current_fingerprint = DeviceService._generate_device_fingerprint(fingerprint_data)

            # Compare fingerprints
            is_valid = current_fingerprint['hash'] == stored_fingerprint.fingerprint_hash

            if not is_valid:
                # Create alert for fingerprint mismatch
                DeviceAlert.objects.create(
                    device=device,
                    alert_type='device_change',
                    severity='high',
                    title='Device Fingerprint Changed',
                    message='Device fingerprint has changed, possibly indicating device compromise.',
                    data={
                        'old_fingerprint': stored_fingerprint.fingerprint_data,
                        'new_fingerprint': current_fingerprint['data']
                    }
                )

            return {
                'is_valid': is_valid,
                'reason': 'Fingerprint match' if is_valid else 'Fingerprint mismatch'
            }

        except Device.DoesNotExist:
            return {
                'is_valid': False,
                'reason': 'Device not found'
            }

    @staticmethod
    def check_device_security(
        device_id: str,
        security_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Check device security status and return alerts.

        Args:
            device_id: Device ID
            security_data: Security-related data

        Returns:
            List of security alerts
        """
        alerts = []

        try:
            device = Device.objects.get(device_id=device_id)

            # Check battery level
            battery_level = security_data.get('battery_level')
            if battery_level is not None and battery_level < 20:
                alerts.append({
                    'type': 'battery_low',
                    'severity': 'medium',
                    'title': 'Low Battery',
                    'message': f'Device battery is at {battery_level}%',
                })

            # Check storage space
            storage_free = security_data.get('storage_free_gb')
            if storage_free is not None and storage_free < 1:
                alerts.append({
                    'type': 'storage_full',
                    'severity': 'high',
                    'title': 'Low Storage Space',
                    'message': f'Device has only {storage_free}GB free storage',
                })

            # Check network security
            network_type = security_data.get('network_type')
            if network_type == 'unknown':
                alerts.append({
                    'type': 'network_issue',
                    'severity': 'low',
                    'title': 'Network Issue',
                    'message': 'Device network connection is unstable',
                })

            # Create alerts in database
            for alert_data in alerts:
                DeviceAlert.objects.create(
                    device=device,
                    alert_type=alert_data['type'],
                    severity=alert_data['severity'],
                    title=alert_data['title'],
                    message=alert_data['message'],
                    data=security_data
                )

        except Device.DoesNotExist:
            pass

        return alerts

    @staticmethod
    def get_device_analytics(device_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get analytics data for a device.

        Args:
            device_id: Device ID
            days: Number of days to look back

        Returns:
            Analytics data
        """
        try:
            device = Device.objects.get(device_id=device_id)

            # Get date range
            end_date = timezone.now().date()
            start_date = end_date - timezone.timedelta(days=days)

            # Aggregate analytics
            analytics = DeviceAnalytics.objects.filter(
                device=device,
                date__range=[start_date, end_date]
            ).aggregate(
                total_opens=models.Sum('app_open_count'),
                total_sessions=models.Sum('session_count'),
                total_location_updates=models.Sum('location_updates'),
                total_qr_scans=models.Sum('qr_scans'),
                total_attendance_marks=models.Sum('attendance_marks'),
            )

            # Get recent locations
            recent_locations = DeviceLocation.objects.filter(
                device=device,
                timestamp__date__gte=start_date
            ).order_by('-timestamp')[:10]

            return {
                'device_info': {
                    'device_id': device.device_id,
                    'device_name': device.device_name,
                    'device_type': device.device_type,
                    'os': device.os,
                    'app_version': device.app_version,
                },
                'analytics': analytics,
                'recent_locations': [
                    {
                        'latitude': loc.latitude,
                        'longitude': loc.longitude,
                        'timestamp': loc.timestamp,
                        'accuracy': loc.accuracy,
                    } for loc in recent_locations
                ],
                'alerts_count': device.alerts.filter(
                    created_at__date__gte=start_date,
                    is_resolved=False
                ).count()
            }

        except Device.DoesNotExist:
            return {}

    @staticmethod
    def deactivate_device(device_id: str, reason: str = "") -> bool:
        """
        Deactivate a device.

        Args:
            device_id: Device ID
            reason: Reason for deactivation

        Returns:
            True if device was deactivated, False otherwise
        """
        try:
            device = Device.objects.get(device_id=device_id)
            device.status = 'inactive'
            device.save()

            # End any active sessions
            DeviceSession.objects.filter(
                device=device,
                is_active=True
            ).update(
                is_active=False,
                ended_at=timezone.now()
            )

            # Create deactivation alert
            DeviceAlert.objects.create(
                device=device,
                alert_type='device_change',
                severity='medium',
                title='Device Deactivated',
                message=f'Device has been deactivated. Reason: {reason}',
                data={'reason': reason}
            )

            return True

        except Device.DoesNotExist:
            return False

    @staticmethod
    def get_device_health_score(device_id: str) -> Dict[str, Any]:
        """
        Calculate a health score for the device.

        Args:
            device_id: Device ID

        Returns:
            Health score data
        """
        try:
            device = Device.objects.get(device_id=device_id)

            score = 100
            issues = []

            # Check if device is trusted
            if not device.is_trusted:
                score -= 20
                issues.append('Device not trusted')

            # Check recent activity
            days_since_last_seen = (timezone.now() - device.last_seen).days
            if days_since_last_seen > 7:
                score -= 30
                issues.append(f'Inactive for {days_since_last_seen} days')

            # Check unresolved alerts
            unresolved_alerts = device.alerts.filter(is_resolved=False).count()
            if unresolved_alerts > 0:
                score -= min(unresolved_alerts * 10, 40)
                issues.append(f'{unresolved_alerts} unresolved alerts')

            # Check app version
            if device.app_version:
                # This would compare with latest version
                pass

            score = max(0, score)

            return {
                'score': score,
                'status': 'healthy' if score >= 80 else 'warning' if score >= 60 else 'critical',
                'issues': issues
            }

        except Device.DoesNotExist:
            return {
                'score': 0,
                'status': 'unknown',
                'issues': ['Device not found']
            }

    @staticmethod
    def cleanup_old_data(days: int = 90) -> Dict[str, int]:
        """
        Clean up old device data.

        Args:
            days: Number of days to keep data

        Returns:
            Cleanup statistics
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days)

        # Delete old locations
        old_locations = DeviceLocation.objects.filter(timestamp__lt=cutoff_date)
        locations_deleted = old_locations.count()
        old_locations.delete()

        # Delete old sessions
        old_sessions = DeviceSession.objects.filter(started_at__lt=cutoff_date)
        sessions_deleted = old_sessions.count()
        old_sessions.delete()

        # Delete old analytics
        old_analytics = DeviceAnalytics.objects.filter(date__lt=cutoff_date)
        analytics_deleted = old_analytics.count()
        old_analytics.delete()

        return {
            'locations_deleted': locations_deleted,
            'sessions_deleted': sessions_deleted,
            'analytics_deleted': analytics_deleted,
        }
