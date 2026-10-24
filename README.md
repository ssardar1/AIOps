# Signal: Prometheus sample dashboard

A Flask webpage with a working demo-job button, live job count, HTTP request counters, and latency histograms. `/metrics` exposes real application measurements; the page does not query a Prometheus server.

## Run locally

Requires Python 3.12.

```sh
cd /workspace/AIOps
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 4 app:app
```

Visit port 8000 in your local deployment. Run `.venv/bin/python -m unittest discover -s tests -v` for the functional test.

## Run with Prometheus

With Docker and Docker Compose installed:

```sh
docker compose up --build -d
```

The Docker app is available at http://localhost:8100 (host port 8100 maps to container port 8000); Prometheus runs on port 9090. With standalone Homebrew Compose, use `docker-compose up --build -d`. In Prometheus, check **Status → Targets** for `signal-demo`, run jobs on the webpage, and query `demo_jobs_total` or the PromQL examples shown on the page. Allow a few scrape intervals before querying rates.

For an existing Prometheus server, add a scrape target pointing at this application's reachable hostname and port (for example `your-app-host:8100` for this Docker deployment) with `metrics_path: /metrics`. The supplied `app:8000` target resolves only within Docker Compose.

Metrics are held in memory and reset when the app restarts. Keep one Gunicorn worker: multiple workers require Prometheus multiprocess configuration. No credentials or external services are needed for the app itself. This is a development demo; restrict access and add authentication before exposing it publicly. Polls of `/api/stats` count as HTTP traffic; scrapes of `/metrics` are excluded.
