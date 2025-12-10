from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Cultivo, CicloSiembra
from .serializers import CultivoSerializer, CicloSerializer


class TiposViewSet(viewsets.ViewSet):
    """ViewSet para retornar tipos de cultivos disponibles"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        tipos = Cultivo.TIPOS_CULTIVO
        return Response([{"value": tipo[0], "label": tipo[1]} for tipo in tipos])


class CultivoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Cultivo.objects.all().order_by('-created_at')
    serializer_class = CultivoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'variedad__nombre']
    search_fields = ['nombre', 'tipo', 'variedad__nombre']

    @action(detail=True, methods=['get'])
    def rendimiento_estimado(self, request, pk=None):
        cultivo = self.get_object()
        ciclos = cultivo.ciclos.all()
        total = 0
        count = 0
        for c in ciclos:
            if c.rendimiento_estimado is not None:
                total += float(c.rendimiento_estimado)
                count += 1
        promedio = total / count if count else None
        return Response({'cultivo': cultivo.nombre, 'rendimiento_promedio': promedio})

    @action(detail=False, methods=['get'])
    def activos(self, request):
        activos = CicloSiembra.objects.filter(estado=CicloSiembra.EN_PROGRESO)
        page = self.paginate_queryset(activos)
        serializer = CicloSerializer(page or activos, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
