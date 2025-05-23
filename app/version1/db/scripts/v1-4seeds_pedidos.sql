USE FARMA_SQL;
GO

-- =============================
-- 1) VENTAS: CABECERAS Y LÍNEAS DE PEDIDO
-- Fechas ajustadas: fecha_pedido_cooperativa >= fecha_pedido_farmacia
-- =============================

-- Pedido de ventas 1 (ABIERTO)
INSERT INTO ventas.ventas_cabecera
  (num_pedido_venta, cod_cooperativa, puerta, acuerdo_venta_asociado,
   fecha_pedido_farmacia, fecha_pedido_cooperativa, estado_pedido, id_cooperativa)
VALUES
  ('PEDV001', 'COOP1', 'P1', 'ACV001',
   '2025-05-17', '2025-05-18', 'ABIERTO', 'COOPERATIVA1');
-- Captura el ID en la misma transacción
DECLARE @vid1 INT = SCOPE_IDENTITY();

-- Líneas para PEDV001
INSERT INTO ventas.ventas_linea
  (venta_id, num_pedido_venta, num_linea_pedido_venta,
   num_pedido_lugonet, num_acuerdo_venta, cod_articulo_cooperativa,
   cantidad_solicitada, cantidad_bonificada, cantidad_confirmada,
   pvl, descuento_porcentaje, descuento_unitario, pvl_neto,
   cargo_cooperativo, cod_proveedor_cooperativa,
   computa_aprovisionamiento, ocultar_web, no_unnefar,
   estado_linea_pedido)
VALUES
  (@vid1, 'PEDV001', '1', NULL, 'ACV001', 'ART123',
   10, 0, 10,
   15.50, NULL, NULL, 155.00,
   NULL, 'PROV01',
   1, 0, 0,
   'ABIERTO'),
  (@vid1, 'PEDV001', '2', NULL, 'ACV001', 'ART456',
   5, 1, 6,
   20.00, 0.00, 0.00, 120.00,
   2.00, 'PROV02',
   1, 0, 0,
   'ABIERTO');

-- Pedido de ventas 2 (COMPLETADO)
INSERT INTO ventas.ventas_cabecera
  (num_pedido_venta, cod_cooperativa, puerta, acuerdo_venta_asociado,
   fecha_pedido_farmacia, fecha_pedido_cooperativa, estado_pedido, id_cooperativa)
VALUES
  ('PEDV002', 'COOP2', 'P2', 'ACV002',
   '2025-05-15', '2025-05-16', 'cerrado', "COOPERATIVA2");
DECLARE @vid2 INT = SCOPE_IDENTITY();

-- Líneas para PEDV002
INSERT INTO ventas.ventas_linea
  (venta_id, num_pedido_venta, num_linea_pedido_venta,
   num_pedido_lugonet, num_acuerdo_venta, cod_articulo_cooperativa,
   cantidad_solicitada, cantidad_bonificada, cantidad_confirmada,
   pvl, descuento_porcentaje, descuento_unitario, pvl_neto,
   cargo_cooperativo, cod_proveedor_cooperativa,
   computa_aprovisionamiento, ocultar_web, no_unnefar,
   estado_linea_pedido)
VALUES
  (@vid2, 'PEDV002', '1', NULL, 'ACV002', 'ART789',
   8, 0, 8,
   12.75, NULL, NULL, 102.00,
   NULL, 'PROV03',
   1, 0, 0,
   'CERRADO'),
  (@vid2, 'PEDV002', '2', NULL, 'ACV002', 'ART321',
   15, 2, 17,
   7.20, 0.00, 0.00, 122.40,
   1.50, 'PROV01',
   1, 0, 0,
   'CERRADO');

GO

-- ============================================
-- 2) VENTAS: REPORTE DE MOVIMIENTOS
-- ============================================

INSERT INTO ventas.ventas_reporte_movimientos
  (id_movimiento, num_pedido_venta, num_linea_pedido_venta,
   cod_cooperativa, puerta, num_albaran, num_linea_albaran,
   fecha_generacion_albaran, fecha_real_movimiento,
   motivo_devolucion, cantidad, cantidad_bonificada_servida,
   lote_calculado, lote, fecha_caducidad, almacen_origen_pedido_integrado)
VALUES
  ('MOVS001', 'PEDV001', '1', 'COOP1', 'P1', 'ALB001', '1',
   '2025-05-19', '2025-05-19',
   NULL, 10, 0,
   0, 'L001', '2026-05-19', 'ALM1'),
  ('MOVS002', 'PEDV001', '2', 'COOP1', 'P1', 'ALB002', '1',
   '2025-05-20', '2025-05-20',
   NULL, 6, 1,
   0, 'L002', '2026-05-20', 'ALM1');

INSERT INTO ventas.ventas_reporte_movimientos
  (id_movimiento, num_pedido_venta, num_linea_pedido_venta,
   cod_cooperativa, puerta, num_albaran, num_linea_albaran,
   fecha_generacion_albaran, fecha_real_movimiento,
   motivo_devolucion, cantidad, cantidad_bonificada_servida,
   lote_calculado, lote, fecha_caducidad, almacen_origen_pedido_integrado)
