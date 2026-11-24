"""Mobile app routes; still call the old endpoint."""

from users import handlers


def mobile_profile(user_id):
    return handlers.lookup_user(user_id)
