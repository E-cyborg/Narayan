import os
n=input("port :") or "8000"
os.system(f"python manage.py runserver {n}")
