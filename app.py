import os
import time

from flask import Flask, Response, g, jsonify, render_template, request
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
registry = CollectorRegistry()
requests = Counter('demo_http_requests_total', 'Completed HTTP requests', ['method', 'route', 'status'], registry=registry)
latency = Histogram('demo_http_request_duration_seconds', 'HTTP request duration', ['route'], registry=registry)
jobs = Counter('demo_jobs_total', 'Demo jobs completed', registry=registry)


@app.before_request
def begin_request():
    g.started = time.perf_counter()


@app.after_request
def record_request(response):
    if request_route() != '/metrics':
        route = request_route()
        requests.labels(request.method, route, str(response.status_code)).inc()
        latency.labels(route).observe(time.perf_counter() - g.started)
    return response


def request_route():
    return request.url_rule.rule if request.url_rule else 'unmatched'


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/jobs')
def run_job():
    jobs.inc()
    return jsonify(message='Demo job completed', completed=int(jobs._value.get()))


@app.get('/api/stats')
def stats():
    return jsonify(completed=int(jobs._value.get()))


@app.get('/metrics')
def metrics():
    return Response(generate_latest(registry), content_type=CONTENT_TYPE_LATEST)


@app.get('/health')
def health():
    return jsonify(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
