-- 1. Crear base de datos y usarla
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'FARMA_SQL')
  CREATE DATABASE [FARMA_SQL];
GO
USE [FARMA_SQL];
GO

-- 2. Crear esquemas
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ventas')
  EXEC('CREATE SCHEMA ventas');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'compras')
  EXEC('CREATE SCHEMA compras');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stock')
  EXEC('CREATE SCHEMA stock');
GO

-- 3. Tablas de VENTAS
CREATE TABLE ventas.ventas_cabecera (
  venta_id INT IDENTITY(1,1) PRIMARY KEY,
  num_pedido_venta NVARCHAR(255) NULL,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255) NULL,
  acuerdo_venta_asociado NVARCHAR(255) NULL,
  num_pedido_laboratorio NVARCHAR(255) NULL,
  fecha_pedido_farmacia DATE NULL,
  fecha_pedido_cooperativa DATE NULL,
  cod_cliente_cooperativa NVARCHAR(255) NULL,
  estado_pedido NVARCHAR(255) NULL,
  id_cooperativa NVARCHAR(255) NULL
);
GO

-- 3. Tabla ventas.ventas_linea (sin FKs num_pedido_venta ni num_acuerdo_venta)
CREATE TABLE ventas.ventas_linea (
  venta_linea_id INT IDENTITY(1,1) PRIMARY KEY,
  venta_id INT NOT NULL,
  num_pedido_venta NVARCHAR(255) NULL,
  num_linea_pedido_venta NVARCHAR(255) NULL,
  num_pedido_lugonet NVARCHAR(255) NULL,
  num_acuerdo_venta NVARCHAR(255) NULL,
  cod_articulo_cooperativa NVARCHAR(255) NULL,
  cantidad_solicitada INT NULL,
  cantidad_bonificada INT NULL,
  cantidad_confirmada INT NULL,
  pvl DECIMAL(18,2) NULL,
  descuento_porcentaje DECIMAL(18,2) NULL,
  descuento_unitario DECIMAL(18,2) NULL,
  pvl_neto DECIMAL(18,2) NULL,
  cargo_cooperativo DECIMAL(18,2) NULL,
  cod_proveedor_cooperativa NVARCHAR(255) NULL,
  computa_aprovisionamiento BIT NULL,
  ocultar_web BIT NULL,
  no_unnefar BIT NULL,
  estado_linea_pedido NVARCHAR(255) NULL,
  CONSTRAINT FK_ventas_linea_cabecera_id FOREIGN KEY(venta_id)
    REFERENCES ventas.ventas_cabecera(venta_id)
);
GO

-- Tabla ventas.ventas_reporte_movimientos (sin FKs sobre num_pedido_venta ni num_linea_pedido_venta)
CREATE TABLE ventas.ventas_reporte_movimientos (
  venta_mov_id INT IDENTITY(1,1) PRIMARY KEY,
  id_movimiento NVARCHAR(255) NULL,
  num_pedido_venta NVARCHAR(255) NULL,
  num_linea_pedido_venta NVARCHAR(255) NULL,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255) NULL,
  num_albaran NVARCHAR(255) NULL,
  num_linea_albaran NVARCHAR(255) NULL,
  fecha_generacion_albaran DATE NULL,
  fecha_real_movimiento DATE NULL,
  motivo_devolucion NVARCHAR(255) NULL,
  cantidad INT NULL,
  cantidad_bonificada_servida INT NULL,
  lote_calculado BIT NULL,
  lote NVARCHAR(255) NULL,
  fecha_caducidad DATE NULL,
  almacen_origen_pedido_integrado NVARCHAR(255) NULL,
  CONSTRAINT UQ_ventas_rep_mov UNIQUE(cod_cooperativa, id_movimiento)
);
GO

