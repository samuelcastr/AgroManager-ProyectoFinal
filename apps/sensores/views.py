from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Sensor, LecturaSensor
from .serializers import SensorSerializer, LecturaSerializer
from apps.core.permissions import HasRolePermission


class TiposViewSet(viewsets.ViewSet):
	"""ViewSet para retornar tipos de sensores disponibles"""
	permission_classes = [IsAuthenticated, HasRolePermission]
	required_permission = 'sensores.list'
	
	def list(self, request):
		tipos = Sensor.TIPOS_SENSOR
		resultado = []

		for tipo_value, tipo_label in tipos:
			sensores = Sensor.objects.filter(tipo=tipo_value)
			count = sensores.count()
			ids = list(sensores.values_list('id', flat=True))

			resultado.append({
				"value": tipo_value,
				"label": tipo_label,
				"count": count,
				"ids": ids,
			})

		return Response(resultado)


class SensorViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated, HasRolePermission]
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer
	
	def get_required_permission(self):
		"""Obtener permiso requerido según la acción"""
		if self.action == 'list' or self.action == 'retrieve':
			return 'sensores.list'
		elif self.action == 'create':
			return 'sensores.create'
		elif self.action in ['update', 'partial_update']:
			return 'sensores.update'
		elif self.action == 'destroy':
			return 'sensores.delete'
		return 'sensores.list'
	
	def check_permissions(self, request):
		"""Override para establecer el permiso requerido dinámicamente"""
		self.required_permission = self.get_required_permission()
		super().check_permissions(request)

	@action(detail=True, methods=['get'])
	def ultimas(self, request, pk=None):
		sensor = self.get_object()
		lecturas = sensor.lecturas.order_by('-timestamp')[:10]
		serializer = LecturaSerializer(lecturas, many=True)
		return Response(serializer.data)


class LecturaViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	permission_classes = [IsAuthenticated, HasRolePermission]
	queryset = LecturaSensor.objects.all()
	serializer_class = LecturaSerializer
	
	def get_required_permission(self):
		"""Obtener permiso requerido según la acción"""
		if self.action == 'list':
			return 'sensores.list'
		elif self.action == 'create':
			return 'sensores.create'
		return 'sensores.list'
	
	def check_permissions(self, request):
		"""Override para establecer el permiso requerido dinámicamente"""
		self.required_permission = self.get_required_permission()
		super().check_permissions(request)

	@action(detail=False, methods=['post'])
	def bulk(self, request):
		items = request.data if isinstance(request.data, list) else []
		created = 0
		for item in items:
			serializer = LecturaSerializer(data=item)
			if serializer.is_valid():
				serializer.save()
				created += 1
		return Response({'created': created})

