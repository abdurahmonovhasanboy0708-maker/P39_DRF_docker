from django.db import models


class Calculation(models.Model):
    """Bajarilgan har bir hisob-kitob tarixi."""
    operation = models.CharField(max_length=20)
    n1 = models.IntegerField()
    n2 = models.IntegerField(null=True, blank=True)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'{self.operation}({self.n1}, {self.n2}) = {self.result[:30]}'