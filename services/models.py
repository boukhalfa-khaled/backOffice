from django.db  import models

class Service(models.Model):
  title       = models.CharField(max_length=255)
  description = models.TextField(null=True)
  price       = models.CharField(max_length=255)
  stock       = models.CharField(max_length=255)
  created_at  = models.DateTimeField(auto_now_add=True)
  update_at   = models.DateTimeField(auto_now=True)


  class Meta:
    ordering: ['-updated_at']

  def __str__(self):
    return str(self.title)