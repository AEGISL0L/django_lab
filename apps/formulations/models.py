from django.conf import settings
from django.db import models
from django.utils import timezone


class FormulaRequest(models.Model):
    class Status(models.TextChoices):
        RECIBIDA = "RECIBIDA", "Recibida"
        EN_PREPARACION = "EN_PREPARACION", "En Preparación"
        COMPLETADO = "COMPLETADO", "Completado"
        CANCELADO = "CANCELADO", "Cancelado"

    petition_id = models.CharField(max_length=32, unique=True)

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    # ✅ antes string; ahora boolean
    requiere_rele = models.BooleanField(default=False)

    telefono_contacto = models.CharField(max_length=20)
    foto_receta = models.ImageField(upload_to="formulas/recetas/", blank=True, null=True)

    fecha_solicitud = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=Status.choices, default=Status.RECIBIDA)
    fecha_preparacion = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    notas_laboratorio = models.TextField(blank=True)

    preparado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="formulas_preparadas",
    )

    def __str__(self) -> str:
        return f"{self.petition_id} - {self.nombre}"
# Create your models here.
