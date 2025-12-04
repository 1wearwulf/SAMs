"""
Anti-cheating services for attendance validation.
"""
from typing import Dict, Any, List, Optional, Tuple
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from utils.device_fingerprint import validate_device_consistency
from utils.geolocation import calculate_distance
from core.constants import (
    GRACE_PERIOD_MINUTES, DEFAULT_GEOFENCE_RADIUS_METERS,
    MAX_GEOFENCE_RADIUS_METERS
)


class AntiCheatService:
    """
    Service for detecting and preventing attendance cheating.
    """

    @staticmethod
    def analyze_attendance_pattern(
        user_id: int,
        session_id: int,
        attendance_time: timezone.datetime,
        device_fingerprint: str,
        location_coords: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """
        Analyze attendance marking for suspicious patterns.

        Args:
            user_id: User ID
            session_id: Session ID
            attendance_time: Time attendance was marked
            device_fingerprint: Device fingerprint
            location_coords: User's location coordinates

        Returns:
            Analysis result with flags and confidence score
        """
        flags = []
        confidence = 1.0
        severity = 'low'

        # Check device consistency
        device_check = AntiCheatService._check_device_consistency(user_id, device_fingerprint)
        if not device_check['is_valid']:
            flags.append({
                'type': 'device_mismatch',
                'description': device_check['message'],
                'severity': 'medium'
            })
            confidence *= 0.7
            severity = 'medium'

        # Check timing patterns
        timing_check = AntiCheatService._check_timing_patterns(user_id, session_id, attendance_time)
        if timing_check['suspicious']:
            flags.extend(timing_check['flags'])
            confidence *= timing_check['confidence_multiplier']
            if timing_check['severity'] == 'high':
                severity = 'high'

        # Check location anomalies
        if location_coords:
            location_check = AntiCheatService._check_location_anomalies(
                user_id, session_id, location_coords, attendance_time
            )
            if location_check['suspicious']:
                flags.extend(location_check['flags'])
                confidence *= location_check['confidence_multiplier']
                if location_check['severity'] == 'high':
                    severity = 'high'

        # Check for proxy attendance patterns
        proxy_check = AntiCheatService._check_proxy_patterns(user_id, session_id, attendance_time)
        if proxy_check['suspicious']:
            flags.extend(proxy_check['flags'])
            confidence *= proxy_check['confidence_multiplier']
            if proxy_check['severity'] == 'critical':
                severity = 'critical'

        return {
            'is_suspicious': len(flags) > 0,
            'flags': flags,
            'confidence': confidence,
            'severity': severity,
            'recommendation': AntiCheatService._get_recommendation(confidence, flags)
        }

    @staticmethod
    def _check_device_consistency(user_id: int, device_fingerprint: str) -> Dict[str, Any]:
        """
        Check if device fingerprint is consistent with user's history.
        """
        # Get user's recent device fingerprints
        cache_key = f"user_devices_{user_id}"
        recent_devices = cache.get(cache_key, [])

        if not recent_devices:
            # First device, consider valid
            recent_devices.append(device_fingerprint)
            cache.set(cache_key, recent_devices, timeout=86400 * 30)  # 30 days
            return {'is_valid': True, 'message': 'First device registration'}

        # Check if current fingerprint matches recent ones
        matches = [fp for fp in recent_devices if fp == device_fingerprint]

        if matches:
            return {'is_valid': True, 'message': 'Device fingerprint matches history'}
        else:
            # Add to recent devices (limit to 5)
            recent_devices.append(device_fingerprint)
            recent_devices = recent_devices[-5:]
            cache.set(cache_key, recent_devices, timeout=86400 * 30)

            return {
                'is_valid': False,
                'message': f'Device fingerprint mismatch. Known devices: {len(recent_devices)}'
            }

    @staticmethod
    def _check_timing_patterns(
        user_id: int,
        session_id: int,
        attendance_time: timezone.datetime
    ) -> Dict[str, Any]:
        """
        Check for suspicious timing patterns.
        """
        flags = []
        confidence_multiplier = 1.0
        max_severity = 'low'

        # Check if attendance is marked too early or too late
        session_start = attendance_time.replace(hour=9, minute=0, second=0, microsecond=0)  # Assume 9 AM start
        session_end = session_start.replace(hour=17, minute=0)  # Assume 5 PM end

        if attendance_time < session_start - timedelta(hours=1):
            flags.append({
                'type': 'too_early',
                'description': 'Attendance marked more than 1 hour before session start',
                'severity': 'medium'
            })
            confidence_multiplier *= 0.8
            max_severity = 'medium'

        if attendance_time > session_end + timedelta(hours=2):
            flags.append({
                'type': 'too_late',
                'description': 'Attendance marked more than 2 hours after session end',
                'severity': 'high'
            })
            confidence_multiplier *= 0.6
            max_severity = 'high'

        # Check for bulk attendance marking (many users at exact same time)
        time_window = timedelta(minutes=1)
        cache_key = f"bulk_attendance_{session_id}_{attendance_time.strftime('%Y%m%d_%H%M')}"
        bulk_count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, bulk_count, timeout=300)  # 5 minutes

        if bulk_count > 10:  # More than 10 attendances in 1 minute
            flags.append({
                'type': 'bulk_marking',
                'description': f'Bulk attendance marking detected ({bulk_count} in 1 minute)',
                'severity': 'high'
            })
            confidence_multiplier *= 0.5
            max_severity = 'high'

        return {
            'suspicious': len(flags) > 0,
            'flags': flags,
            'confidence_multiplier': confidence_multiplier,
            'severity': max_severity
        }

    @staticmethod
    def _check_location_anomalies(
        user_id: int,
        session_id: int,
        location_coords: Tuple[float, float],
        attendance_time: timezone.datetime
    ) -> Dict[str, Any]:
        """
        Check for location-based anomalies.
        """
        flags = []
        confidence_multiplier = 1.0
        max_severity = 'low'

        # Get user's location history
        history_key = f"user_location_history_{user_id}"
        location_history = cache.get(history_key, [])

        # Check for impossible travel speeds
        if location_history:
            last_location = location_history[-1]
            time_diff = attendance_time - last_location['timestamp']
            distance = calculate_distance(location_coords, last_location['coords'])

            # Speed in m/s (rough calculation)
            if time_diff.total_seconds() > 0:
                speed = distance / time_diff.total_seconds()

                # If speed > 100 m/s (360 km/h), flag as suspicious
                if speed > 100:
                    flags.append({
                        'type': 'impossible_speed',
                        'description': f'Impossible travel speed: {speed:.1f} m/s',
                        'severity': 'high'
                    })
                    confidence_multiplier *= 0.4
                    max_severity = 'high'

        # Update location history
        location_history.append({
            'coords': location_coords,
            'timestamp': attendance_time
        })
        location_history = location_history[-10:]  # Keep last 10 locations
        cache.set(history_key, location_history, timeout=86400 * 7)  # 7 days

        return {
            'suspicious': len(flags) > 0,
            'flags': flags,
            'confidence_multiplier': confidence_multiplier,
            'severity': max_severity
        }

    @staticmethod
    def _check_proxy_patterns(
        user_id: int,
        session_id: int,
        attendance_time: timezone.datetime
    ) -> Dict[str, Any]:
        """
        Check for proxy attendance patterns.
        """
        flags = []
        confidence_multiplier = 1.0
        max_severity = 'low'

        # Check for same IP marking multiple attendances
        ip_key = f"ip_attendance_{session_id}"
        ip_counts = cache.get(ip_key, {})

        # This would need actual IP tracking, simplified for now

        # Check for rapid successive markings
        user_timing_key = f"user_timing_{user_id}"
        last_marking = cache.get(user_timing_key)

        if last_marking:
            time_diff = (attendance_time - last_marking).total_seconds()
            if time_diff < 30:  # Less than 30 seconds since last marking
                flags.append({
                    'type': 'rapid_marking',
                    'description': f'Attendance marked {time_diff:.1f}s after previous marking',
                    'severity': 'critical'
                })
                confidence_multiplier *= 0.3
                max_severity = 'critical'

        cache.set(user_timing_key, attendance_time, timeout=3600)  # 1 hour

        return {
            'suspicious': len(flags) > 0,
            'flags': flags,
            'confidence_multiplier': confidence_multiplier,
            'severity': max_severity
        }

    @staticmethod
    def _get_recommendation(confidence: float, flags: List[Dict[str, Any]]) -> str:
        """
        Get recommendation based on confidence and flags.
        """
        if confidence > 0.8:
            return 'Allow attendance'
        elif confidence > 0.6:
            return 'Flag for manual review'
        elif confidence > 0.4:
            return 'Require additional verification'
        else:
            return 'Reject attendance - high risk of cheating'

    @staticmethod
    def report_suspicious_activity(
        user_id: int,
        session_id: int,
        flags: List[Dict[str, Any]],
        severity: str
    ) -> None:
        """
        Report suspicious activity for monitoring.

        Args:
            user_id: User ID
            session_id: Session ID
            flags: List of flags
            severity: Severity level
        """
        # In a real implementation, this would:
        # 1. Create database records
        # 2. Send notifications to administrators
        # 3. Log to monitoring systems
        # 4. Trigger automated responses

        report = {
            'user_id': user_id,
            'session_id': session_id,
            'flags': flags,
            'severity': severity,
            'timestamp': timezone.now(),
            'reported': True
        }

        # Cache for immediate access
        cache_key = f"suspicious_activity_{user_id}_{session_id}"
        cache.set(cache_key, report, timeout=86400 * 7)  # 7 days

        # Add to global suspicious activities list
        global_key = "suspicious_activities"
        activities = cache.get(global_key, [])
        activities.append(report)
        activities = activities[-100:]  # Keep last 100
        cache.set(global_key, activities, timeout=86400 * 30)  # 30 days

    @staticmethod
    def get_suspicious_activities(limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent suspicious activities.

        Args:
            limit: Maximum number of activities to return

        Returns:
            List of suspicious activity reports
        """
        global_key = "suspicious_activities"
        activities = cache.get(global_key, [])
        return activities[-limit:]

    @staticmethod
    def clear_user_cache(user_id: int) -> None:
        """
        Clear cached data for a user (useful for testing or resets).

        Args:
            user_id: User ID
        """
        cache_keys = [
            f"user_devices_{user_id}",
            f"user_location_history_{user_id}",
            f"user_timing_{user_id}"
        ]

        for key in cache_keys:
            cache.delete(key)
