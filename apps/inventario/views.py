from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Insumo, Lote, MovimientoStock, registrar_salida_stock
from .serializers import InsumoAlertSerializer, AjusteMasivoSerializer, MovimientoStockSerializer, InsumoSerializer, LoteSerializer
from apps.core.permissions import HasRolePermission


class AlertasStockAPIView(APIView):
	"""Retorna insumos cuyo stock total está por debajo o igual al stock mínimo."""
	permission_classes = [IsAuthenticated, HasRolePermission]
	required_permission = 'inventario.list'

	def get(self, request):
		insumos = Insumo.objects.all()
		data = []
		for ins in insumos:
			total = ins.total_stock
			por_debajo = total <= ins.stock_minimo
			data.append({
				"id": ins.id,
				"nombre": ins.nombre,
				"unidad_medida": ins.unidad_medida,
				"stock_minimo": ins.stock_minimo,
				"total_stock": total,
				"por_debajo": por_debajo,
			})
		serializer = InsumoAlertSerializer(data, many=True)
		return Response(serializer.data)


class AjusteMasivoAPIView(APIView):
	"""Recibe una lista de ajustes (ENTRADA/SALIDA/AJUSTE) y los aplica en una única transacción.

	- ENTRADA: crea un nuevo Lote con la cantidad indicada y registra MovimientoStock
	- SALIDA: utiliza `registrar_salida_stock` (FIFO) y registra MovimientoStock
	- AJUSTE: registra un MovimientoStock y ajusta el primer lote disponible (si es negativo)
	
	NOTA: CSRF exempt porque usa autenticación JWT (no cookies)
	"""
	permission_classes = [IsAuthenticated, HasRolePermission]
	required_permission = 'inventario.create'

	def post(self, request):
		serializer = AjusteMasivoSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		items = serializer.validated_data["items"]

		movimientos_creados = []

		try:
			with transaction.atomic():
				for it in items:
					insumo = get_object_or_404(Insumo, pk=it["insumo_id"])
					tipo = it["tipo"]
					cantidad = it["cantidad"]
					descripcion = it.get("descripcion", "") or ""

					if tipo == "ENTRADA":
						lote = Lote.objects.create(insumo=insumo, cantidad_actual=abs(cantidad))
						mov = MovimientoStock.objects.create(
							insumo=insumo, tipo="ENTRADA", cantidad=abs(cantidad), descripcion=descripcion
						)
						movimientos_creados.append(mov)

					elif tipo == "SALIDA":
						# registrar_salida_stock lanzará ValidationError si falla
						mov = registrar_salida_stock(insumo, abs(cantidad), descripcion=descripcion)
						# registrar_salida_stock crea el MovimientoStock internamente
						# Recuperar el último movimiento SALIDA para este insumo y cantidad
						last = MovimientoStock.objects.filter(insumo=insumo, tipo="SALIDA", cantidad=abs(cantidad)).order_by("-fecha").first()
						if last:
							movimientos_creados.append(last)

					else:  # AJUSTE
						# Si cantidad negativa, intentar reducir stock FIFO
						if cantidad < 0:
							registrar_salida_stock(insumo, abs(cantidad), descripcion=descripcion)
						else:
							Lote.objects.create(insumo=insumo, cantidad_actual=abs(cantidad))

						mov = None
						# registrar_salida_stock crea movimiento cuando reduce stock
						if cantidad < 0:
							last = MovimientoStock.objects.filter(insumo=insumo, tipo="SALIDA", cantidad=abs(cantidad)).order_by("-fecha").first()
							if last:
								movimientos_creados.append(last)
						else:
							mov = MovimientoStock.objects.create(
								insumo=insumo, tipo="AJUSTE", cantidad=abs(cantidad), descripcion=descripcion
							)
							movimientos_creados.append(mov)

		except ValidationError as exc:
			return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

		out = MovimientoStockSerializer(movimientos_creados, many=True).data
		return Response({"movimientos": out}, status=status.HTTP_201_CREATED)


# ViewSets para los modelos principales
class InsumoViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated, HasRolePermission]
	queryset = Insumo.objects.all()
	serializer_class = InsumoSerializer
	
	def get_required_permission(self):
		"""Obtener permiso requerido según la acción"""
		if self.action == 'list' or self.action == 'retrieve':
			return 'inventario.list'
		elif self.action == 'create':
			return 'inventario.create'
		elif self.action in ['update', 'partial_update']:
			return 'inventario.update'
		elif self.action == 'destroy':
			return 'inventario.delete'
		return 'inventario.list'
	
	def check_permissions(self, request):
		"""Override para establecer el permiso requerido dinámicamente"""
		self.required_permission = self.get_required_permission()
		super().check_permissions(request)


class LoteViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated, HasRolePermission]
	queryset = Lote.objects.all()
	serializer_class = LoteSerializer
	
	def get_required_permission(self):
		"""Obtener permiso requerido según la acción"""
		if self.action == 'list' or self.action == 'retrieve':
			return 'inventario.list'
		elif self.action == 'create':
			return 'inventario.create'
		elif self.action in ['update', 'partial_update']:
			return 'inventario.update'
		elif self.action == 'destroy':
			return 'inventario.delete'
		return 'inventario.list'
	
	def check_permissions(self, request):
		"""Override para establecer el permiso requerido dinámicamente"""
		self.required_permission = self.get_required_permission()
		super().check_permissions(request)


class MovimientoStockViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated, HasRolePermission]
	queryset = MovimientoStock.objects.all()
	serializer_class = MovimientoStockSerializer
	
	def get_required_permission(self):
		"""Obtener permiso requerido según la acción"""
		if self.action == 'list' or self.action == 'retrieve':
			return 'inventario.list'
		elif self.action == 'create':
			return 'inventario.create'
		elif self.action in ['update', 'partial_update']:
			return 'inventario.update'
		elif self.action == 'destroy':
			return 'inventario.delete'
		return 'inventario.list'
	
	def check_permissions(self, request):
		"""Override para establecer el permiso requerido dinámicamente"""
		self.required_permission = self.get_required_permission()
		super().check_permissions(request)
