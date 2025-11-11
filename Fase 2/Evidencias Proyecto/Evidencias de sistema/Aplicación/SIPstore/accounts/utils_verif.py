import random
import time
from django.utils import timezone
from django.conf import settings

SESSION_KEY = "pw_reset"

def _now_ts():
    return int(time.time())

def create_code_session(request, user_id, method, ttl_seconds=None):
    if ttl_seconds is None:
        ttl_seconds = getattr(settings, "PASSWORD_RESET_TTL", 120)
    code = f"{random.randint(0, 999999):06d}"
    expires_at = _now_ts() + int(ttl_seconds)
    request.session[SESSION_KEY] = {
        "user_id": int(user_id),
        "method": method,
        "code": code,
        "expires_at": expires_at,
        "attempts": 0,
        "used": False,
        "sent_at": _now_ts(),
    }
    request.session.modified = True
    return code

def get_data(request):
    return request.session.get(SESSION_KEY)

def clear_session(request):
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
        request.session.modified = True

def mark_used(request):
    data = get_data(request)
    if data:
        data["used"] = True
        request.session[SESSION_KEY] = data
        request.session.modified = True

def increment_attempts(request):
    data = get_data(request)
    if data:
        data["attempts"] = data.get("attempts", 0) + 1
        request.session[SESSION_KEY] = data
        request.session.modified = True

def is_expired(data):
    if not data:
        return True
    return int(time.time()) > int(data.get("expires_at", 0))

def remaining_seconds(data):
    if not data:
        return 0
    rem = int(data.get("expires_at", 0)) - int(time.time())
    return max(0, rem)
