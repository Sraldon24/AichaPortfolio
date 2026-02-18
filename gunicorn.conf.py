# Use WEB_CONCURRENCY if set, otherwise default to 4 workers
# This prevents excessive memory usage in containerized environments where cpu_count() might report host CPUs.
import os
workers = int(os.environ.get('WEB_CONCURRENCY', 4))
threads = int(os.environ.get('PYTHON_MAX_THREADS', 1))

timeout = int(os.environ.get('WEB_TIMEOUT', 120))
keepalive = int(os.environ.get('WEB_KEEPALIVE', 5))

max_requests = 1000
max_requests_jitter = 50
capture_output = True
enable_stdio_inheritance = True
