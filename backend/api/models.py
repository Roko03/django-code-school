from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (('prof', 'professor'), ('stu', 'student'), ('adm', 'admin'))
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES, default='stu')
    bio = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Korisnici'

    def save(self,*args,**kwargs):
        if self.role == 'adm':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)


class Workshop(models.Model):
    LEVEL = (
        ('jun', 'Junior'),
        ('mid', 'Mid'),
        ('sen', 'Senior'),
    )
    SUBJECT = (
        ('rjs', 'React'),
        ('ex', 'Express'),
        ('njs', 'Next.JS'),
    )
    name = models.TextField(max_length=150, null=False)
    time = models.DateTimeField(auto_now_add=False)
    info = models.TextField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)
    level = models.CharField(blank=True, max_length=150, choices=LEVEL)
    subject = models.CharField(blank=True,max_length=150, choices=SUBJECT)

    class Meta:
        verbose_name_plural = 'Radionice'

    def __str__(self):
        return f"{self.name} {self.time} {self.info} {self.user_id} {self.level} {self.subject}"

class Organization(models.Model):
    name = models.TextField(max_length=150, null=False)
    info = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Organizacije'

    def __str__(self):
        return f"{self.name} {self.info}"


class UserOrganization(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Korisnici po organizacijama'

    def __str__(self):
        return f"{self.user_id} {self.organization_id}" 


class LoginWorkshop(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop_id = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Prijave za radionicu'

    def __str__(self):
        return f"{self.user_id} {self.workshop_id}"