from version1.ventas.application.ports import PedidoVentaRepository
from version1.ventas.adapters.dto_pharma import PedidoVentaPharmaEditable
from version1.ventas.adapters.dto_coop import PedidoVentaCoopEditable
from version1.ventas.domain.entities import PedidoVenta
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

            cab = pedido.cabecera

            # === Construir campos y valores dinámicos para la cabecera ===
            campos = [
                "num_pedido_venta", "cod_cooperativa", "puerta", "acuerdo_venta_asociado",
                "num_pedido_laboratorio", "fecha_pedido_farmacia", "fecha_pedido_cooperativa",
                "cod_cliente_cooperativa", "estado_pedido"
            ]
            valores = [
                cab.num_pedido_venta, cab.cod_cooperativa, cab.puerta, cab.acuerdo_venta_asociado,
                cab.num_pedido_laboratorio, cab.fecha_pedido_farmacia, cab.fecha_pedido_cooperativa,
                cab.cod_cliente_cooperativa, cab.estado_pedido
            ]

            # Si existe id_cooperativa, la añadimos
            if hasattr(cab, "id_cooperativa") and cab.id_cooperativa is not None:
                campos.append("id_cooperativa")
                valores.append(cab.id_cooperativa)

            campos_sql = ", ".join(campos)
            placeholders_sql = ", ".join(["?"] * len(valores))

            cursor.execute(
                f"""
                INSERT INTO ventas.ventas_cabecera ({campos_sql})
                OUTPUT INSERTED.venta_id
                VALUES ({placeholders_sql})
                """,
                *valores
            )

            venta_id = cursor.fetchone()[0]

            # === Insertar líneas ===
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

    def get_pedidos(self, cod_cooperativa=None, estado_pedido=None, id_cooperativa=None):
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
        if id_cooperativa:
            query += " AND id_cooperativa = ?"
            params.append(id_cooperativa)

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
        from inspect import signature

        def row_to_dict(row, columns):
            return dict(zip(columns, row))

        def filter_kwargs(data_dict, cls):
            valid_keys = signature(cls.__init__).parameters.keys()
            return {k: v for k, v in data_dict.items() if k in valid_keys and k != 'self'}

        cab_raw = row_to_dict(cab_row, cab_columns)
        cab_data = filter_kwargs(cab_raw, CabeceraPedidoVenta)
        cab = CabeceraPedidoVenta(**cab_data)

        lineas = []
        for linea_row in lineas_rows:
            linea_raw = row_to_dict(linea_row, lineas_columns)
            linea_data = filter_kwargs(linea_raw, LineaPedidoVenta)
            lineas.append(LineaPedidoVenta(**linea_data))

        return PedidoVenta(cabecera=cab, lineas=lineas)
    
    def update_pedido_coop(self, venta_id: int, data: PedidoVentaCoopEditable):
        conn = None
        cursor = None

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Actualizar cabecera si existe
            if data.cabecera:
                set_clauses = []
                params = []

                for field, value in data.cabecera.dict(exclude_unset=True).items():
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

                if set_clauses:
                    query = f"""
                        UPDATE ventas.ventas_cabecera
                        SET {', '.join(set_clauses)}
                        WHERE venta_id = ?
                    """
                    cursor.execute(query, *params, venta_id)

            # Actualizar líneas si existen
            if data.lineas:
                for linea in data.lineas:
                    linea_data = linea.dict(exclude_unset=True)
                    if "venta_linea_id" not in linea_data:
                        continue  # O lanza excepción si prefieres obligarlo

                    venta_linea_id = linea_data.pop("venta_linea_id")
                    set_clauses = []
                    params = []

                    for field, value in linea_data.items():
                        set_clauses.append(f"{field} = ?")
                        params.append(value)

                    if set_clauses:
                        query = f"""
                            UPDATE ventas.ventas_linea
                            SET {', '.join(set_clauses)}
                            WHERE venta_id = ? AND venta_linea_id = ?
                        """
                        cursor.execute(query, *params, venta_id, venta_linea_id)

            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar el pedido cooperativa: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update_pedido_pharma(self, venta_id: int, data: PedidoVentaPharmaEditable):
        conn = None
        cursor = None

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Actualizar cabecera
            if data.cabecera:
                set_clauses = []
                params = []

                for field, value in data.cabecera.dict(exclude_unset=True).items():
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

                if set_clauses:
                    query = f"""
                        UPDATE ventas.ventas_cabecera
                        SET {', '.join(set_clauses)}
                        WHERE venta_id = ?
                    """
                    cursor.execute(query, *params, venta_id)

            # Actualizar líneas
            if data.lineas:
                for linea in data.lineas:
                    linea_data = linea.dict(exclude_unset=True)
                    if "venta_linea_id" not in linea_data:
                        continue

                    venta_linea_id = linea_data.pop("venta_linea_id")
                    set_clauses = []
                    params = []

                    for field, value in linea_data.items():
                        set_clauses.append(f"{field} = ?")
                        params.append(value)

                    if set_clauses:
                        query = f"""
                            UPDATE ventas.ventas_linea
                            SET {', '.join(set_clauses)}
                            WHERE venta_linea_id = ?
                        """
                        cursor.execute(query, *params, venta_linea_id)

            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar el pedido pharma: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


