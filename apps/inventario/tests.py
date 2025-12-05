from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError

from .models import Insumo, Lote, MovimientoStock, registrar_salida_stock


class MovimientoStockTests(TestCase):
	def setUp(self):
		self.insumo = Insumo.objects.create(nombre="Semilla", unidad_medida="kg", stock_minimo=2)
		# crear lotes: 10 y 5
		Lote.objects.create(insumo=self.insumo, cantidad_actual=10)
		Lote.objects.create(insumo=self.insumo, cantidad_actual=5)

	def test_registrar_salida_fifo_and_movimiento(self):
		# consumir 12 -> primero 10 del lote1, luego 2 del lote2
		registrar_salida_stock(self.insumo, 12, descripcion="Prueba FIFO")

		lotes = list(self.insumo.lotes.order_by("fecha_ingreso"))
		self.assertEqual(lotes[0].cantidad_actual, 0)
		self.assertEqual(lotes[1].cantidad_actual, 3)

		mov = MovimientoStock.objects.filter(insumo=self.insumo, tipo="SALIDA").first()
		self.assertIsNotNone(mov)
		self.assertEqual(mov.cantidad, 12)


class AjusteMasivoTransactionTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.ins_a = Insumo.objects.create(nombre="A", unidad_medida="u", stock_minimo=1)
		self.ins_b = Insumo.objects.create(nombre="B", unidad_medida="u", stock_minimo=1)
		Lote.objects.create(insumo=self.ins_a, cantidad_actual=5)
		Lote.objects.create(insumo=self.ins_b, cantidad_actual=3)

	def test_ajuste_masivo_rollback_on_error(self):
		url = reverse('ajuste-masivo')
		payload = {
			"items": [
				{"insumo_id": self.ins_a.id, "tipo": "SALIDA", "cantidad": 4},
				{"insumo_id": self.ins_b.id, "tipo": "SALIDA", "cantidad": 10},  # excede stock
			]
		}

		resp = self.client.post(url, payload, format='json')
		self.assertEqual(resp.status_code, 400)

		# Verificar que no se aplicó el primer ajuste (rollback)
		la = self.ins_a.lotes.first()
		self.assertEqual(la.cantidad_actual, 5)

	def test_ajuste_masivo_successful(self):
		url = reverse('ajuste-masivo')
		payload = {
			"items": [
				{"insumo_id": self.ins_a.id, "tipo": "SALIDA", "cantidad": 2},
				{"insumo_id": self.ins_b.id, "tipo": "ENTRADA", "cantidad": 4},
			]
		}

		resp = self.client.post(url, payload, format='json')
		self.assertEqual(resp.status_code, 201)

		# Verificar salidas/entradas
		self.ins_a.refresh_from_db()
		self.ins_b.refresh_from_db()

		self.assertEqual(self.ins_a.total_stock, 3)  # 5 - 2
		self.assertEqual(self.ins_b.total_stock, 7)  # 3 + 4
