from django.db  import models
from users.models import User
import  datetime

class Customer(models.Model):
  name       = models.CharField(max_length=255)
  email      = models.CharField(max_length=255)
  phone      = models.CharField(max_length=255)
  address    = models.CharField(max_length=255)
  description  = models.TextField(null=True)
  date       = models.DateField(default=datetime.date.today)
  created_at = models.DateTimeField(auto_now_add=True)
  update_at  = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)


  class Meta:
    ordering: ['-updated_at']

  def __str__(self):
    return str(self.name)


class Document(models.Model):
  title = models.CharField(max_length=255)
  type = models.CharField(max_length=255)
  file = models.FileField(upload_to='uploads/',null=False)
  customer_id = models.ForeignKey(to=Customer, verbose_name="Customer", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering: ['-created_at']

  def __str__(self):
    return str(self.title)