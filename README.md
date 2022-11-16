##Please install the pack: python -m pip install faker
install->  pip install pip --upgrade

###Remenber in the file /Projeto1/venv/lib/python3.11/site-packages/django/core/servers/basehttp.py you have to change the line 42
#OLD: app_path = getattr(settings, "WSGI_APPLICATION")
#NEW: app_path = getattr(settings, "WSGI_APPLICATION").strip()