-- 4. Tablas de COMPRAS
CREATE TABLE compras.compras_cabecera (
  compra_id INT IDENTITY(1,1) PRIMARY KEY,
  num_pedido_compra NVARCHAR(255) NULL,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255) NULL,
  cod_proveedor_cooperativa NVARCHAR(255) NULL,
  TipoPedido NVARCHAR(255) NULL,
  dias_aplazamiento INT NULL,
  pvl DECIMAL(18,2) NULL,
  pvl_neto DECIMAL(18,2) NULL,
  precio_libre DECIMAL(18,2) NULL,
  precio_libre_neto DECIMAL(18,2) NULL,
  dto_comercial DECIMAL(18,2) NULL,
  dto_logistico DECIMAL(18,2) NULL,
  dto_pronto_pago DECIMAL(18,2) NULL,
  dto_gestion DECIMAL(18,2) NULL,
  no_unnefar BIT NULL,
  fecha_pedido DATE NULL,
  fecha_prevista_entrega DATE NULL,
  num_acuerdo_compra NVARCHAR(255) NULL,
  estado_pedido NVARCHAR(255) NULL,
  almacen_origen_pedido_integrado NVARCHAR(255) NULL,
  CONSTRAINT UQ_compras_cabecera UNIQUE(cod_cooperativa, num_pedido_compra)
);
GO

CREATE TABLE compras.compras_linea (
  compra_linea_id INT IDENTITY(1,1) PRIMARY KEY,
  compra_id INT  NULL,
  num_pedido_compra NVARCHAR(255)  NULL,
  num_linea_pedido_compra NVARCHAR(255)  NULL,
  cod_articulo_cooperativa NVARCHAR(255)  NULL,
  cantidad_solicitada INT  NULL,
  pvl DECIMAL(18,2)  NULL,
  pvl_neto DECIMAL(18,2)  NULL,
  precio_libre DECIMAL(18,2)  NULL,
  precio_libre_neto DECIMAL(18,2)  NULL,
  dto_comercial DECIMAL(18,2)  NULL,
  dto_logistico DECIMAL(18,2)  NULL,
  dto_pronto_pago DECIMAL(18,2)  NULL,
  dto_gestion DECIMAL(18,2)  NULL,
  pedido_cooperativa NVARCHAR(255)  NULL,
  estado_linea_pedido NVARCHAR(255)  NULL,
  CONSTRAINT UQ_compras_linea UNIQUE(compra_id, num_linea_pedido_compra),
  CONSTRAINT FK_compras_linea_cabecera FOREIGN KEY(compra_id)
    REFERENCES compras.compras_cabecera(compra_id)
);
GO

-- Tabla compras.compras_reporte_movimientos (sin FKs sobre num_pedido_compra ni num_linea_pedido_compra)
CREATE TABLE compras.compras_reporte_movimientos (
  compra_mov_id INT IDENTITY(1,1) PRIMARY KEY,
  id_movimiento NVARCHAR(255)  NULL,
  num_pedido_compra NVARCHAR(255)  NULL,
  num_linea_pedido_compra NVARCHAR(255)  NULL,
  num_albaran NVARCHAR(255)  NULL,
  num_linea_albaran NVARCHAR(255)  NULL,
  fecha_generacion_albaran DATE  NULL,
  fecha_real_movimiento DATE  NULL,
  cantidad INT  NULL,
  motivo_devolucion NVARCHAR(255) NULL,
  lote_calculado BIT  NULL,
  lote NVARCHAR(255)  NULL,
  fecha_caducidad DATE  NULL,
  CONSTRAINT UQ_compras_rep_mov UNIQUE(id_movimiento)
);
GO

-- 5. Tablas de STOCK
CREATE TABLE stock.stock_reporte_regularizaciones (
  stock_regulaciones_id INT IDENTITY(1,1) PRIMARY KEY,
  id_movimiento NVARCHAR(255)  NULL,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255)  NULL,
  fecha_real_movimiento DATE  NULL,
  cod_proveedor_cooperativa NVARCHAR(255)  NULL,
  cod_articulo_cooperativa NVARCHAR(255) NULL,
  cantidad INT  NULL,
  lote_calculado BIT  NULL,
  lote NVARCHAR(255)  NULL,
  fecha_caducidad DATE  NULL,
  CONSTRAINT UQ_stock_reg UNIQUE(cod_cooperativa, id_movimiento)
);
GO

CREATE TABLE stock.stock_reporte (
  stock_reporte_id INT IDENTITY(1,1) PRIMARY KEY,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255)  NULL,
  fecha_reporte DATE  NULL,
  cod_articulo_cooperativa NVARCHAR(255) NULL,
  stock INT  NULL,
  stock_no_disponible INT  NULL,
  stock_pendiente_colocar INT  NULL,
  stock_en_curso INT  NULL,
  CONSTRAINT UQ_stock_rep UNIQUE(cod_cooperativa, puerta, fecha_reporte, cod_articulo_cooperativa)
);
GO
