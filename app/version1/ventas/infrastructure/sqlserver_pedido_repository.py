# sqlserver_pedido_repository.py

from version1.ventas.domain.entities import PedidoVenta, CabeceraPedidoVenta, LineaPedidoVenta
from version1.ventas.application.create_pedido_pharma import PedidoVentaRepository
import pyodbc

class SqlServerPedidoRepository(PedidoVentaRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def save(self, pedido: PedidoVenta) -> None:
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        # Insertar cabecera
        cab = pedido.cabecera
        cursor.execute("""
            INSERT INTO CabeceraPedidoVenta (
                num_pedido_venta, cod_cooperativa, puerta, acuerdo_venta_asociado,
                num_pedido_laboratorio, fecha_pedido_farmacia, fecha_pedido_cooperativa,
                cod_cliente_cooperativa, estado_pedido
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, cab.num_pedido_venta, cab.cod_cooperativa, cab.puerta, cab.acuerdo_venta_asociado,
             cab.num_pedido_laboratorio, cab.fecha_pedido_farmacia, cab.fecha_pedido_cooperativa,
             cab.cod_cliente_cooperativa, cab.estado_pedido)

        # Insertar líneas
        for linea in pedido.lineas:
            cursor.execute("""
                INSERT INTO LineaPedidoVenta (
                    num_pedido_venta, num_linea_pedido_venta, num_pedido_lugonet,
                    num_acuerdo_venta, cod_articulo_cooperativa, cantidad_solicitada,
                    cantidad_bonificada, cantidad_confirmada, pvp, descuento_porcentaje,
                    descuento_unitario, pvp_neto, cargo_cooperativo,
                    cod_proveedor_cooperativa, computa_aprovisionamiento,
                    ocultar_web, no_unnefar, estado_linea_pedido
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, linea.num_pedido_venta, linea.num_linea_pedido_venta, linea.num_pedido_lugonet,
                 linea.num_acuerdo_venta, linea.cod_articulo_cooperativa, linea.cantidad_solicitada,
                 linea.cantidad_bonificada, linea.cantidad_confirmada, linea.pvl,
                 linea.descuento_porcentaje, linea.descuento_unitario, linea.pvl_neto,
                 linea.cargo_cooperativo, linea.cod_proveedor_cooperativa,
                 linea.computa_aprovisionamiento, linea.ocultar_web, linea.no_unnefar,
                 linea.estado_linea_pedido)

        conn.commit()
        cursor.close()
        conn.close()
