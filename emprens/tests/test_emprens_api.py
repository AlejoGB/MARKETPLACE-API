from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Emprendimiento, Producto, User
from emprens.serializers import EmprendimientoSerializer, ProductoSerializer


EMPRENS_URL = reverse('emprens:empren-list')
EMPREN_CREATE_URL = reverse('emprens:empren-create')

def barrio_url(barrio):
    """Return empren barrio list URL"""
    return reverse('emprens:barrio-list', args=[barrio])


def productos_list(id):
    '''Return empren detail URL'''
    return reverse('emprens:empren-productos', args=[id])


def product_create(id):
    '''Return product create URL'''
    return reverse('emprens:producto-create', args=[id])

def empren_detail(id):
    '''Return empren detail URL'''
    return reverse('emprens:empren-detail', args=[id])

def empren_rud(id):
    '''Return empren RUD URL'''
    return reverse('emprens:empren-rud', args=[id])

def producto_rud(id):
    '''Return producto RUD URL'''
    return reverse('emprens:producto-rud', args=[id])


def sample_empren(owner, **params):
    
    # crea un emprendimiento para pruebas
    defaults = {
        'name': 'Sample Name',
        'tag': 'Alimentos',
        'subtag': 'Panaderia',
        'cont_whatsapp': '+5411 1234-5678',
        'direccion': 'Larazabal 1245',
        'barrio': 'Devoto',
        'ciudad': 'CABA',
        'cobertura': 'Devoto, Villa Crespo, Saavedra',
        'envio': '$60-$120',
        'horario': '9 a 18'
    }

    defaults.update(params)
    return Emprendimiento.objects.create(owner=owner, **defaults)

def sample_producto(emprendimiento, **params):
    # crea un producto para pruebas
    defaults = {
        'name': 'Triple Bacon',
        'tag': 'Hamburguesa',
        'precio': 240.00,
        'inmediato': True
    }

    defaults.update(params)
    return Producto.objects.create(emprendimiento=emprendimiento, **defaults)

def sample_user( **params):
    # crea un producto para pruebas
    defaults = {
        'name': 'SampleTest',
        'email': 'test@test',
        'password': 'test#1234',
        'is_owner': True
    }

    defaults.update(params)
    return User.objects.create(**defaults)


