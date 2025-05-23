# sqlserver_pedido_repository.py

import pyodbc
from version1.compras.domain.entities import PedidoCompra
from version1.compras.application.use_case_pharma.create_pedido_pharma import PedidoCompraRepository
from version1.compras.adapters.dto_pharma import PedidoCompraPharmaEditableDTO,PedidoCompraPharmaEscrituraDTO,PedidoCompraPharmaLecturaDTO
from version1.compras.adapters.dto_coop import  PedidoCompraCoopEditableDTO,PedidoCompraCoopEscrituraDTO,PedidoCompraCoopLecturaDTO

class SqlServerPedidoRepository(PedidoCompraRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def save(self, pedido: PedidoCompra) -> None:
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        try:
            # --- 1) INSERT CABECERA y capturar el ID con OUTPUT … INTO
            sql_cab = """
            SET NOCOUNT ON;
            DECLARE @NewIds TABLE (id INT);

            INSERT INTO compras.compras_cabecera (
                num_pedido_compra,
                cod_cooperativa,
                puerta,
                cod_proveedor_cooperativa,
                tipo_pedido,
                dias_aplazamiento,
                pvl,
                pvl_neto,
                precio_libre,
                precio_libre_neto,
                dto_comercial,
                dto_logistico,
                dto_pronto_pago,
                dto_gestion,
                no_unnefar,
                fecha_pedido,
                fecha_prevista_entrega,
                num_acuerdo_compra,
                estado_pedido,
                almacen_origen_pedido_integrado,
                id_cooperativa
            )
            OUTPUT INSERTED.compra_id INTO @NewIds
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

            SELECT id FROM @NewIds;
            """
            cab = pedido.cabecera
            params = [
                cab.num_pedido_compra,
                cab.cod_cooperativa,
                cab.puerta,
                cab.cod_proveedor_cooperativa,
                cab.tipo_pedido,
                cab.dias_aplazamiento,
                cab.pvl,
                cab.pvl_neto,
                cab.precio_libre,
                cab.precio_libre_neto,
                cab.dto_comercial,
                cab.dto_logistico,
                cab.dto_pronto_pago,
                cab.dto_gestion,
                cab.no_unnefar,
                cab.fecha_pedido,
                cab.fecha_prevista_entrega,
                cab.num_acuerdo_compra,
                cab.estado_pedido,
                cab.almacen_origen_pedido_integrado,
                cab.id_cooperativa
            ]
            cursor.execute(sql_cab, params)

            # será el único result-set que devuelve una fila con el nuevo ID
            row = cursor.fetchone()
            if not row:
                raise RuntimeError("No se recuperó compra_id tras el INSERT")
            compra_id = row[0]

            # --- 2) INSERTAR LÍNEAS
            sql_linea = """
            INSERT INTO compras.compras_linea (
                compra_id,
                num_pedido_compra,
                num_linea_pedido_compra,
                cod_articulo_cooperativa,
                cantidad_solicitada,
                pvl,
                pvl_neto,
                precio_libre,
                precio_libre_neto,
                dto_comercial,
                dto_logistico,
                dto_pronto_pago,
                dto_gestion,
                pedido_cooperativa,
                estado_linea_pedido
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            for linea in pedido.lineas:
                cursor.execute(sql_linea, [
                    compra_id,
                    linea.num_pedido_compra,
                    linea.num_linea_pedido_compra,
                    linea.cod_articulo_cooperativa,
                    linea.cantidad_solicitada,
                    linea.pvl,
                    linea.pvl_neto,
                    linea.precio_libre,
                    linea.precio_libre_neto,
                    linea.dto_comercial,
                    linea.dto_logistico,
                    linea.dto_pronto_pago,
                    linea.dto_gestion,
                    linea.pedido_cooperativa,
                    linea.estado_linea_pedido
                ])

            conn.commit()

        except:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    def get_pedido(self, compra_id: int):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM compras.compras_cabecera WHERE compra_id = ?", compra_id)
        cab = cursor.fetchone()
        if not cab:
            return None

        cab_columns = [col[0] for col in cursor.description]

        cursor.execute("SELECT * FROM compras.compras_linea WHERE compra_id = ?", compra_id)
        lineas = cursor.fetchall()
        lineas_columns = [col[0] for col in cursor.description]

        return self._build_pedido_compra(cab, lineas, cab_columns, lineas_columns)
    
    def get_pedidos(self, cod_cooperativa=None, estado_pedido=None, id_cooperativa=None):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        query = "SELECT * FROM compras.compras_cabecera WHERE 1=1"
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
            compra_id = cab.compra_id
            cursor.execute("SELECT * FROM compras.compras_linea WHERE compra_id = ?", compra_id)
            lineas = cursor.fetchall()
            lineas_columns = [col[0] for col in cursor.description]

            pedidos.append(self._build_pedido_compra(cab, lineas, cab_columns, lineas_columns))

        cursor.close()
        conn.close()
        return pedidos
    
    def _build_pedido_compra(self, cab_row, lineas_rows, cab_columns, lineas_columns):
        from version1.compras.domain.entities import CabeceraPedidoCompra, LineaPedidoCompra, PedidoCompra
        from inspect import signature

        def row_to_dict(row, columns):
            return dict(zip(columns, row))

        def filter_kwargs(data_dict, cls):
            valid_keys = signature(cls.__init__).parameters.keys()
            return {k: v for k, v in data_dict.items() if k in valid_keys and k != 'self'}

        cab_raw = row_to_dict(cab_row, cab_columns)
        cab_data = filter_kwargs(cab_raw, CabeceraPedidoCompra)
        cab = CabeceraPedidoCompra(**cab_data)

        lineas = []
        for linea_row in lineas_rows:
            linea_raw = row_to_dict(linea_row, lineas_columns)
            linea_data = filter_kwargs(linea_raw, LineaPedidoCompra)
            lineas.append(LineaPedidoCompra(**linea_data))

        return PedidoCompra(cabecera=cab, lineas=lineas)

    def update_pedido_coop(self, compra_id: int, data: PedidoCompraCoopEditableDTO):
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
                        UPDATE compras.compras_cabecera
                        SET {', '.join(set_clauses)}
                        WHERE compra_id = ?
                    """
                    cursor.execute(query, *params, compra_id)

            # Actualizar líneas si existen
            if data.lineas:
                for linea in data.lineas:
                    linea_data = linea.dict(exclude_unset=True)

                    compra_id_linea = linea_data.pop("compra_id_linea", None)
                    if compra_id_linea is None:
                        # Si no hay ID de línea, ignora o lanza error
                        continue

                    set_clauses = []
                    params = []

                    for field, value in linea_data.items():
                        set_clauses.append(f"{field} = ?")
                        params.append(value)

                    if set_clauses:
                        query = f"""
                            UPDATE compras.compras_linea
                            SET {', '.join(set_clauses)}
                            WHERE compra_linea_id = ?
                        """
                        cursor.execute(query, *params, compra_id_linea)

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


    def update_pedido_pharma(self, compra_id: int, data: PedidoCompraPharmaEditableDTO):
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
                        UPDATE compras.compras_cabecera
                        SET {', '.join(set_clauses)}
                        WHERE compra_id = ?
                    """
                    cursor.execute(query, *params, compra_id)

            # Actualizar líneas si existen
            if data.lineas:
                for linea in data.lineas:
                    linea_data = linea.dict(exclude_unset=True)

                    compra_id_linea = linea_data.pop("compra_id_linea", None)
                    if compra_id_linea is None:
                        continue

                    set_clauses = []
                    params = []

                    for field, value in linea_data.items():
                        set_clauses.append(f"{field} = ?")
                        params.append(value)

                    if set_clauses:
                        query = f"""
                            UPDATE compras.compras_linea
                            SET {', '.join(set_clauses)}
                            WHERE compra_linea_id = ?
                        """
                        cursor.execute(query, *params, compra_id_linea)

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
                
