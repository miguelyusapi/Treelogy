-- USE FARMA_SQL;
-- GO

-- CREATE OR ALTER TRIGGER trg_ventas_cabecera_estado_pedido_upper
-- ON ventas.ventas_cabecera
-- AFTER INSERT, UPDATE
-- AS
-- BEGIN
--   SET NOCOUNT ON;

--   UPDATE vc
--   SET vc.estado_pedido = UPPER(vc.estado_pedido)
--   FROM ventas.ventas_cabecera vc
--   INNER JOIN inserted i ON vc.venta_id = i.venta_id
--   WHERE vc.estado_pedido COLLATE Latin1_General_BIN <> UPPER(vc.estado_pedido);
-- END;
-- GO

-- CREATE OR ALTER TRIGGER trg_ventas_linea_estado_linea_pedido_upper
-- ON ventas.ventas_linea
-- AFTER INSERT, UPDATE
-- AS
-- BEGIN
--   SET NOCOUNT ON;

--   UPDATE vl
--   SET vl.estado_linea_pedido = UPPER(vl.estado_linea_pedido)
--   FROM ventas.ventas_linea vl
--   INNER JOIN inserted i ON vl.venta_linea_id = i.venta_linea_id
--   WHERE vl.estado_linea_pedido COLLATE Latin1_General_BIN <> UPPER(vl.estado_linea_pedido);
-- END;
-- GO

-- CREATE OR ALTER TRIGGER trg_compras_cabecera_estado_pedido_upper
-- ON compras.compras_cabecera
-- AFTER INSERT, UPDATE
-- AS
-- BEGIN
--   SET NOCOUNT ON;

--   UPDATE cc
--   SET cc.estado_pedido = UPPER(cc.estado_pedido)
--   FROM compras.compras_cabecera cc
--   INNER JOIN inserted i ON cc.compra_id = i.compra_id
--   WHERE cc.estado_pedido COLLATE Latin1_General_BIN <> UPPER(cc.estado_pedido);
-- END;
-- GO

-- CREATE OR ALTER TRIGGER trg_compras_linea_estado_linea_pedido_upper
-- ON compras.compras_linea
-- AFTER INSERT, UPDATE
-- AS
-- BEGIN
--   SET NOCOUNT ON;

--   UPDATE cl
--   SET cl.estado_linea_pedido = UPPER(cl.estado_linea_pedido)
--   FROM compras.compras_linea cl
--   INNER JOIN inserted i ON cl.compra_linea_id = i.compra_linea_id
--   WHERE cl.estado_linea_pedido COLLATE Latin1_General_BIN <> UPPER(cl.estado_linea_pedido);
-- END;
-- GO