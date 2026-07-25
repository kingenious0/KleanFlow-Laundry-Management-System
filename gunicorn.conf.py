"""
KleanFlow Laundry Management System
Gunicorn WSGI Production Server Configuration
"""

import os
import multiprocessing

# ── Network Binding ────────────────────────────────────────────────────────────
# Bind address — override with GUNICORN_BIND env var (e.g. "0.0.0.0:8000")
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")

# ── Worker Configuration ───────────────────────────────────────────────────────
# Recommended: (2 × CPU cores) + 1
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

# Thread-based worker class (suitable for Flask; sync is also acceptable)
worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", 2))

# Maximum simultaneous connections per worker
worker_connections = 1000

# ── Timeouts ───────────────────────────────────────────────────────────────────
# Seconds before killing a hung worker
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))

# Seconds to wait for the next request on a keep-alive connection
keepalive = 5

# Graceful restart timeout
graceful_timeout = 30

# ── Logging ────────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)

# Write access log to file (use "-" to write to stdout)
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "logs/access.log")

# Write error log to file (use "-" to write to stderr)
errorlog = os.getenv("GUNICORN_ERROR_LOG", "logs/error.log")

# Log level: debug, info, warning, error, critical
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# Apache Combined Log Format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sμs'

# ── Security ───────────────────────────────────────────────────────────────────
# Limit HTTP request line size
limit_request_line = 4096

# Limit HTTP header count
limit_request_fields = 100

# Limit HTTP header size
limit_request_field_size = 8190

# ── Process Management ─────────────────────────────────────────────────────────
# Name appearing in process list (useful for systemd/supervisor monitoring)
proc_name = "kleanflow"

# Run in foreground (set True only when daemonising manually)
daemon = False

# Pre-load the application code before forking workers (reduces memory if using Copy-on-Write)
preload_app = True

# ── Hooks ─────────────────────────────────────────────────────────────────────
def on_starting(server):
    """Log startup message."""
    server.log.info("KleanFlow WSGI server starting on %s", bind)


def worker_exit(server, worker):
    """Log worker exit."""
    server.log.info("Worker %s exiting (pid: %s)", worker, worker.pid)
