"""Request handlers."""

from users import store
from users.cache import TTLCache

_settings_cache = TTLCache(ttl_seconds=300)


def show_user(user_id):
    return store.get_user(user_id)


def lookup_user(user_id):
    """Old endpoint, kept for the mobile app."""
    return show_user(user_id)


def change_email(user_id, email):
    store.update_email(user_id, email)
    return {"ok": True}


def remove_user(user_id):
    store.delete_user(user_id)
    return {"ok": True}


def settings():
    value = _settings_cache.get("settings")
    if value is None:
        value = {"theme": "light"}
        _settings_cache.set("settings", value)
    return value
