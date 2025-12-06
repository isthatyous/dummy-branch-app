from flask import Blueprint, Response, request, g
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

bp = Blueprint("metrics", __name__)

# Define endpoints to exclude from metrics
EXCLUDED_PATHS = {"/metrics", "/health", "/favicon.ico"}

# Metrics - Using Histogram instead of Summary for better percentile support
REQUEST_COUNT = Counter(
    "request_count",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

def setup_metrics(app):
    """Setup metrics tracking for the Flask application"""
    
    @app.before_request
    def before_request():
        """Track request start time, skip excluded paths"""
        if request.path in EXCLUDED_PATHS:
            return
        g.start_time = time.perf_counter()
    
    @app.after_request
    def after_request(response):
        """Record metrics after request completes"""
        if request.path in EXCLUDED_PATHS:
            return response
        
        # Record request count with status code
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        
        # Record latency if start_time was set
        if hasattr(g, 'start_time'):
            latency = time.perf_counter() - g.start_time
            REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        
        return response

@bp.route("/metrics")
def metrics():
    """Expose Prometheus metrics"""
    return Response(generate_latest(REGISTRY), mimetype="text/plain")