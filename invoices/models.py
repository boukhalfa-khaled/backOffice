from django.db  import models
from users.models import User
from customers.models import Customer
from services.models import Service 

class Invoice(models.Model):
  PENDING = 'pending'
  PAID = 'paid'
  UNPAID = 'unpaid'
  STATU_CHOICES = [
    (PENDING, 'Pending'),
    (PAID, 'Paid'),
    (UNPAID, 'Unpaid'),
  ]

  title       = models.CharField(max_length=255)
  description = models.TextField(null=True)
  status      = models.CharField(max_length=20, choices=STATU_CHOICES, default=PENDING,)
  price       = models.DecimalField(max_digits=10, decimal_places=2)
  qty         = models.IntegerField()
  total       = models.DecimalField(max_digits=10, decimal_places=2)
  created_at  = models.DateTimeField(auto_now_add=True)
  update_at   = models.DateTimeField(auto_now=True)
  service_id  = models.ForeignKey(to=Service, null=True, on_delete=models.CASCADE)
  customer_id = models.ForeignKey(to=Customer, null=True, on_delete=models.CASCADE)
  created_by  = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)


  class Meta:
    ordering: ['-updated_at']

  def __str__(self):
    return str(self.title)
