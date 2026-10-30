import math

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.models import Calculation
from apps.serializers import (
    CalculatorQuerySerializer,
    CalculationSerializer,
    NumberQuerySerializer,
)

MAX_POWER = 1000
MAX_FACTORIAL = 1000
MAX_FIBONACCI = 5000


def _error(message, code=status.HTTP_400_BAD_REQUEST):
    return Response({'error': message}, status=code)


def _power(a, b):
    if b < 0:
        raise ValueError("Daraja ko'rsatkichi manfiy bo'lmasligi kerak")
    if b > MAX_POWER:
        raise ValueError(f"Daraja ko'rsatkichi {MAX_POWER} dan oshmasligi kerak")
    return a ** b


def _div(a, b):
    if b == 0:
        raise ValueError("0 ga bo'lish mumkin emas")
    return a / b


def _mod(a, b):
    if b == 0:
        raise ValueError("0 ga bo'lish mumkin emas")
    return a % b


OPERATIONS = {
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
    'div': _div,
    'pow': _power,
    'mod': _mod,
    'gcd': lambda a, b: math.gcd(a, b),
    'lcm': lambda a, b: math.lcm(a, b),
}


def _compute(operation, n1, n2):
    """Hisoblaydi, tarixga yozadi va javob dict'ini qaytaradi."""
    result = OPERATIONS[operation](n1, n2)
    Calculation.objects.create(operation=operation, n1=n1, n2=n2, result=str(result))
    return {'operation': operation, 'n1': n1, 'n2': n2, 'result': result}


# ---------------------------------------------------------------- PATH
@extend_schema(summary="Ikki son yig'indisi (path)")
@api_view(['GET'])
@permission_classes([AllowAny])
def calculator_path(request, n1, n2):
    return Response(_compute('add', n1, n2), status=status.HTTP_200_OK)


@extend_schema(summary="Amal tanlab hisoblash (path)",
               description='operation: ' + ', '.join(OPERATIONS))
@api_view(['GET'])
@permission_classes([AllowAny])
def calculator_operation_path(request, operation, n1, n2):
    if operation not in OPERATIONS:
        return _error(f"Noma'lum amal. Mumkin: {', '.join(OPERATIONS)}")
    try:
        return Response(_compute(operation, n1, n2))
    except ValueError as e:
        return _error(str(e))


# --------------------------------------------------------------- QUERY
@extend_schema(parameters=[CalculatorQuerySerializer], summary='Kalkulyator (query)')
@api_view(['GET'])
@permission_classes([AllowAny])
def calculator_query(request):
    serializer = CalculatorQuerySerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(
            {'error': "n1 yoki n2 ga noto'g'ri qiymat berildi", 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = serializer.validated_data
    try:
        return Response(_compute(data.get('operation', 'add'), data['n1'], data['n2']))
    except ValueError as e:
        return _error(str(e))


# -------------------------------------------------------------- EXTRAS
@extend_schema(summary='Faktorial')
@api_view(['GET'])
@permission_classes([AllowAny])
def factorial_view(request, n):
    if n > MAX_FACTORIAL:
        return _error(f"n {MAX_FACTORIAL} dan oshmasligi kerak")
    result = math.factorial(n)
    Calculation.objects.create(operation='factorial', n1=n, result=str(result))
    return Response({'n': n, 'result': result})


@extend_schema(summary='Tub son tekshiruvi', parameters=[NumberQuerySerializer])
@api_view(['GET'])
@permission_classes([AllowAny])
def prime_view(request):
    serializer = NumberQuerySerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    n = serializer.validated_data['n']
    is_prime = n > 1 and all(n % i for i in range(2, math.isqrt(n) + 1))
    Calculation.objects.create(operation='prime', n1=n, result=str(is_prime))
    return Response({'n': n, 'is_prime': is_prime})


@extend_schema(summary='Fibonachchi soni')
@api_view(['GET'])
@permission_classes([AllowAny])
def fibonacci_view(request, n):
    if n > MAX_FIBONACCI:
        return _error(f"n {MAX_FIBONACCI} dan oshmasligi kerak")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    Calculation.objects.create(operation='fibonacci', n1=n, result=str(a))
    return Response({'n': n, 'result': a})


# ------------------------------------------------------------- HISTORY
@extend_schema(summary="Hisob-kitoblar tarixi (sahifalangan, ?operation=add bilan filtrlash)")
class HistoryView(generics.ListAPIView):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
    filterset_fields = ['operation']


@extend_schema(summary='Tarixni tozalash (login talab qilinadi)', responses={204: None})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def history_clear_view(request):
    Calculation.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(summary='Health check', responses={200: OpenApiTypes.OBJECT})
@api_view(['GET'])
@permission_classes([AllowAny])
def health_view(request):
    return Response({'status': 'ok'})