class PublicEmprendimientoApiTest(TestCase):
    # Test unauthenticated empren API access

    def setUp(self):
        # For empren creation only
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'Test#1234'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2@test2.com',
            'Test#1234'
        )
        self.client.force_authenticate(self.user2)
        self.client.force_authenticate(self.user)

    # def test_auth_required(self):
    #     test donde se requiere autentificacion
    #     res = self.client.get(EMPRENS_URL)

    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_emprens(self):
        sample_empren(owner=self.user)
        sample_empren(owner=self.user2, name='pansitos')

        res = self.client.get(EMPRENS_URL)

        emprens = Emprendimiento.objects.all().order_by('-id')
        serializer = EmprendimientoSerializer(emprens, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_emprens_by_barrio(self):
        sample_empren(owner=self.user)
        sample_empren(owner=self.user2, name='Heladito', barrio='Barracas')

        url = barrio_url('Barracas')
        res = self.client.get(url)
        emprens = Emprendimiento.objects.getByBarrio('Barracas').order_by('-id')
        serializer = EmprendimientoSerializer(emprens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_emprens_by_id(self):
        sample_empren(owner=self.user)
        sample_empren(owner=self.user2, name='panadero', id=10)

        url = empren_detail(10)
        res = self.client.get(url)
        emprens = Emprendimiento.objects.getById(10)
        serializer = EmprendimientoSerializer(emprens)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        '''Por ahora llego hasta RETRIEVE
            faltan: los privados CREATE UPDATE
             RETRIEVE(PRIVATE) DELETE'''

class PrivateEmprendimientoApiTests(TestCase):
    # Test authenticated empren API access

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
             'test2@test.com',
             'Test#1234'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2@test2.com',
            'Test#1234'
        )
        self.client.force_authenticate(self.user) 

    def test_create_emprendimiento(self):

        payload = {
            'name': 'Buenas Burgers',
            'tag': 'Alimentos',
            'subtag': 'Panaderia',
            'cont_whatsapp': '+5411 1234-5678',
            'direccion': 'Larazabal 1245',
            'barrio': 'Devoto',
            'ciudad': 'CABA',
            'cobertura': 'Devoto, Villa Crespo, Saavedra',
            'envio': '$60-$120',
            'horario': '9 a 18',
            #'owner': self.user.email
        }
        res = self.client.post(EMPREN_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        empren = Emprendimiento.objects.get(id=res.data['pk'])
        
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(empren, key))
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_owner,True)
        self.assertEqual(self.user, getattr(empren, 'owner'))

    def test_create_segundo_emprendimiento_fail(self):
        # TODO: este test no esta chequeado que este saliendo bien
        self.user.is_owner = True
        self.user.save()
        payload = {
            'name': 'Buenas Burgers',
            'tag': 'Alimentos',
            'subtag': 'Panaderia',
            'cont_whatsapp': '+5411 1234-5678',
            'direccion': 'Larazabal 1245',
            'barrio': 'Devoto',
            'ciudad': 'CABA',
            'cobertura': 'Devoto, Villa Crespo, Saavedra',
            'envio': '$60-$120',
            'horario': '9 a 18',
            #'owner': self.user.email
        }
        
        self.assertTrue(EmprendimientoSerializer(payload))
        res = self.client.post(EMPREN_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_emprendimiento(self):
        # test updating emprendimiento for auth user

        sample_empren(owner=self.user, name='panadero', id=10)
        self.user.is_owner = True
        self.user.save()
        
        url = empren_rud(10)
        payload = {'name': 'new name', 'tag': 'NewTag'}
        res = self.client.patch(url, payload)
        
        empren_upd = Emprendimiento.objects.getById(10)


        self.assertEqual(empren_upd.name, payload['name'])
        self.assertEqual(empren_upd.tag, payload['tag'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_emprendimiento_fail_not_owner(self):
        sample_empren(owner=self.user2, name='testFail', id=10)
        self.user.is_owner = True
        self.user.save()

        url = empren_rud(10)
        payload = {'name': 'new name', 'tag': 'NewTag'}
        res = self.client.patch(url, payload)
        
        empren_upd = Emprendimiento.objects.getById(10)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_emprendimiento(self):
        # test delete emprendimiento
        sample_empren(owner=self.user, name='testFail', id=10)
        self.user.is_owner = True
        self.user.save()

        url = empren_rud(10)
        res = self.client.delete(url)

        empren_del = Emprendimiento.objects.getById(10)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(empren_del, None)
        


    def test_delete_emprendimiento_fail_not_owner(self):
        # test delete emprendimiento not owner
        sample_empren(owner=self.user2, name='testFail', id=10)

        url = empren_rud(10)
        res = self.client.delete(url)

        empren_del = Emprendimiento.objects.getById(10)

        self.assertEqual(empren_del.pk, 10)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PublicProductoApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'Test#1234'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2@test2.com',
            'Test#1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_productos(self):
        empren = sample_empren(owner=self.user, id=10)

        sample_producto(emprendimiento=empren)  # capaz hay q poner un 10 aca
        sample_producto(emprendimiento=empren, name='Fideos')

        url = productos_list(10)
        res = self.client.get(url)

        productos = Producto.objects.filter(emprendimiento=10)
        serializer = ProductoSerializer(productos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

class PrivateProductoApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'Test#1234'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2@test2.com',
            'Test#1234'
        )
        self.client.force_authenticate(self.user)

    def test_create_producto(self):
        empren = sample_empren(owner=self.user, id=10)
        self.user.is_owner = True
        self.user.save()
        payload = {
        'name': 'Triple Bacon',
        'tag': 'Hamburguesa',
        'descripcion': 'asd asd asd',
        'precio': 240.00,
        'inmediato': True
        }
        
        url = product_create(10)
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        producto = Producto.objects.get(id=res.data['pk'])
        
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(producto, key))
        self.assertEqual(empren, getattr(producto, 'emprendimiento'))


    def test_create_producto_fail_not_owner(self):
        empren = sample_empren(owner=self.user2, id=10)
        self.user.is_owner = True
        self.user.save()
        payload = {
        'name': 'Triple Bacon',
        'tag': 'Hamburguesa',
        'descripcion': 'asd asd asd',
        'precio': 240.00,
        'inmediato': True
        }
        
        url = product_create(10)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_update_producto(self):
        # test updating emprendimiento for auth user
        empren = sample_empren(owner=self.user, name='panadero', id=10)
        sample_producto(emprendimiento=empren)
        sample_producto(emprendimiento=empren, name='Fideos', pk=25) 
        self.user.is_owner = True
        self.user.save()
        
        url = producto_rud(25)
        payload = {'name': 'new name', 'tag': 'NewTag'}
        res = self.client.patch(url, payload)
        
        prod_upd = Producto.objects.getById(25)


        self.assertEqual(prod_upd.name, payload['name'])
        self.assertEqual(prod_upd.tag, payload['tag'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_producto_fail_not_owner(self):
        # test updating emprendimiento for unauth user
        empren = sample_empren(owner=self.user2, name='panadero', id=10)
        sample_producto(emprendimiento=empren)
        sample_producto(emprendimiento=empren, name='Fideos', pk=25) 
        self.user.is_owner = True
        self.user.save()
        
        url = producto_rud(25)
        payload = {'name': 'new name', 'tag': 'NewTag'}
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_producto(self):
        # test delete producto
        empren = sample_empren(owner=self.user, name='testFail', id=10)
        sample_producto(emprendimiento=empren, name='Fideos', pk=25)
        self.user.is_owner = True
        self.user.save()

        url = producto_rud(25)
        res = self.client.delete(url)

        prod_del = Producto.objects.getById(25)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(prod_del, None)


    def test_delete_producto_fail_not_owner(self):
        # test delete producto
        empren = sample_empren(owner=self.user2, name='testFail', id=10)
        sample_producto(emprendimiento=empren, name='Fideos', pk=25)
        self.user.is_owner = True
        self.user.save()

        url = producto_rud(25)
        res = self.client.delete(url)

        prod_del = Producto.objects.getById(25)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(prod_del.id, 25)
        