"""
Redis utility functions for SAMS.
"""
import redis
import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from functools import wraps

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client wrapper with connection pooling."""
    
    _connections = {}
    
    @classmethod
    def get_connection(cls, db=0):
        """Get or create Redis connection."""
        if db not in cls._connections:
            try:
                cls._connections[db] = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=db,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_keepalive=True,
                    retry_on_timeout=True,
                )
                # Test connection
                cls._connections[db].ping()
                logger.info(f"Connected to Redis DB {db}")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis DB {db}: {e}")
                return None
        
        return cls._connections[db]
    
    @classmethod
    def close_all(cls):
        """Close all Redis connections."""
        for db, conn in cls._connections.items():
            if conn:
                conn.close()
                logger.info(f"Closed Redis connection DB {db}")
        cls._connections.clear()

def cache_result(key_template, timeout=300, db=0):
    """
    Decorator to cache function results in Redis.
    
    Args:
        key_template: Template string for cache key
        timeout: Cache timeout in seconds
        db: Redis database number
    
    Example:
        @cache_result('user:{user_id}:profile', timeout=600)
        def get_user_profile(user_id):
            return User.objects.get(id=user_id)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = key_template.format(*args, **kwargs)
            
            # Try to get from cache
            redis_client = RedisClient.get_connection(db)
            if redis_client:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    try:
                        logger.debug(f"Cache hit: {cache_key}")
                        return json.loads(cached_data)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode cached data for {cache_key}")
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            if redis_client and result is not None:
                try:
                    serialized_data = json.dumps(result, default=str)
                    redis_client.setex(cache_key, timeout, serialized_data)
                    logger.debug(f"Cached result: {cache_key} for {timeout}s")
                except Exception as e:
                    logger.error(f"Failed to cache data for {cache_key}: {e}")
            
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern, db=0):
    """
    Invalidate cache keys matching pattern.
    
    Args:
        pattern: Redis pattern to match (e.g., 'user:*:profile')
        db: Redis database number
    """
    redis_client = RedisClient.get_connection(db)
    if not redis_client:
        return 0
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            deleted = redis_client.delete(*keys)
            logger.info(f"Invalidated {deleted} cache keys matching {pattern}")
            return deleted
    except Exception as e:
        logger.error(f"Failed to invalidate cache pattern {pattern}: {e}")
    
    return 0

def get_cache_stats(db=0):
    """
    Get Redis cache statistics.
    
    Returns:
        dict: Cache statistics
    """
    redis_client = RedisClient.get_connection(db)
    if not redis_client:
        return {}
    
    try:
        info = redis_client.info()
        stats = {
            'connected_clients': info.get('connected_clients', 0),
            'used_memory_human': info.get('used_memory_human', '0B'),
            'total_commands_processed': info.get('total_commands_processed', 0),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
            'uptime_in_seconds': info.get('uptime_in_seconds', 0),
            'db_size': redis_client.dbsize(),
        }
        
        # Calculate hit rate
        hits = stats['keyspace_hits']
        misses = stats['keyspace_misses']
        total = hits + misses
        stats['hit_rate'] = (hits / total * 100) if total > 0 else 0
        
        return stats
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        return {}

def set_user_session(user_id, session_data, timeout=3600):
    """
    Store user session data in Redis.
    
    Args:
        user_id: User ID
        session_data: Session data dictionary
        timeout: Session timeout in seconds
    
    Returns:
        bool: True if successful
    """
    redis_client = RedisClient.get_connection(2)  # Use sessions DB
    if not redis_client:
        return False
    
    try:
        key = f"session:user:{user_id}"
        serialized_data = json.dumps({
            'user_id': user_id,
            'data': session_data,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=timeout)).isoformat(),
        })
        redis_client.setex(key, timeout, serialized_data)
        return True
    except Exception as e:
        logger.error(f"Failed to set user session for {user_id}: {e}")
        return False

def get_user_session(user_id):
    """
    Get user session data from Redis.
    
    Args:
        user_id: User ID
    
    Returns:
        dict: Session data or None
    """
    redis_client = RedisClient.get_connection(2)
    if not redis_client:
        return None
    
    try:
        key = f"session:user:{user_id}"
        data = redis_client.get(key)
        if data:
            session = json.loads(data)
            # Check if session is expired
            expires_at = datetime.fromisoformat(session['expires_at'])
            if datetime.now() < expires_at:
                return session['data']
            else:
                # Clean up expired session
                redis_client.delete(key)
    except Exception as e:
        logger.error(f"Failed to get user session for {user_id}: {e}")
    
    return None
