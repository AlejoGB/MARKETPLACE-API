from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='Test#1234'):
    # crea usuario de prueba
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    
    def test_create_user_with_email_success(self):
        # Test creating a new user with an email is succesful
        email = 'test@test.com'
        password = 'Password#123'
        user = get_user_model().objects.create_user(email = email, password = password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # chequea si esta nromalizado
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_empren_str(self):
        # test empren str representation
        empren = models.Emprendimiento.objects.create(
            # Mandatory fields
            owner=sample_user(),
            name='Buenas Burgers',
            tag='Alimentos',
            subtag='Panaderia',
            cont_whatsapp='+5411 1234-5678',
            direccion='Larazabal 1245',
            barrio='Devoto',
            ciudad='CABA',
            cobertura='Devoto, Villa Crespo, Saavedra',
            envio='$60-$120',
            horario='9 a 18'
        )

        self.assertEqual(str(empren), empren.name)

        



