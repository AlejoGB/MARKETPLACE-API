from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                     PermissionsMixin
from .utils import unique_slug_generator
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
import random
import os


def get_filename_ext(filepath):  # genera la extension del archivo para el path
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):  # genera un path para la imagen con un numero aleatorio
    new_filename = random.randint(1, 154125125)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"emprens/{new_filename}/{final_filename}"


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Se necesita email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, default=0)
    email = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=20, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    adress_1 = models.CharField(max_length=200, default=0)
    adress_2 = models.CharField(max_length=200, default=0)
    adress_3 = models.CharField(max_length=200, default=0)
    adress_4 = models.CharField(max_length=200, default=0)
    adress_5 = models.CharField(max_length=200, default=0)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class EmprendimientoQuerySet(models.query.QuerySet):

    def barrio(self, barrio):
        return self.filter(barrio__iexact=barrio)

    def active(self):
        return self.filter(active=True)

    def tag(self, tag):
        return self.filter(tag__iexact=tag)

    def subtag(self, subtag):
        return self.filter(subtag__iexact=subtag)


class EmprendimientoManager(models.Manager):

    def get_queryset(self):
        return EmprendimientoQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()

    def getById(self, id):
        qs = self.get_queryset().filter(id=id).active()  # Emprendimiento.objects.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def getByBarrio(self, barrio):  # Emprendimiento.objects.getbyBarrio()
        return self.get_queryset().barrio(barrio).active()

    def getByTag(self, tag):
        return self.get_queryset.tag(tag).active()

    def getBySubtag(self, subtag):
        return self.get_queryset.subtag(subtag).active()


class Emprendimiento(models.Model):
    # descripcion
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    tag = models.CharField(max_length=50)
    subtag = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    # contacto
    cont_mail = models.CharField(max_length=100)
    cont_insta = models.CharField(max_length=100)
    cont_whatsapp = models.CharField(max_length=100)
    # ubicacion
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length= 50)
    ciudad = models.CharField(max_length = 100)
    # entrega
    cobertura = models.CharField(max_length=120)
    envio = models.CharField(max_length=80)
    horario = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    # private
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING, related_name = 'empren')
    featured = models.BooleanField(default=False)

    objects = EmprendimientoManager()

    def get_absolute_url(self):
        # return "/emprens/{slug}".format(slug=self.slug)
        return reverse("detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name  # , self.rubro , self.subrubro , self.barrio , self.ciudad


def emprendimiento_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(emprendimiento_pre_save_receiver, sender=Emprendimiento)


class ProductoManager(models.Manager):
    def getByEmpren(self, id):  # Producto.objects.getbyEmpren()
        return self.get_queryset().filter(emprendimiento=id)  # Emprendimiento.objects.get_queryset()


class Producto(models.Model):

    emprendimiento = models.ForeignKey('Emprendimiento', on_delete=models.CASCADE, null=True, related_name='producto')
    name = models.CharField(max_length=120)
    tag = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    banner = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    precio = models.IntegerField(default=0)
    inmediato = models.BooleanField(default=False)
    stock = models.BooleanField(default=True)

    def __str__(self):
        return "%s - By: %s" % (self.nombre, self.emprendimiento)