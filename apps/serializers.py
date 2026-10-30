from rest_framework import serializers

from apps.models import Calculation

OPERATION_CHOICES = ['add', 'sub', 'mul', 'div', 'pow', 'mod', 'gcd', 'lcm']


class CalculatorQuerySerializer(serializers.Serializer):
    n1 = serializers.IntegerField(help_text='Son 1')
    n2 = serializers.IntegerField(help_text='Son 2')
    operation = serializers.ChoiceField(
        choices=OPERATION_CHOICES, default='add', required=False,
        help_text='Amal turi (default: add)',
    )


class NumberQuerySerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=0, help_text="Manfiy bo'lmagan butun son")


class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = ['id', 'operation', 'n1', 'n2', 'result', 'created_at']
