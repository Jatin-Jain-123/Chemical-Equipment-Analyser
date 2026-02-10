from django.db import models


class EquipmentDataset(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"Dataset uploaded at {self.uploaded_at}"