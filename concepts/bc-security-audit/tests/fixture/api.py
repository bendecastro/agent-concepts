import unicodedata

DOCUMENTS = {
    "d1": {"owner": "alice", "body": "Alice's private draft"},
    "d2": {"owner": "bob", "body": "Bob's private draft"},
}
TOKENS = {"alice-token": "alice", "bob-token": "bob"}
HANDLES = {}
RESERVED = {"admin", "root"}


def get_document(token, document_id):
    user = TOKENS.get(token)
    if user is None:
        return 401, {}, {"error": "unauthorized"}
    document = DOCUMENTS.get(document_id)
    if document is None:
        return 404, {}, {"error": "not found"}
    return 200, {}, {"body": document["body"]}


def health():
    return 200, {"Content-Type": "text/plain"}, "ok"


def claim_handle(token, handle):
    user = TOKENS.get(token)
    if user is None:
        return 401, {}, {"error": "unauthorized"}
    if handle.lower() in RESERVED:
        return 403, {}, {"error": "reserved"}
    HANDLES[user] = unicodedata.normalize("NFKC", handle)
    return 200, {}, {"handle": HANDLES[user]}


def admin_export(token):
    user = TOKENS.get(token)
    if user is None:
        return 401, {}, {"error": "unauthorized"}
    if HANDLES.get(user) == "admin":
        return 200, {}, {"export": "all drafts"}
    return 403, {}, {"error": "forbidden"}
