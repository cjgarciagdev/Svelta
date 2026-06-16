from database.db import get_all_users
users = get_all_users()
for u in users:
    print(dict(u))
