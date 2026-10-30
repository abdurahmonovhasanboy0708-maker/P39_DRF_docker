from django.urls import path

from apps.views import (
    calculator_path, calculator_query, calculator_operation_path,
    factorial_view, prime_view, fibonacci_view,
    HistoryView, history_clear_view, health_view,
)

urlpatterns = [
    path('health/', health_view),

    path('calculator/path/<int:n1>/<int:n2>', calculator_path),
    path('calculator/path/<slug:operation>/<int:n1>/<int:n2>', calculator_operation_path),
    path('calculator/query', calculator_query),

    path('math/factorial/<int:n>', factorial_view),
    path('math/fibonacci/<int:n>', fibonacci_view),
    path('math/prime', prime_view),

    path('history', HistoryView.as_view()),
    path('history/clear', history_clear_view),
]