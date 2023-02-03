from django.db import models


class AuditModel(models.Model):
    """
    Base Model to audit other models
    """

    created_at  = models.DateTimeField(
        verbose_name='Create at',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='Modified at',
        auto_now=True
    )

    class Meta:
        abstract = True
