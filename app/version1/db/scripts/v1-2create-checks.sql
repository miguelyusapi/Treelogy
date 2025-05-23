USE FARMA_SQL;
GO

--------------------------------------------------------------------------------
-- 1) VENTAS: CABECERA
-- Asegura que la fecha de pedido cooperativa no sea anterior
-- a la fecha de pedido farmacia. :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}
--------------------------------------------------------------------------------
ALTER TABLE ventas.ventas_cabecera
  ADD CONSTRAINT CK_ventas_cabecera_fecha CHECK (
    fecha_pedido_cooperativa >= fecha_pedido_farmacia
  );
GO

ALTER TABLE ventas.ventas_cabecera
  ALTER COLUMN estado_pedido VARCHAR(7) NULL;
GO

ALTER TABLE ventas.ventas_cabecera
  ADD CONSTRAINT CK_ventas_cabecera_estado_pedido
  CHECK (estado_pedido IN ('ABIERTO', 'CERRADO'));
GO
--------------------------------------------------------------------------------
-- 2) VENTAS: LÍNEA
-- Cantidades ≥0, PVL ≥0, descuento_pct entre 0 y 100,
-- descuento_unitario ≥0, PVL neto ≥0, cargo cooperativo ≥0. :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}
--------------------------------------------------------------------------------
ALTER TABLE ventas.ventas_linea
  ADD 
    CONSTRAINT CK_ventas_linea_cant_nonneg CHECK (
      cantidad_solicitada  >= 0 AND
      cantidad_bonificada  >= 0 AND
      cantidad_confirmada  >= 0
    ),
    CONSTRAINT CK_ventas_linea_pvl_nonneg CHECK (
      pvl >= 0
    ),
    CONSTRAINT CK_ventas_linea_desc_pct CHECK (
      descuento_porcentaje IS NULL OR 
      (descuento_porcentaje BETWEEN 0 AND 100)
    ),
    CONSTRAINT CK_ventas_linea_desc_unit_nonneg CHECK (
      descuento_unitario IS NULL OR 
      descuento_unitario >= 0
    ),
    CONSTRAINT CK_ventas_linea_pvlneto_nonneg CHECK (
      pvl_neto >= 0
    ),
    CONSTRAINT CK_ventas_linea_cargo_nonneg CHECK (
      cargo_cooperativo IS NULL OR
      cargo_cooperativo >= 0
    );
GO

ALTER TABLE ventas.ventas_linea
  ALTER COLUMN estado_linea_pedido VARCHAR(7) NULL;
GO

ALTER TABLE ventas.ventas_linea
  ADD CONSTRAINT CK_ventas_linea_estado_pedido
  CHECK (estado_linea_pedido IN ('ABIERTO', 'CERRADO'));
GO

--------------------------------------------------------------------------------
-- 3) VENTAS: REPORTE DE MOVIMIENTOS
-- Cantidades ≥0. :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}
--------------------------------------------------------------------------------
ALTER TABLE ventas.ventas_reporte_movimientos
  ADD
    CONSTRAINT CK_ventas_rep_mov_cant_nonneg CHECK (
      cantidad                 >= 0 AND
      cantidad_bonificada_servida >= 0
    );
GO

--------------------------------------------------------------------------------
-- 4) COMPRAS: CABECERA
-- dias_aplazamiento ≥0, precios y totales ≥0,
-- fecha_prevista_entrega ≥ fecha_pedido. :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}
--------------------------------------------------------------------------------
ALTER TABLE compras.compras_cabecera
  ADD 
    CONSTRAINT CK_compras_cabecera_days_nonneg CHECK (
      dias_aplazamiento >= 0
    ),
    CONSTRAINT CK_compras_cabecera_pvl_nonneg CHECK (
      pvl      >= 0 AND
      pvl_neto >= 0 AND
      precio_libre >= 0 AND
      precio_libre_neto >= 0
    ),
    CONSTRAINT CK_compras_cabecera_dto_nonneg CHECK (
      dto_comercial >= 0 AND
      dto_logistico >= 0 AND
      dto_pronto_pago >= 0 AND
      dto_gestion    >= 0
    ),
    CONSTRAINT CK_compras_cabecera_fecha CHECK (
      fecha_prevista_entrega >= fecha_pedido
    );
GO
ALTER TABLE compras.compras_cabecera
  ALTER COLUMN estado_pedido VARCHAR(7) NULL;
GO

ALTER TABLE compras.compras_cabecera
  ADD CONSTRAINT CK_compras_cabecera_estado_pedido
  CHECK (estado_pedido IN ('ABIERTO', 'CERRADO'));
GO

--------------------------------------------------------------------------------
-- 5) COMPRAS: LÍNEA
-- Cantidad ≥0, precios y descuentos ≥0. :contentReference[oaicite:8]{index=8}:contentReference[oaicite:9]{index=9}
--------------------------------------------------------------------------------
ALTER TABLE compras.compras_linea
  ADD
    CONSTRAINT CK_compras_linea_cant_nonneg CHECK (
      cantidad_solicitada >= 0
    ),
    CONSTRAINT CK_compras_linea_pvl_nonneg CHECK (
      pvl           >= 0 AND
      pvl_neto      >= 0 AND
      precio_libre  >= 0 AND
      precio_libre_neto >= 0
    ),
    CONSTRAINT CK_compras_linea_dto_nonneg CHECK (
      dto_comercial >= 0 AND
      dto_logistico >= 0 AND
      dto_pronto_pago >= 0 AND
      dto_gestion    >= 0
    );
GO

ALTER TABLE compras.compras_linea
  ALTER COLUMN estado_linea_pedido VARCHAR(7) NULL;
GO

ALTER TABLE compras.compras_linea
  ADD CONSTRAINT CK_compras_linea_estado_pedido
  CHECK (estado_linea_pedido IN ('ABIERTO', 'CERRADO'));
GO
--------------------------------------------------------------------------------
-- 6) COMPRAS: REPORTE DE MOVIMIENTOS
-- Cantidad ≥0. :contentReference[oaicite:10]{index=10}:contentReference[oaicite:11]{index=11}
--------------------------------------------------------------------------------
ALTER TABLE compras.compras_reporte_movimientos
  ADD CONSTRAINT CK_compras_rep_mov_cant_nonneg CHECK (
    cantidad >= 0
  );
GO

--------------------------------------------------------------------------------
-- 7) STOCK: REGULARIZACIONES
-- Cantidad ≥0. :contentReference[oaicite:12]{index=12}:contentReference[oaicite:13]{index=13}
--------------------------------------------------------------------------------
ALTER TABLE stock.stock_reporte_regularizaciones
  ADD CONSTRAINT CK_stock_reg_cant_nonneg CHECK (
    cantidad >= 0
  );
GO

--------------------------------------------------------------------------------
-- 8) STOCK: REPORTE
-- Stocks ≥0. :contentReference[oaicite:14]{index=14}:contentReference[oaicite:15]{index=15}
--------------------------------------------------------------------------------
ALTER TABLE stock.stock_reporte
  ADD
    CONSTRAINT CK_stock_rep_nonneg CHECK (
      stock                 >= 0 AND
      stock_no_disponible   >= 0 AND
      stock_pendiente_colocar >= 0 AND
      stock_en_curso        >= 0
    );
GO
