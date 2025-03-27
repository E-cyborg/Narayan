import os
n=input("port :") or "8000"
os.system(f"python3 manage.py runserver {n}")
