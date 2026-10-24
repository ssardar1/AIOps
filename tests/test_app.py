import unittest
from app import app


class AppTests(unittest.TestCase):
    def test_page_and_instrumentation(self):
        with app.test_client() as client:
            self.assertIn(b'Generate a signal', client.get('/').data)
            before = client.get('/api/stats').json['completed']
            result = client.post('/api/jobs')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json['completed'], before + 1)
            self.assertEqual(client.get('/health').json, {'status': 'ok'})
            metrics = client.get('/metrics')
            self.assertIn('text/plain', metrics.content_type)
            self.assertIn(f'demo_jobs_total {float(before + 1)}'.encode(), metrics.data)
            self.assertIn(b'demo_http_requests_total{method="POST",route="/api/jobs",status="200"}', metrics.data)
            self.assertIn(b'demo_http_request_duration_seconds_bucket', metrics.data)
            self.assertNotIn(b'route="/metrics"', metrics.data)


if __name__ == '__main__':
    unittest.main()
