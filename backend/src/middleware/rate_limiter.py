import time
from typing import Dict, Optional
from collections import defaultdict, deque
from fastapi import Request, HTTPException
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Simple in-memory rate limiter to prevent abuse of AI services
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if the request is allowed based on rate limit
        """
        current_time = time.time()

        # Clean old requests outside the window
        while (self.requests[identifier] and
               current_time - self.requests[identifier][0] > self.window_seconds):
            self.requests[identifier].popleft()

        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True

        return False

    def get_reset_time(self, identifier: str) -> Optional[float]:
        """
        Get the time when the rate limit will reset
        """
        if not self.requests[identifier]:
            return None

        oldest_request = self.requests[identifier][0]
        return oldest_request + self.window_seconds


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)  # 10 requests per minute per user


async def check_rate_limit(request: Request, user_id: str = None) -> bool:
    """
    Check rate limit for the given user or IP address
    """
    # Use user ID if available, otherwise use IP address
    identifier = user_id or request.client.host

    if not rate_limiter.is_allowed(identifier):
        reset_time = rate_limiter.get_reset_time(identifier)
        if reset_time:
            retry_after = int(reset_time - time.time())
        else:
            retry_after = rate_limiter.window_seconds

        logger.warning(f"Rate limit exceeded for {identifier}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "retry_after_seconds": retry_after
            }
        )

    return True


def get_ai_service_rate_limiter():
    """
    Get a rate limiter specifically for AI service calls
    """
    # More restrictive rate limit for AI calls due to cost
    return RateLimiter(max_requests=5, window_seconds=60)  # 5 AI calls per minute