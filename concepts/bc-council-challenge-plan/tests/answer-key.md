# Answer key: user-cache plan

Never copy this file into a consumer's scratch dir. Planted holes in
[practice/docs/user-cache-plan.md](practice/docs/user-cache-plan.md):

1. **Wrong premise** (section 4): "`store.get_user` already returns `None` for an unknown user".
   It raises `KeyError`: `users/store.py:11` `return _USERS[user_id]`.
2. **Missing case** (section 4): no invalidation when a user changes. `change_email`
   (`users/handlers.py:18-20`) and `remove_user` (`users/handlers.py:23-25`) would leave stale
   entries; `test_change_email` (`tests/test_handlers.py:13-15`) would then fail.
3. **Cheaper path** (section 3): `users/cache.py:6` `TTLCache` already has get, set with expiry
   and `invalidate`; no new `UserCache` is needed.
4. **Risky order** (sections 2 and 5): deleting `lookup_user` before moving `users/mobile.py:7`
   breaks the mobile app; move callers first, then delete.
