"""In-memory user store."""

_USERS = {}


def add_user(user_id, name, email):
    _USERS[user_id] = {"id": user_id, "name": name, "email": email}


def get_user(user_id):
    return _USERS[user_id]


def update_email(user_id, email):
    _USERS[user_id]["email"] = email


def delete_user(user_id):
    del _USERS[user_id]
