from version1.ventas.domain.entities import PedidoVenta
from version1.ventas.application.create_pedido_pharma import PedidoVentaRepository
import pyodbc


class SqlServerPedidoRepository(PedidoVentaRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def save(self, pedido: PedidoVenta) -> None:
        conn = None
        cursor = None

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Insertar cabecera
            cab = pedido.cabecera
            cursor.execute("""
                INSERT INTO ventas.ventas_cabecera (
                    num_pedido_venta, cod_cooperativa, puerta, acuerdo_venta_asociado,
                    num_pedido_laboratorio, fecha_pedido_farmacia, fecha_pedido_cooperativa,
                    cod_cliente_cooperativa, estado_pedido
                ) OUTPUT INSERTED.venta_id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, cab.num_pedido_venta, cab.cod_cooperativa, cab.puerta, cab.acuerdo_venta_asociado,
                 cab.num_pedido_laboratorio, cab.fecha_pedido_farmacia, cab.fecha_pedido_cooperativa,
                 cab.cod_cliente_cooperativa, cab.estado_pedido)
            
            venta_id = cursor.fetchone()[0]

            # Insertar líneas
            for linea in pedido.lineas:
                cursor.execute("""
                    INSERT INTO ventas.ventas_linea (
                        venta_id,
                        num_pedido_venta, num_linea_pedido_venta, num_pedido_lugonet,
                        num_acuerdo_venta, cod_articulo_cooperativa, cantidad_solicitada,
                        cantidad_bonificada, cantidad_confirmada, pvl, descuento_porcentaje,
                        descuento_unitario, pvl_neto, cargo_cooperativo,
                        cod_proveedor_cooperativa, computa_aprovisionamiento,
                        ocultar_web, no_unnefar, estado_linea_pedido
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, venta_id, linea.num_pedido_venta, linea.num_linea_pedido_venta, linea.num_pedido_lugonet,
                     linea.num_acuerdo_venta, linea.cod_articulo_cooperativa, linea.cantidad_solicitada,
                     linea.cantidad_bonificada, linea.cantidad_confirmada, linea.pvl,
                     linea.descuento_porcentaje, linea.descuento_unitario, linea.pvl_neto,
                     linea.cargo_cooperativo, linea.cod_proveedor_cooperativa,
                     linea.computa_aprovisionamiento, linea.ocultar_web,
                     linea.no_unnefar, linea.estado_linea_pedido)
                
            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al guardar el pedido en SQL Server: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_pedidos(self, cod_cooperativa=None, estado_pedido=None, fecha_inicio=None, fecha_fin=None):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        query = "SELECT * FROM ventas.ventas_cabecera WHERE 1=1"
        params = []

        if cod_cooperativa:
            query += " AND cod_cooperativa = ?"
            params.append(cod_cooperativa)
        if estado_pedido:
            query += " AND estado_pedido = ?"
            params.append(estado_pedido)
        if fecha_inicio:
            query += " AND fecha_pedido_cooperativa >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND fecha_pedido_cooperativa <= ?"
            params.append(fecha_fin)

        cursor.execute(query, *params)
        cabeceras = cursor.fetchall()

        cab_columns = [col[0] for col in cursor.description]

        pedidos = []
        for cab in cabeceras:
            venta_id = cab.venta_id
            cursor.execute("SELECT * FROM ventas.ventas_linea WHERE venta_id = ?", venta_id)
            lineas = cursor.fetchall()
            lineas_columns = [col[0] for col in cursor.description]

            pedidos.append(self._build_pedido_venta(cab, lineas, cab_columns, lineas_columns))

        cursor.close()
        conn.close()
        return pedidos

    def get_pedido(self, venta_id: int):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ventas.ventas_cabecera WHERE venta_id = ?", venta_id)
        cab = cursor.fetchone()
        if not cab:
            return None

        cab_columns = [col[0] for col in cursor.description]

        cursor.execute("SELECT * FROM ventas.ventas_linea WHERE venta_id = ?", venta_id)
        lineas = cursor.fetchall()
        lineas_columns = [col[0] for col in cursor.description]

        return self._build_pedido_venta(cab, lineas, cab_columns, lineas_columns)

    def _build_pedido_venta(self, cab_row, lineas_rows, cab_columns, lineas_columns):
        from version1.ventas.domain.entities import CabeceraPedidoVenta, LineaPedidoVenta, PedidoVenta

        def row_to_dict(row, columns):
            return dict(zip(columns, row))

        cab = CabeceraPedidoVenta(**row_to_dict(cab_row, cab_columns))
        lineas = [LineaPedidoVenta(**row_to_dict(linea, lineas_columns)) for linea in lineas_rows]
        return PedidoVenta(cabecera=cab, lineas=lineas)
    
    def update_pedido_cooperativa(self, venta_id: int, command):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        try:
            # Actualizar cabecera
            cursor.execute("""
                UPDATE ventas.ventas_cabecera
                SET cod_cliente_cooperativa = ?, estado_pedido = ?
                WHERE venta_id = ?
            """, command.cod_cliente_cooperativa, command.estado_pedido, venta_id)

            # Actualizar líneas
            for linea in command.lineas:
                cursor.execute("""
                    UPDATE ventas.ventas_linea
                    SET estado_linea_pedido = ?
                    WHERE venta_id = ? AND venta_linea_id = ?
                """, linea.estado_linea_pedido, venta_id, linea.venta_linea_id)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error actualizando pedido: {str(e)}")
        finally:
            cursor.close()
            conn.close()


