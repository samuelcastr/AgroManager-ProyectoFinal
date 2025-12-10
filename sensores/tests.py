from django.test import TestCase
from django.utils import timezone

from .models import Sensor, LecturaSensor


class SimpleSensorTest(TestCase):
	def test_create_sensor_and_lectura(self):
		s = Sensor.objects.create(serial='S1', tipo='HUMEDAD')
		l = LecturaSensor.objects.create(sensor=s, timestamp=timezone.now(), valor=12.345)
		self.assertEqual(s.lecturas.count(), 1)
