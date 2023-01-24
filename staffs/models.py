import uuid
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from main.models import BaseModel
from main.variables import phone_regex


AUTH_TYPE =(
    ("10", "Login"),
    ("20", "Logout"),
)

class  StaffDesignation(BaseModel):
    name = models.CharField(max_length=128 )
    permission = models.ManyToManyField('users.Permission', blank=True)

    class Meta:
        db_table = 'staff_designation'
        verbose_name = ('staff_designation')
        verbose_name_plural = ('staff_designation')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)
    
    def permissionlist(self):
        result = []
        permissions = self.permission.all()
        for perm in permissions:
            result.append(str(perm.code))
        return result
    

class Staff(BaseModel):
    name = models.CharField(max_length=128 )
    profile = models.ImageField(upload_to="Staffs/profile/", blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=15 , validators=[phone_regex],)
    email = models.EmailField()
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    designation = models.ForeignKey('staffs.StaffDesignation', on_delete=models.CASCADE)
    salary = models.DecimalField(default=0.00,decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    permission = models.ManyToManyField('users.Permission', blank=True)
    
    user = models.ForeignKey(
        "auth.User", blank=True, related_name="user_%(class)s_objects", on_delete=models.CASCADE)
    password= models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    
    account_holder_name = models.CharField(max_length=128, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    bank_branch = models.CharField(max_length=128, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=128, blank=True, null=True)
    

    class Meta:
        db_table = 'staff'
        verbose_name = ('staff')
        verbose_name_plural = ('staff')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.name)
    
    def permissionlist(self):
        result = []
        permissions = self.permission.all()
        for perm in permissions:
            result.append(str(perm.code))
        return result
    
    
class StaffAuth(models.Model):
    auth_type = models.CharField(max_length=128,choices=AUTH_TYPE )
    staff = models.ForeignKey('staffs.Staff', on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    
    class Meta:
        db_table = 'staff_auth'
        verbose_name = ('staff_auth')
        verbose_name_plural = ('staff_auth')
        ordering = ('auto_id',)

    def __str__(self):
        return str(self.staff)