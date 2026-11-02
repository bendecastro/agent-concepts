import importlib

DOCUMENTS = {
    "d1": {"owner": "alice", "body": "Alice's private draft"},
    "d2": {"owner": "bob", "body": "Bob's private draft"},
}
TOKENS = {"alice-token": "alice", "bob-token": "bob"}


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


def preview(token, expression):
    user = TOKENS.get(token)
    if user is None:
        return 401, {}, {"error": "unauthorized"}
    renderer = importlib.import_module("preview_engine")
    return 200, {}, {"result": renderer.render(expression)}