VALUES
  ('MOVS003', 'PEDV002', '1', 'COOP2', 'P2', 'ALB003', '1',
   '2025-05-17', '2025-05-17',
   NULL, 8, 0,
   0, 'L003', '2026-05-17', 'ALM2');

GO

-- ==========================================
-- 3) COMPRAS: CABECERA Y LÍNEAS DE PEDIDO
-- Fechas ajustadas: fecha_prevista_entrega >= fecha_pedido
-- ==========================================

INSERT INTO compras.compras_cabecera
  (num_pedido_compra, cod_cooperativa, puerta, cod_proveedor_cooperativa,
   TipoPedido, dias_aplazamiento, pvl, pvl_neto,
   precio_libre, precio_libre_neto,
   dto_comercial, dto_logistico, dto_pronto_pago, dto_gestion,
   no_unnefar, fecha_pedido, fecha_prevista_entrega,
   num_acuerdo_compra, estado_pedido, almacen_origen_pedido_integrado)
VALUES
  ('PCP001', 'COOP1', 'P1', 'PROV01',
   'NORMAL', 30, 200.00, 180.00,
   220.00, 198.00,
   5.00, 2.00, 1.00, 0.50,
   0, '2025-05-14', '2025-05-21',
   'ACC001', 'abierto', 'ALM1');
DECLARE @cid1 INT = SCOPE_IDENTITY();

INSERT INTO compras.compras_linea
  (compra_id, num_pedido_compra, num_linea_pedido_compra,
   cod_articulo_cooperativa, cantidad_solicitada,
   pvl, pvl_neto,
   precio_libre, precio_libre_neto,
   dto_comercial, dto_logistico, dto_pronto_pago, dto_gestion,
   pedido_cooperativa, estado_linea_pedido)
VALUES
  (@cid1, 'PCP001', '1', 'ART123', 12,
   10.00, 120.00,
   11.00, 132.00,
   1.00, 0.50, 0.25, 0.10,
   "PCOOP001", 'ABIERTO'),
  (@cid1, 'PCP001', '2', 'ART456', 20,
   8.50, 170.00,
   9.00, 180.00,
   1.50, 0.75, 0.30, 0.15,
   "PCOOP002", 'abierto');

INSERT INTO compras.compras_cabecera
  (num_pedido_compra, cod_cooperativa, puerta, cod_proveedor_cooperativa,
   TipoPedido, dias_aplazamiento, pvl, pvl_neto,
   precio_libre, precio_libre_neto,
   dto_comercial, dto_logistico, dto_pronto_pago, dto_gestion,
   no_unnefar, fecha_pedido, fecha_prevista_entrega,
   num_acuerdo_compra, estado_pedido, almacen_origen_pedido_integrado)
VALUES
  ('PCP002', 'COOP2', 'P2', 'PROV02',
   'URGENTE', 15, 350.00, 315.00,
   380.00, 342.00,
   10.00, 3.00, 1.50, 0.75,
   1, '2025-05-10', '2025-05-15',
   'ACC002', 'abierto', 'ALM2');
DECLARE @cid2 INT = SCOPE_IDENTITY();

INSERT INTO compras.compras_linea
  (compra_id, num_pedido_compra, num_linea_pedido_compra,
   cod_articulo_cooperativa, cantidad_solicitada,
   pvl, pvl_neto,
   precio_libre, precio_libre_neto,
   dto_comercial, dto_logistico, dto_pronto_pago, dto_gestion,
   pedido_cooperativa, estado_linea_pedido)
VALUES
  (@cid2, 'PCP002', '1', 'ART789', 5,
   40.00, 200.00,
   45.00, 225.00,
   2.00, 1.00, 0.50, 0.25,
   "PCOOP003", 'abierto'),
  (@cid2, 'PCP002', '2', 'ART321', 10,
   25.00, 250.00,
   28.00, 280.00,
   3.00, 1.50, 0.75, 0.35,
   "PCOOP004", 'abierto');

GO

-- ============================================
-- 4) COMPRAS: REPORTE DE MOVIMIENTOS
-- ============================================

INSERT INTO compras.compras_reporte_movimientos
  (id_movimiento, num_pedido_compra, num_linea_pedido_compra,
   num_albaran, num_linea_albaran,
   fecha_generacion_albaran, fecha_real_movimiento,
   cantidad, motivo_devolucion, lote_calculado,
   lote, fecha_caducidad)
VALUES
  ('MOVC001', 'PCP001', '1', 'ALBC001', '1',
   '2025-05-20', '2025-05-20',
   12, NULL, 1,
   'L100', '2026-05-20'),
  ('MOVC002', 'PCP002', '2', 'ALBC002', '1',
   '2025-05-15', '2025-05-15',
   10, NULL, 0,
   'L200', '2026-05-15');

GO