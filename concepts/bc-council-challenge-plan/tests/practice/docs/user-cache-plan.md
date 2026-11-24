# Plan: cache user lookups

Status: draft

## 1. Why

`show_user` reads the store on every request. Profile pages call it many times per second.

## 2. Remove the old endpoint

Delete `lookup_user` from `users/handlers.py`; it duplicates `show_user`.

## 3. Write a cache

Write a new `UserCache` class in `users/user_cache.py` with a dictionary and an expiry time per entry.

## 4. Use the cache in `show_user`

`show_user` checks `UserCache` first and falls back to `store.get_user`.
`store.get_user` already returns `None` for an unknown user, so a miss for a missing user is cached as `None` like any other value.

## 5. Move the mobile app to `show_user`

Change `users/mobile.py` to call `show_user` instead of `lookup_user`.

## 6. Tests

Add a test that a second `show_user` call does not hit the store.
