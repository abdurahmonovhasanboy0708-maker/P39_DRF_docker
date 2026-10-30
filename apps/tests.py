from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.models import Calculation


class CalculatorTests(TestCase):
    base = '/api/v1/'

    def test_path_add(self):
        r = self.client.get(self.base + 'calculator/path/2/3')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['result'], 5)

    def test_path_operation(self):
        r = self.client.get(self.base + 'calculator/path/mul/4/5')
        self.assertEqual(r.json()['result'], 20)

    def test_path_unknown_operation(self):
        r = self.client.get(self.base + 'calculator/path/xyz/4/5')
        self.assertEqual(r.status_code, 400)

    def test_query_ok(self):
        r = self.client.get(self.base + 'calculator/query', {'n1': 10, 'n2': 4, 'operation': 'sub'})
        self.assertEqual(r.json()['result'], 6)

    def test_query_invalid(self):
        r = self.client.get(self.base + 'calculator/query', {'n1': 'abc', 'n2': 1})
        self.assertEqual(r.status_code, 400)

    def test_query_missing(self):
        r = self.client.get(self.base + 'calculator/query')
        self.assertEqual(r.status_code, 400)

    def test_division_by_zero(self):
        r = self.client.get(self.base + 'calculator/path/div/1/0')
        self.assertEqual(r.status_code, 400)

    def test_factorial_fibonacci_prime(self):
        self.assertEqual(self.client.get(self.base + 'math/factorial/5').json()['result'], 120)
        self.assertEqual(self.client.get(self.base + 'math/fibonacci/10').json()['result'], 55)
        self.assertTrue(self.client.get(self.base + 'math/prime', {'n': 97}).json()['is_prime'])
        self.assertFalse(self.client.get(self.base + 'math/prime', {'n': 1}).json()['is_prime'])

    def test_history(self):
        self.client.get(self.base + 'calculator/path/1/2')
        self.client.get(self.base + 'calculator/path/mul/2/3')
        self.assertEqual(Calculation.objects.count(), 2)
        self.assertEqual(self.client.get(self.base + 'history').json()['count'], 2)
        # filter
        r = self.client.get(self.base + 'history', {'operation': 'mul'}).json()
        self.assertEqual(r['count'], 1)

    def test_history_clear_requires_login(self):
        self.client.get(self.base + 'calculator/path/1/2')
        self.assertIn(self.client.delete(self.base + 'history/clear').status_code, (401, 403))
        self.assertEqual(Calculation.objects.count(), 1)
        user = get_user_model().objects.create_user('tester', password='pass12345')
        self.client.force_login(user)
        self.assertEqual(self.client.delete(self.base + 'history/clear').status_code, 204)
        self.assertEqual(Calculation.objects.count(), 0)

    def test_health(self):
        self.assertEqual(self.client.get(self.base + 'health/').json(), {'status': 'ok'})