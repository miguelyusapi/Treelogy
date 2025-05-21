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
  CONSTRAINT UQ_ventas_cabecera UNIQUE(cod_cooperativa, num_pedido_venta)
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
  id_movimiento NVARCHAR(255) NOT NULL,
  num_pedido_venta NVARCHAR(255) NOT NULL,
  num_linea_pedido_venta NVARCHAR(255) NOT NULL,
  cod_cooperativa NVARCHAR(255) NOT NULL,
  puerta NVARCHAR(255) NOT NULL,
  num_albaran NVARCHAR(255) NOT NULL,
  num_linea_albaran NVARCHAR(255) NOT NULL,
  fecha_generacion_albaran DATE NOT NULL,
  fecha_real_movimiento DATE NOT NULL,
  motivo_devolucion NVARCHAR(255) NULL,
  cantidad INT NOT NULL,
  cantidad_bonificada_servida INT NOT NULL,
  lote_calculado BIT NULL,
  lote NVARCHAR(255) NULL,
  fecha_caducidad DATE NULL,
  almacen_origen_pedido_integrado NVARCHAR(255) NOT NULL,
  CONSTRAINT UQ_ventas_rep_mov UNIQUE(cod_cooperativa, id_movimiento)
);
GO

-- 4. Tablas de COMPRAS
CREATE TABLE compras.compras_cabecera (
  compra_id INT IDENTITY(1,1) PRIMARY KEY,
  num_pedido_compra NVARCHAR(255) NOT NULL,
  cod_cooperativa NVARCHAR(255) NOT NULL,
  puerta NVARCHAR(255) NOT NULL,
  cod_proveedor_cooperativa NVARCHAR(255) NOT NULL,
  TipoPedido NVARCHAR(255) NOT NULL,
  dias_aplazamiento INT NOT NULL,
  pvl DECIMAL(18,2) NOT NULL,
  pvl_neto DECIMAL(18,2) NOT NULL,
  precio_libre DECIMAL(18,2) NOT NULL,
  precio_libre_neto DECIMAL(18,2) NOT NULL,
  dto_comercial DECIMAL(18,2) NOT NULL,
  dto_logistico DECIMAL(18,2) NOT NULL,
  dto_pronto_pago DECIMAL(18,2) NOT NULL,
  dto_gestion DECIMAL(18,2) NOT NULL,
  no_unnefar BIT NOT NULL,
  fecha_pedido DATE NOT NULL,
  fecha_prevista_entrega DATE NOT NULL,
  num_acuerdo_compra NVARCHAR(255) NOT NULL,
  estado_pedido NVARCHAR(255) NOT NULL,
  almacen_origen_pedido_integrado NVARCHAR(255) NULL,
  CONSTRAINT UQ_compras_cabecera UNIQUE(cod_cooperativa, num_pedido_compra)
);
GO

CREATE TABLE compras.compras_linea (
  compra_linea_id INT IDENTITY(1,1) PRIMARY KEY,
  compra_id INT NOT NULL,
  num_pedido_compra NVARCHAR(255) NOT NULL,
  num_linea_pedido_compra NVARCHAR(255) NOT NULL,
  cod_articulo_cooperativa NVARCHAR(255) NOT NULL,
  cantidad_solicitada INT NOT NULL,
  pvl DECIMAL(18,2) NOT NULL,
  pvl_neto DECIMAL(18,2) NOT NULL,
  precio_libre DECIMAL(18,2) NOT NULL,
  precio_libre_neto DECIMAL(18,2) NOT NULL,
  dto_comercial DECIMAL(18,2) NOT NULL,
  dto_logistico DECIMAL(18,2) NOT NULL,
  dto_pronto_pago DECIMAL(18,2) NOT NULL,
  dto_gestion DECIMAL(18,2) NOT NULL,
  pedido_cooperativa NVARCHAR(255) NOT NULL,
  estado_linea_pedido NVARCHAR(255) NOT NULL,
  CONSTRAINT UQ_compras_linea UNIQUE(compra_id, num_linea_pedido_compra),
  CONSTRAINT FK_compras_linea_cabecera FOREIGN KEY(compra_id)
    REFERENCES compras.compras_cabecera(compra_id)
);
GO

-- Tabla compras.compras_reporte_movimientos (sin FKs sobre num_pedido_compra ni num_linea_pedido_compra)
CREATE TABLE compras.compras_reporte_movimientos (
  compra_mov_id INT IDENTITY(1,1) PRIMARY KEY,
  id_movimiento NVARCHAR(255) NOT NULL,
  num_pedido_compra NVARCHAR(255) NOT NULL,
  num_linea_pedido_compra NVARCHAR(255) NOT NULL,
  num_albaran NVARCHAR(255) NOT NULL,
  num_linea_albaran NVARCHAR(255) NOT NULL,
  fecha_generacion_albaran DATE NOT NULL,
  fecha_real_movimiento DATE NOT NULL,
  cantidad INT NOT NULL,
  motivo_devolucion NVARCHAR(255) NULL,
  lote_calculado BIT NOT NULL,
  lote NVARCHAR(255) NOT NULL,
  fecha_caducidad DATE NOT NULL,
  CONSTRAINT UQ_compras_rep_mov UNIQUE(id_movimiento)
);
GO

-- 5. Tablas de STOCK
CREATE TABLE stock.stock_reporte_regularizaciones (
  stock_regulaciones_id INT IDENTITY(1,1) PRIMARY KEY,
  id_movimiento NVARCHAR(255) NOT NULL,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255) NOT NULL,
  fecha_real_movimiento DATE NOT NULL,
  cod_proveedor_cooperativa NVARCHAR(255) NOT NULL,
  cod_articulo_cooperativa NVARCHAR(255) NULL,
  cantidad INT NOT NULL,
  lote_calculado BIT NOT NULL,
  lote NVARCHAR(255) NOT NULL,
  fecha_caducidad DATE NOT NULL,
  CONSTRAINT UQ_stock_reg UNIQUE(cod_cooperativa, id_movimiento)
);
GO

CREATE TABLE stock.stock_reporte (
  stock_reporte_id INT IDENTITY(1,1) PRIMARY KEY,
  cod_cooperativa NVARCHAR(255) NULL,
  puerta NVARCHAR(255) NOT NULL,
  fecha_reporte DATE NOT NULL,
  cod_articulo_cooperativa NVARCHAR(255) NULL,
  stock INT NOT NULL,
  stock_no_disponible INT NOT NULL,
  stock_pendiente_colocar INT NOT NULL,
  stock_en_curso INT NOT NULL,
  CONSTRAINT UQ_stock_rep UNIQUE(cod_cooperativa, puerta, fecha_reporte, cod_articulo_cooperativa)
);
GO
