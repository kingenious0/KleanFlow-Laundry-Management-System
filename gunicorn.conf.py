"""
Gunicorn WSGI Production Server Configuration for KleanFlow Laundry Management System.
"""

import os
import multiprocessing

# Network Interface & Port Binding
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")

# Worker Processes & Concurrency
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", 2))
worker_connections = 1000

# Timeouts & Keep-Alive
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
keepalive = 5

# Logging
os.makedirs("logs", exist_ok=True)
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process Naming
proc_name = "kleanflow_app"
daemon = False
