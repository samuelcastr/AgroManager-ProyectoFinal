from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db import transaction
from .models import Cultivo, CicloSiembra, Variedad
from .serializers import CicloSerializer
from datetime import date, timedelta


class TransaccionesAtomicasTestCase(TestCase):
	"""Tests para verificar que las transacciones atómicas funcionan correctamente"""

	def setUp(self):
		self.variedad = Variedad.objects.create(
			nombre="Variedad Test",
			descripcion="Variedad para pruebas"
		)

	def test_transaccion_atomica_cultivo_rollback(self):
		"""Verificar que si ocurre un error, la transacción se revierte"""
		initial_count = Cultivo.objects.count()
		
		try:
			with transaction.atomic():
				cultivo = Cultivo.objects.create(
					nombre="Cultivo Test",
					tipo="cereal",
					variedad=self.variedad
				)
				# Simular error
				raise ValueError("Error simulado")
		except ValueError:
			pass
		
		# Verificar que el cultivo NO se creó
		self.assertEqual(Cultivo.objects.count(), initial_count)

	def test_transaccion_atomica_cultivo_commit(self):
		"""Verificar que si no hay error, la transacción se ejecuta"""
		initial_count = Cultivo.objects.count()
		
		with transaction.atomic():
			cultivo = Cultivo.objects.create(
				nombre="Cultivo Test",
				tipo="cereal",
				variedad=self.variedad
			)
		
		# Verificar que el cultivo se creó
		self.assertEqual(Cultivo.objects.count(), initial_count + 1)


class CicloValidationTests(TestCase):
	def test_fecha_siembra_menor_que_cosecha(self):
		v = Variedad.objects.create(nombre='TestVar')
		cultivo = Cultivo.objects.create(nombre='C', tipo='tipo', variedad=v)
		data = {
			'cultivo': cultivo.id,
			'fecha_siembra': date(2025, 5, 1),
			'fecha_cosecha_estimada': date(2025, 4, 1),
			'superficie_hectareas': 1.5,
		}
		serializer = CicloSerializer(data=data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('`fecha_siembra`', str(serializer.errors))


class CultivoEndpointsTests(APITestCase):
	def setUp(self):
		self.var = Variedad.objects.create(nombre='HíbridaA')
		self.cultivo = Cultivo.objects.create(nombre='Maiz dulce', tipo='maiz', variedad=self.var)

	def test_rendimiento_estimado_endpoint(self):
		CicloSiembra.objects.create(
			cultivo=self.cultivo,
			fecha_siembra=date(2025, 1, 1),
			fecha_cosecha_estimada=date(2025, 5, 1),
			rendimiento_estimado=100.0,
		)
		CicloSiembra.objects.create(
			cultivo=self.cultivo,
			fecha_siembra=date(2025, 6, 1),
			fecha_cosecha_estimada=date(2025, 9, 1),
			rendimiento_estimado=200.0,
		)
		url = f'/api/cultivos/{self.cultivo.id}/rendimiento_estimado/'
		resp = self.client.get(url, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data.get('rendimiento_promedio'), 150.0)

	def test_search_name_icontains(self):
	
		resp = self.client.get('/api/cultivos/?search=maiz')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		names = [r.get('nombre') for r in resp.data]
	
		if isinstance(resp.data, dict) and 'results' in resp.data:
			results = resp.data['results']
			names = [r.get('nombre') for r in results]
		self.assertTrue(any('Maiz' in n or 'maiz' in n.lower() for n in names))
