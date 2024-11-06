from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "companies"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Logo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='logos')
    image = models.ImageField(upload_to='logos/')
    is_primary = models.BooleanField(default=False)
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.name} - {'Primary' if self.is_primary else 'Secondary'} Logo"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other logos of this company to non-primary
            Logo.objects.filter(company=self.company, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
