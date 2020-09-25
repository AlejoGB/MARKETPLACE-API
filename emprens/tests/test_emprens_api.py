from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Emprendimiento, Producto
from emprens.serializers import EmprendimientoSerializer, ProductoSerializer


EMPRENS_URL = reverse('emprens:empren-list')
EMPREN_CREATE_URL = reverse('emprens:empren-create')

def barrio_url(barrio):
    """Return empren barrio list URL"""
    return reverse('emprens:barrio-list', args=[barrio])


def productos_list(id):
    '''Return empren detail URL'''
    return reverse('emprens:empren-productos', args=[id])

def empren_detail(id):
    '''Return empren detail URL'''
    return reverse('emprens:empren-detail', args=[id])

def sample_empren(owner, **params):
    
    # crea un emprendimiento para pruebas
    defaults = {
        'name': 'Buenas Burgers',
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
            'test@test.com',
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
        
        self.assertEqual(self.user, getattr(empren, 'owner'))

    # def test_create_segundo_emprendimiento_fail(self):

    #     payload = {
    #         'name': 'Buenas Burgers',
    #         'tag': 'Alimentos',
    #         'subtag': 'Panaderia',
    #         'cont_whatsapp': '+5411 1234-5678',
    #         'direccion': 'Larazabal 1245',
    #         'barrio': 'Devoto',
    #         'ciudad': 'CABA',
    #         'cobertura': 'Devoto, Villa Crespo, Saavedra',
    #         'envio': '$60-$120',
    #         'horario': '9 a 18'
    #     }
    #     res = self.client.post(EMPREN_CREATE_URL, payload)

    #     payload2 = {
    #         'name': 'Buenas Burgers2',
    #         'tag': 'Alimentos',
    #         'subtag': 'Panaderia',
    #         'cont_whatsapp': '+5411 1234-5678',
    #         'direccion': 'Larazabal 1245',
    #         'barrio': 'Devoto',
    #         'ciudad': 'CABA',
    #         'cobertura': 'Devoto, Villa Crespo, Saavedra',
    #         'envio': '$60-$120',
    #         'horario': '9 a 18' 
    #     }

    #     res2 = self.client.post(EMPREN_CREATE_URL, payload)
        
    #     self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)


class PublicProductoApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
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