workers = 4  # Number of worker processes
bind = '0.0.0.0:8000'  # Address and port to bind to
timeout = 120  # Worker timeout in seconds
accesslog = '-'  # Log to stdout
errorlog = '-'  # Log errors to stdout
capture_output = True  # Capture stdout and stderr to the error log

# Set the maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 100

# Gunicorn user and group
#user = 'your_user'
#group = 'your_group'

# Gunicorn process name (change to a descriptive name)
proc_name = 'webNUT'

# Set the location of the Gunicorn process ID file
#pidfile = '/path/to/gunicorn.pid'

# Daemonize the Gunicorn process (run in the background)
#daemon = True

# Set the Python executable path (if using a virtual environment)
# pythonpath = '/path/to/your/virtualenv/bin/python'

# Enable the Gunicorn master process to restart workers gracefully
preload_app = True

# Location of your WSGI application
#pythonpath = '/path/to/your/django/project'
#working_dir = '/path/to/your/django/project'

# Specify the Django application (wsgi.py) and its callable object
app_uri = 'webNUT.wsgi:application'

# Enable and configure HTTP keep-alive
keepalive = 2
keepalive_requests = 100
keepalive_timeout = 5

# Set the maximum number of simultaneous clients Gunicorn should accept
backlog = 2048

# Enable greenlet support for improved concurrency
worker_class = 'gevent'

# Use a Unix socket instead of TCP/IP
# bind = 'unix:/path/to/your/socket.sock'

# Environment variables (you can specify additional environment variables here)
# env = 'DJANGO_SETTINGS_MODULE=your_project.settings'

# Additional security settings (e.g., limit request header size)
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190
