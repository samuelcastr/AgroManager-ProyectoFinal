from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Sensor, LecturaSensor
from .serializers import SensorSerializer, LecturaSerializer


class SensorViewSet(viewsets.ModelViewSet):
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer

	@action(detail=True, methods=['get'])
	def ultimas(self, request, pk=None):
		sensor = self.get_object()
		lecturas = sensor.lecturas.order_by('-timestamp')[:10]
		serializer = LecturaSerializer(lecturas, many=True)
		return Response(serializer.data)


class LecturaViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = LecturaSensor.objects.all()
	serializer_class = LecturaSerializer

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

