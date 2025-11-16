-- 🛠️ Script Optimizado y Corregido para MySQL 🛠️

-- Desactivar temporalmente la verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 0;

-- Tablas con dependencias (Se asume que 'control_detallepedido' y 'control_pedido'
-- deben vaciarse primero si existen dependencias)
TRUNCATE TABLE control_detallepedido;
TRUNCATE TABLE control_pedido;

TRUNCATE TABLE store_imagenproducto;
TRUNCATE TABLE store_panelsip_categorias;
TRUNCATE TABLE store_kitconstruccion_categorias;
TRUNCATE TABLE store_inventario;

-- Luego las tablas principales
TRUNCATE TABLE store_panelsip;
TRUNCATE TABLE store_kitconstruccion;
TRUNCATE TABLE control_local;
TRUNCATE TABLE store_categoria;

-- Restaurar la verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- Resetear AUTO_INCREMENT en MySQL
ALTER TABLE store_categoria AUTO_INCREMENT = 11;
ALTER TABLE control_local AUTO_INCREMENT = 6;
ALTER TABLE store_panelsip AUTO_INCREMENT = 41;
ALTER TABLE store_kitconstruccion AUTO_INCREMENT = 81;
ALTER TABLE store_inventario AUTO_INCREMENT = 81;
ALTER TABLE store_imagenproducto AUTO_INCREMENT = 85;
ALTER TABLE control_pedido AUTO_INCREMENT = 41;
ALTER TABLE control_detallepedido AUTO_INCREMENT = 45;

-- =================================================================================================
-- 1. store_categoria (10 Categorías)
-- =================================================================================================

INSERT INTO store_categoria (id, nombre) VALUES
(1, 'Panel'),                       
(2, 'Kit Autoconstrucción'),        
(3, 'Muros Externos'),             
(4, 'Muros Internos'),              
(5, 'Cielo'),                      
(6, 'Piso'),                       
(7, 'Kit Vivienda Estándar'),       
(8, 'Kit Premium (Mayor 100m2)'),   
(9, 'Aislación Térmica'),           
(10, 'Herramientas de Montaje');    

-- =================================================================================================
-- 2. control_local (5 Locales)
-- =================================================================================================

INSERT INTO control_local (id, nombre, ubicacion, telefono) VALUES
(1, 'Santiago Centro - Retiro Express', 'Av. Libertador Bernardo O''Higgins 980, Santiago', '+56 9 1234 5678'),
(2, 'Bodega Maipu - Almacenamiento', 'Camino a Melipilla 15000, Maipú', '+56 9 8765 4321'),
(3, 'Sede Concepción Sur', 'Costanera 201, San Pedro de la Paz, Biobío', '+56 9 1122 3344'),
(4, 'Punto de Venta Puerto Montt', 'Avenida Presidente Ibáñez 600, Puerto Montt', '+56 9 5566 7788'),
(5, 'Viña del Mar - Showroom', 'Calle Arlegui 450, Viña del Mar, Valparaíso', '+56 9 9900 8877');

-- =================================================================================================
-- 3. store_panelsip (40 Paneles SIP)
-- =================================================================================================

-- ID 1-10: 16cm -> 160mm
INSERT INTO store_panelsip (id, nombre, precio, descripcion, tipo_obs, madera_union, espesor, largo, ancho) VALUES
(1, 'Panel SIP 160mm - Standard', 16500.0, 'Panel estructural de alto rendimiento para muros exteriores e interiores. Espesor 160mm.', 'OSB Estructural', 'Pino Radiata', 160.0, 2.44, 1.22),
(2, 'Panel SIP 160mm - Reforzado', 18990.0, 'Versión de alta densidad para zonas con carga estructural extra.', 'OSB Alta Densidad', 'Eucalipto', 160.0, 2.44, 1.22),
(3, 'Panel SIP 160mm - Ignífugo', 25500.0, 'Tratamiento retardante de fuego. Ideal para áreas de alto riesgo.', 'OSB Ignífugo', 'Pino Radiata', 160.0, 2.44, 1.22),
(4, 'Panel SIP 160mm - Losa', 21500.0, 'Diseñado para uso horizontal en pisos y losas.', 'OSB Estructural', 'Pino Radiata', 160.0, 3.00, 1.22),
(5, 'Panel SIP 160mm - Especial Muro Curvo', 28000.0, 'Diseño flexible para arquitectura moderna.', 'OSB Plywood', 'Pino Radiata', 160.0, 2.44, 1.22),
(6, 'Panel SIP 160mm - Acústico', 24000.0, 'Mejora de aislamiento de ruido para divisiones internas.', 'OSB Estructural', 'Pino Radiata', 160.0, 2.44, 1.22),
(7, 'Panel SIP 160mm - Premium', 32000.0, 'Terminación superficial de alta calidad para vista.', 'Fibrocemento', 'Pino Radiata', 160.0, 2.44, 1.22),
(8, 'Panel SIP 160mm - Grande (Stock)', 16990.0, 'Panel de mayor largo para menos uniones.', 'OSB Estructural', 'Pino Radiata', 160.0, 3.00, 1.50),
(9, 'Panel SIP 160mm - Pequeño', 15500.0, 'Tamaño para relleno y ajustes.', 'OSB Estructural', 'Pino Radiata', 160.0, 1.22, 1.22),
(10, 'Panel SIP 160mm - Techo', 19500.0, 'Diseñado para pendientes y cubiertas.', 'OSB Estructural', 'Pino Radiata', 160.0, 2.44, 1.22);

-- ID 11-20: 11cm -> 110mm
INSERT INTO store_panelsip (id, nombre, precio, descripcion, tipo_obs, madera_union, espesor, largo, ancho) VALUES
(11, 'Panel SIP 110mm - Estándar Divisorio', 12500.0, 'Ideal para muros internos y divisiones no estructurales.', 'OSB Estructural', 'Pino Radiata', 110.0, 2.44, 1.22),
(12, 'Panel SIP 110mm - Baño', 14800.0, 'Resistente a la humedad para zonas de servicio.', 'OSB con Barrera Humedad', 'Pino Radiata', 110.0, 2.44, 1.22),
(13, 'Panel SIP 110mm - Losa Ligera', 16200.0, 'Para aplicaciones ligeras de piso o entrepiso.', 'OSB Estructural', 'Pino Radiata', 110.0, 3.00, 1.22),
(14, 'Panel SIP 110mm - Relleno', 10500.0, 'Panel base para complemento de estructura.', 'OSB Estructural', 'Pino Radiata', 110.0, 2.44, 1.22),
(15, 'Panel SIP 110mm - Compacto', 13500.0, 'Aislamiento base para cubiertas de poco espesor.', 'OSB Estructural', 'Pino Radiata', 110.0, 2.44, 1.22),
(16, 'Panel SIP 110mm - Alto Rendimiento', 17000.0, 'Mejora en la densidad del núcleo de poliestireno.', 'OSB Alta Densidad', 'Pino Radiata', 110.0, 2.44, 1.22),
(17, 'Panel SIP 110mm - Industrial', 15900.0, 'Especial para cierres perimetrales de bodegas.', 'OSB Estructural', 'Pino Radiata', 110.0, 3.00, 1.50),
(18, 'Panel SIP 110mm - Económico', 11000.0, 'Opción más accesible para proyectos con presupuesto ajustado.', 'OSB Estándar', 'Pino Radiata', 110.0, 2.44, 1.22),
(19, 'Panel SIP 110mm - Rápido Montaje', 13000.0, 'Con pre-cortes de unión rápidos.', 'OSB Estructural', 'Pino Radiata', 110.0, 2.44, 1.22),
(20, 'Panel SIP 110mm - Reversible', 14500.0, 'Puede ser usado en ambos lados con la misma resistencia.', 'OSB Estructural', 'Pino Radiata', 110.0, 2.44, 1.22);

-- ID 21-40: 10cm -> 100mm, 15cm -> 150mm, 20cm -> 200mm (POR PEDIDO)
INSERT INTO store_panelsip (id, nombre, precio, descripcion, tipo_obs, madera_union, espesor, largo, ancho) VALUES
(21, 'Panel SIP 100mm - Pedido Estándar', 11000.0, 'Panel de fabricación por encargo, espesor 100mm.', 'OSB Estándar', 'Pino Radiata', 100.0, 2.44, 1.22),
(22, 'Panel SIP 150mm - Pedido Ignífugo', 23000.0, 'Panel de fabricación por encargo, espesor 150mm.', 'OSB Ignífugo', 'Pino Radiata', 150.0, 2.44, 1.22),
(23, 'Panel SIP 200mm - Pedido Extremo', 35000.0, 'Máximo aislamiento, fabricación por encargo, espesor 200mm.', 'OSB Estructural', 'Pino Radiata', 200.0, 3.00, 1.50),
(24, 'Panel SIP 100mm - Pedido Compacto', 10500.0, 'Panel de fabricación por encargo, espesor 100mm.', 'OSB Estándar', 'Pino Radiata', 100.0, 1.22, 1.22),
(25, 'Panel SIP 150mm - Pedido Techo Curvo', 27000.0, 'Diseño especial, fabricación por encargo, espesor 150mm.', 'OSB Plywood', 'Eucalipto', 150.0, 2.44, 1.22),
(26, 'Panel SIP 200mm - Pedido Losa', 38000.0, 'Para uso horizontal pesado, fabricación por encargo, espesor 200mm.', 'OSB Alta Densidad', 'Pino Radiata', 200.0, 3.00, 1.22),
(27, 'Panel SIP 100mm - Pedido Económico', 9500.0, 'Opción más básica por encargo, espesor 100mm.', 'OSB Estándar', 'Pino Radiata', 100.0, 2.44, 1.22),
(28, 'Panel SIP 150mm - Pedido Premium Vista', 30000.0, 'Terminación fibrocemento, fabricación por encargo, espesor 150mm.', 'Fibrocemento', 'Pino Radiata', 150.0, 2.44, 1.22),
(29, 'Panel SIP 200mm - Pedido Acústico', 42000.0, 'Alto rendimiento acústico, fabricación por encargo, espesor 200mm.', 'OSB Estructural', 'Pino Radiata', 200.0, 2.44, 1.22),
(30, 'Panel SIP 100mm - Pedido Kit Ahorro', 11500.0, 'Fabricación por encargo para kit específico, espesor 100mm.', 'OSB Estándar', 'Pino Radiata', 100.0, 3.00, 1.50),
(31, 'Panel SIP 150mm - Pedido Muro Exterior', 20000.0, 'Panel principal por encargo, espesor 150mm.', 'OSB Estructural', 'Pino Radiata', 150.0, 2.44, 1.22),
(32, 'Panel SIP 200mm - Pedido Reforzado', 45000.0, 'Máxima resistencia, fabricación por encargo, espesor 200mm.', 'OSB Alta Densidad', 'Eucalipto', 200.0, 2.44, 1.22),
(33, 'Panel SIP 100mm - Pedido Baño/Cocina', 13000.0, 'Tratamiento anti-humedad, fabricación por encargo, espesor 100mm.', 'OSB con Barrera Humedad', 'Pino Radiata', 100.0, 2.44, 1.22),
(34, 'Panel SIP 150mm - Pedido Gran Formato', 22500.0, 'Panel de gran formato por encargo, espesor 150mm.', 'OSB Estructural', 'Pino Radiata', 150.0, 3.00, 1.50),
(35, 'Panel SIP 200mm - Pedido Comercial', 40000.0, 'Para grandes proyectos comerciales, espesor 200mm.', 'OSB Estructural', 'Pino Radiata', 200.0, 2.44, 1.22),
(36, 'Panel SIP 100mm - Pedido Color Blanco', 14000.0, 'Color blanco interior, fabricación por encargo, espesor 100mm.', 'OSB Fibra Blanca', 'Pino Radiata', 100.0, 2.44, 1.22),
(37, 'Panel SIP 150mm - Pedido Industrial Alto', 26000.0, 'Panel para altura industrial, fabricación por encargo, espesor 150mm.', 'OSB Estructural', 'Pino Radiata', 150.0, 3.00, 1.22),
(38, 'Panel SIP 200mm - Pedido Losa Extrema', 48000.0, 'Máxima carga para losa, fabricación por encargo, espesor 200mm.', 'OSB Alta Densidad', 'Eucalipto', 200.0, 2.44, 1.22),
(39, 'Panel SIP 100mm - Pedido Quick Connect', 15000.0, 'Sistema de unión rápida, fabricación por encargo, espesor 100mm.', 'OSB Estructural', 'Pino Radiata', 100.0, 2.44, 1.22),
(40, 'Panel SIP 150mm - Pedido Bajo Presupuesto', 18000.0, 'Opción más simple por encargo, espesor 150mm.', 'OSB Estándar', 'Pino Radiata', 150.0, 2.44, 1.22);

-- =================================================================================================
-- 4. store_kitconstruccion (40 Kits)
-- =================================================================================================

-- ID 41-60: En Stock (Kits Pequeños y Estándar)
INSERT INTO store_kitconstruccion (id, nombre, precio, descripcion, m2, dormitorios, banos) VALUES
(41, 'Kit Cabaña Estándar - 30m2', 3200000.0, 'Kit de autoconstrucción de una cabaña pequeña, ideal para parcelas.', 30.0, 1, 1),
(42, 'Kit Cabaña Premium - 45m2', 4500000.0, 'Diseño moderno con grandes ventanales.', 45.0, 1, 1),
(43, 'Kit Vivienda Familiar - 60m2', 6800000.0, 'Vivienda modular de rápido montaje, 2 dormitorios.', 60.0, 2, 1),
(44, 'Kit Vivienda Clásica - 75m2', 7990000.0, 'Estilo tradicional con espacios bien definidos.', 75.0, 3, 1),
(45, 'Kit Duplex - 90m2', 9500000.0, 'Dos pisos, ideal para terrenos reducidos.', 90.0, 3, 2),
(46, 'Kit Estudio - 25m2', 2800000.0, 'Diseño tipo loft, perfecto para oficina o estudio.', 25.0, 0, 1),
(47, 'Kit Vivienda Económica - 55m2', 5900000.0, 'Opción accesible con 2 dormitorios.', 55.0, 2, 1),
(48, 'Kit Cabaña Rural - 40m2', 4100000.0, 'Diseño rústico, rápido de armar.', 40.0, 2, 1),
(49, 'Kit Vivienda Urbana - 80m2', 8800000.0, 'Diseño funcional, 3 dormitorios.', 80.0, 3, 2),
(50, 'Kit Vivienda Grande - 100m2', 11000000.0, 'Espaciosa casa familiar, 4 dormitorios, 2 baños.', 100.0, 4, 2),
(51, 'Kit Vivienda Básica - 65m2', 7100000.0, 'Modelo sencillo y eficiente.', 65.0, 2, 1),
(52, 'Kit Vacacional - 50m2', 5200000.0, 'Ideal para playa o montaña.', 50.0, 2, 1),
(53, 'Kit Casa Moderna - 85m2', 9200000.0, 'Fachada minimalista y techos planos.', 85.0, 3, 2),
(54, 'Kit Vivienda 2 Baños - 70m2', 7500000.0, 'Especialmente diseñado para la comodidad familiar.', 70.0, 3, 2),
(55, 'Kit Oficina en Casa - 35m2', 3800000.0, 'Espacio de trabajo independiente.', 35.0, 1, 1),
(56, 'Kit Chalet Montaña - 95m2', 10500000.0, 'Diseño robusto para zonas frías.', 95.0, 3, 2),
(57, 'Kit Mini-Depto - 20m2', 2500000.0, 'La solución más compacta y económica.', 20.0, 0, 1),
(58, 'Kit Familiar Lujo - 110m2', 12500000.0, 'Acabados de primera línea.', 110.0, 4, 3),
(59, 'Kit Vivienda Rápida - 72m2', 7700000.0, 'Kit enfocado en la velocidad de montaje.', 72.0, 3, 1),
(60, 'Kit Básico 4 Dormitorios - 88m2', 9100000.0, 'Optimización de espacio para familias numerosas.', 88.0, 4, 1);

-- ID 61-80: Por Pedido (Kits Grandes y Especiales)
INSERT INTO store_kitconstruccion (id, nombre, precio, descripcion, m2, dormitorios, banos) VALUES
(61, 'Kit Mansión SIP - 150m2 (Pedido)', 16000000.0, 'El kit más grande y espacioso, requiere fabricación.', 150.0, 5, 3),
(62, 'Kit Diseño Arquitecto - 120m2 (Pedido)', 14500000.0, 'Diseño exclusivo, con planos a medida.', 120.0, 4, 2),
(63, 'Kit Casa Flotante - 80m2 (Pedido)', 18000000.0, 'Diseño especial para uso en plataformas flotantes.', 80.0, 2, 1),
(64, 'Kit Taller Industrial - 200m2 (Pedido)', 25000000.0, 'Gran volumen para uso comercial o taller.', 200.0, 0, 1),
(65, 'Kit Lujo 3 Baños - 130m2 (Pedido)', 15500000.0, 'Máximo confort y múltiples baños.', 130.0, 4, 3),
(66, 'Kit Modelo Austral - 115m2 (Pedido)', 13800000.0, 'Diseño con doble aislamiento para el sur de Chile.', 115.0, 3, 2),
(67, 'Kit Familiar XXL - 140m2 (Pedido)', 17500000.0, 'Máximo espacio interior y exterior.', 140.0, 5, 3),
(68, 'Kit Vivienda Social - 50m2 (Pedido)', 4900000.0, 'Modelo optimizado para proyectos de vivienda social.', 50.0, 2, 1),
(69, 'Kit Vivienda con Terraza - 98m2 (Pedido)', 11500000.0, 'Incluye materiales para amplia terraza techada.', 98.0, 3, 2),
(70, 'Kit Granja Familiar - 105m2 (Pedido)', 12800000.0, 'Diseño campestre con grandes espacios de guardado.', 105.0, 3, 2),
(71, 'Kit Casa de Invitados - 48m2 (Pedido)', 4700000.0, 'Cabaña independiente para visitas.', 48.0, 2, 1),
(72, 'Kit Vivienda Sustentable - 95m2 (Pedido)', 14000000.0, 'Materiales eco-amigables y diseños de eficiencia energética.', 95.0, 3, 2),
(73, 'Kit de Montaje Rápido XL - 125m2 (Pedido)', 13500000.0, 'Diseñado para ser levantado en tiempo récord.', 125.0, 4, 2),
(74, 'Kit Vivienda con Altillo - 78m2 (Pedido)', 8900000.0, 'Aprovechamiento de espacio con un altillo funcional.', 78.0, 3, 1),
(75, 'Kit Casa Playa - 68m2 (Pedido)', 7800000.0, 'Especialmente resistente a la salinidad.', 68.0, 2, 1),
(76, 'Kit Cabaña Doble Altura - 55m2 (Pedido)', 6200000.0, 'Techo a doble altura para mayor sensación de amplitud.', 55.0, 1, 1),
(77, 'Kit Residencial Premium - 160m2 (Pedido)', 18500000.0, 'Máximo lujo y personalización.', 160.0, 5, 4),
(78, 'Kit Oficina Modular - 40m2 (Pedido)', 4300000.0, 'Unidades modulares para combinar.', 40.0, 1, 1),
(79, 'Kit Vivienda Térmica Extrema - 118m2 (Pedido)', 14900000.0, 'Diseñado para los climas más exigentes.', 118.0, 4, 2),
(80, 'Kit Personalizable Base - 70m2 (Pedido)', 8000000.0, 'Base para que el cliente adapte a su gusto.', 70.0, 2, 1);

-- =================================================================================================
-- 5. store_inventario (80 Inventarios - 40 Paneles + 40 Kits)
-- =================================================================================================

-- PanelSIP (IDs 1-40)
-- Stock (IDs 1-20): 50 unidades disponibles
INSERT INTO store_inventario (id, disponible, reservado, modo_stock, content_type_id, object_id)
SELECT id, 50, 0, 'stock', 12, id FROM store_panelsip WHERE id <= 20;
-- Pedido (IDs 21-40): 0 unidades disponibles
INSERT INTO store_inventario (id, disponible, reservado, modo_stock, content_type_id, object_id)
SELECT id + 40, 0, 0, 'pedido', 12, id FROM store_panelsip WHERE id BETWEEN 21 AND 40;

-- KitConstruccion (IDs 41-80)
-- Stock (IDs 41-60): 10 unidades disponibles
INSERT INTO store_inventario (id, disponible, reservado, modo_stock, content_type_id, object_id)
SELECT id + 40, 10, 0, 'stock', 10, id FROM store_kitconstruccion WHERE id BETWEEN 41 AND 60;
-- Pedido (IDs 61-80): 0 unidades disponibles
INSERT INTO store_inventario (id, disponible, reservado, modo_stock, content_type_id, object_id)
SELECT id + 80, 0, 0, 'pedido', 10, id FROM store_kitconstruccion WHERE id BETWEEN 61 AND 80;


-- =================================================================================================
-- 6. store_imagenproducto (80 Imágenes)
-- =================================================================================================

-- Paneles SIP
INSERT INTO store_imagenproducto (id, imagen, content_type_id, object_id)
SELECT id, 'panel.png', 12, id FROM store_panelsip;

-- Kits de Construcción
-- Se ajusta el ID base para seguir la secuencia (1-40 para Paneles, 41-80 para Kits)
INSERT INTO store_imagenproducto (id, imagen, content_type_id, object_id)
SELECT id+40, 'kit.png', 10, id FROM store_kitconstruccion;

-- =================================================================================================
-- 7. store_panelsip_categorias (Asignación de Categorías a Paneles)
-- =================================================================================================

INSERT INTO store_panelsip_categorias (panelsip_id, categoria_id) VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
(11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1),
(21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 1), (27, 1), (28, 1), (29, 1), (30, 1),
(31, 1), (32, 1), (33, 1), (34, 1), (35, 1), (36, 1), (37, 1), (38, 1), (39, 1), (40, 1),

(1, 3), (1, 9),(2, 3), (2, 9),(3, 3), (3, 9),(4, 6), (4, 9),(5, 3), (5, 4),(6, 4), (6, 9),(7, 3), (7, 4),(8, 3), (8, 6),(9, 4), (9, 10),(10, 5), (10, 9),

(11, 4), (11, 9),(12, 4), (12, 9),(13, 6), (13, 9),
(14, 4), (14, 10),(15, 5), (15, 9),(16, 3), (16, 9),(17, 3), (17, 9),(18, 4), (18, 9),(19, 3), (19, 10),(20, 3), (20, 4),

(21, 3), (21, 4),(22, 3), (22, 9),
(23, 3), (23, 9),(24, 4), (24, 10),(25, 5), (25, 9),(26, 6), (26, 9),(27, 3), (27, 4),(28, 3), (28, 4),(29, 4), (29, 9),(30, 4), (30, 10),

(31, 3), (31, 9),(32, 3), (32, 9),(33, 4), (33, 9),(34, 3), (34, 6),(35, 3), (35, 4),(36, 4), (36, 9),(37, 5), (37, 3),(38, 6), (38, 9),(39, 3), (39, 10),(40, 3), (40, 9);

-- =================================================================================================
-- 8. store_kitconstruccion_categorias (Asignación de Categorías a Kits)
-- =================================================================================================

INSERT INTO store_kitconstruccion_categorias (kitconstruccion_id, categoria_id) VALUES
(41, 2), (42, 2), (43, 2), (44, 2), (45, 2), (46, 2), (47, 2), (48, 2), (49, 2), (50, 2),
(51, 2), (52, 2), (53, 2), (54, 2), (55, 2), (56, 2), (57, 2), (58, 2), (59, 2), (60, 2),
(61, 2), (62, 2), (63, 2), (64, 2), (65, 2), (66, 2), (67, 2), (68, 2), (69, 2), (70, 2),
(71, 2), (72, 2), (73, 2), (74, 2), (75, 2), (76, 2), (77, 2), (78, 2), (79, 2), (80, 2),

(41, 7), (41, 9),(42, 7), (42, 10),(43, 8), (43, 9),(44, 8), (44, 10),(45, 7), (45, 9),(46, 7), (46, 10),(47, 8), (47, 9),(48, 7), (48, 9),(49, 8), (49, 9),(50, 7), (50, 10),

(51, 8), (51, 9), (51, 10),(52, 7), (52, 9),(53, 8), (53, 9),(54, 7), (54, 10),(55, 8), (55, 9),(56, 8), (56, 10),(57, 7), (57, 9),(58, 8), (58, 9),(59, 7), (59, 10),(60, 8), (60, 9),

(61, 7), (61, 9),(62, 8), (62, 9),(63, 7), (63, 10),(64, 8), (64, 9),(65, 7), (65, 9),(66, 8), (66, 10),(67, 7), (67, 9),(68, 8), (68, 9),(69, 7), (69, 10),(70, 8), (70, 9),

(71, 7), (71, 9),(72, 8), (72, 9),(73, 7), (73, 10),(74, 8), (74, 9),(75, 7), (75, 9),(76, 8), (76, 10),(77, 7), (77, 9),(78, 8), (78, 9),(79, 7), (79, 10),(80, 8), (80, 9);

-- =================================================================================================
-- 9. control_pedido (40 Pedidos Variados)
-- =================================================================================================

INSERT INTO control_pedido (id, local_id, nombre_local, comprador, rut_cli, correo_cli, celular_cli, ubicacion_cli, fecha_pedido, fecha_retiro, estado, monto_total, metodo_pago) VALUES
-- Pedidos Completados (2025-09)
(1, 1, 'Santiago Centro - Retiro Express', 'Javier Ignacio Soto', '18.123.456-7', 'javier.soto@mail.cl', '+56911223344', 'Retiro en Local 1', '2025-09-15 10:30:00', '2025-09-20 15:00:00', 'completado', 0, 'pago_web'),
(2, 3, 'Sede Concepción Sur', 'Carolina Andrea Rojas', '17.876.543-K', 'caro.rojas@mail.cl', '+56998765432', 'Calle Las Hortensias 150, Concepción', '2025-09-16 14:45:00', '2025-09-22 10:00:00', 'completado', 0, 'pago_web'),
(3, 5, 'Viña del Mar - Showroom', 'Marco Antonio Vidal', '16.555.333-2', 'marco.vidal@mail.cl', '+56922334455', 'Av. Central 990, Viña del Mar', '2025-09-17 09:00:00', '2025-09-21 11:30:00', 'completado', 0, 'pago_tienda'),
(4, 2, 'Bodega Maipu - Almacenamiento', 'Fernanda Paz Orellana', '19.444.222-1', 'fernanda.o@mail.cl', '+56933445566', 'Calle El Sol 123, Maipú', '2025-09-18 16:15:00', '2025-09-25 09:45:00', 'completado', 0, 'pago_web'),
(5, 4, 'Punto de Venta Puerto Montt', 'Ricardo Esteban Muñoz', '15.987.654-2', 'ricardo.m@mail.cl', '+56944556677', 'Pasaje Austral 500, Puerto Montt', '2025-09-19 11:50:00', '2025-09-26 14:00:00', 'completado', 0, 'pago_web'),
(6, 1, 'Santiago Centro - Retiro Express', 'Susana Inés Pérez', '14.321.098-9', 'susanaperez@mail.cl', '+56955667788', 'Retiro en Local 1', '2025-09-20 12:00:00', '2025-09-27 10:00:00', 'completado', 0, 'pago_tienda'),
(7, 3, 'Sede Concepción Sur', 'Daniel Alejandro Castro', '18.777.666-4', 'danielcastro@mail.cl', '+56966778899', 'Av. Los Robles 10, Talcahuano', '2025-09-21 15:30:00', '2025-09-28 15:00:00', 'completado', 0, 'pago_web'),
(8, 5, 'Viña del Mar - Showroom', 'María José Lagos', '17.111.999-0', 'marialagos@mail.cl', '+56977889900', 'Calle Libertad 300, Reñaca', '2025-09-22 17:00:00', '2025-09-29 12:00:00', 'completado', 0, 'pago_web'),
(9, 2, 'Bodega Maipu - Almacenamiento', 'Patricio Andrés Díaz', '16.000.111-5', 'patricio.diaz@mail.cl', '+56988990011', 'Calle Sur 50, Maipú', '2025-09-23 08:30:00', '2025-09-30 08:30:00', 'completado', 0, 'pago_tienda'),
(10, 4, 'Punto de Venta Puerto Montt', 'Andrea Soledad Gómez', '19.222.888-3', 'andrea.gomez@mail.cl', '+56990011223', 'Los Alerces 1200, Puerto Varas', '2025-09-24 10:45:00', '2025-10-01 10:45:00', 'completado', 0, 'pago_web'),
-- Pedidos Cancelados
(11, 1, 'Santiago Centro - Retiro Express', 'Roberto Carlos Soto', '18.123.456-7', 'roberto.soto@mail.cl', '+56911223344', 'Retiro en Local 1', '2025-10-01 10:30:00', NULL, 'cancelado', 0, 'pago_web'),
(12, 3, 'Sede Concepción Sur', 'Javiera Ignacia Rojas', '17.876.543-K', 'javiera.rojas@mail.cl', '+56998765432', 'Calle Las Hortensias 150, Concepción', '2025-10-02 14:45:00', NULL, 'cancelado', 0, 'pago_web'),
(13, 5, 'Viña del Mar - Showroom', 'Martín Andrés Vidal', '16.555.333-2', 'martin.vidal@mail.cl', '+56922334455', 'Av. Central 990, Viña del Mar', '2025-10-03 09:00:00', NULL, 'cancelado', 0, 'pago_tienda'),
(14, 2, 'Bodega Maipu - Almacenamiento', 'Juan Pablo Orellana', '19.444.222-1', 'juanpablo.o@mail.cl', '+56933445566', 'Calle El Sol 123, Maipú', '2025-10-04 16:15:00', NULL, 'cancelado', 0, 'pago_web'),
(15, 4, 'Punto de Venta Puerto Montt', 'Sebastián Esteban Muñoz', '15.987.654-2', 'sebastian.m@mail.cl', '+56944556677', 'Pasaje Austral 500, Puerto Montt', '2025-10-05 11:50:00', NULL, 'cancelado', 0, 'pago_web'),
-- Pedidos En Proceso (2025-10)
(16, 1, 'Santiago Centro - Retiro Express', 'Catalina Inés Pérez', '14.321.098-9', 'catalinaperez@mail.cl', '+56955667788', 'Retiro en Local 1', '2025-10-06 12:00:00', NULL, 'en_proceso', 0, 'pago_tienda'),
(17, 3, 'Sede Concepción Sur', 'Benjamín Alejandro Castro', '18.777.666-4', 'benjamin.castro@mail.cl', '+56966778899', 'Av. Los Robles 10, Talcahuano', '2025-10-07 15:30:00', NULL, 'en_proceso', 0, 'pago_web'),
(18, 5, 'Viña del Mar - Showroom', 'Francisca José Lagos', '17.111.999-0', 'francisca.lagos@mail.cl', '+56977889900', 'Calle Libertad 300, Reñaca', '2025-10-08 17:00:00', NULL, 'en_proceso', 0, 'pago_web'),
(19, 2, 'Bodega Maipu - Almacenamiento', 'Diego Andrés Díaz', '16.000.111-5', 'diego.diaz@mail.cl', '+56988990011', 'Calle Sur 50, Maipú', '2025-10-09 08:30:00', NULL, 'en_proceso', 0, 'pago_tienda'),
(20, 4, 'Punto de Venta Puerto Montt', 'Camila Soledad Gómez', '19.222.888-3', 'camila.gomez@mail.cl', '+56990011223', 'Los Alerces 1200, Puerto Varas', '2025-10-10 10:45:00', NULL, 'en_proceso', 0, 'pago_web'),
-- Pedidos Pendientes (2025-10-18 - Hoy)
(21, 1, 'Santiago Centro - Retiro Express', 'Alfonso Matías Pérez', '14.567.890-1', 'alfonso.perez@mail.cl', '+56910203040', 'Retiro en Local 1', '2025-10-18 19:24:00', NULL, 'pendiente', 0, 'pago_web'),
(22, 3, 'Sede Concepción Sur', 'Gabriela Elena Torres', '17.010.203-4', 'gabriela.torres@mail.cl', '+56920304050', 'Av. Alemania 50, Concepción', '2025-10-18 19:26:00', NULL, 'pendiente', 0, 'pago_tienda'),
(23, 5, 'Viña del Mar - Showroom', 'Joaquín Andrés Ruiz', '16.987.654-3', 'joaquin.ruiz@mail.cl', '+56930405060', 'Calle Valparaíso 100, Viña del Mar', '2025-10-18 19:28:00', NULL, 'pendiente', 0, 'pago_web'),
(24, 2, 'Bodega Maipu - Almacenamiento', 'Paula Constanza Soto', '18.765.432-1', 'paula.soto@mail.cl', '+56940506070', 'Lote 15, Camino a Pajaritos, Maipú', '2025-10-18 19:30:00', NULL, 'pendiente', 0, 'pago_tienda'),
(25, 4, 'Punto de Venta Puerto Montt', 'Vicente Nicolás Tapia', '19.123.000-0', 'vicente.tapia@mail.cl', '+56950607080', 'Ruta 5 Sur, Km 1020, Puerto Montt', '2025-10-18 19:32:00', NULL, 'pendiente', 0, 'pago_web'),
(26, 1, 'Santiago Centro - Retiro Express', 'Beatriz Isabel Leiva', '15.678.901-2', 'beatriz.leiva@mail.cl', '+56960708090', 'Retiro en Local 1', '2025-10-18 19:34:00', NULL, 'pendiente', 0, 'pago_web'),
(27, 3, 'Sede Concepción Sur', 'Carlos Rodrigo Fuentes', '16.543.210-9', 'carlos.fuentes@mail.cl', '+56970809000', 'Barrio Universitario, Concepción', '2025-10-18 19:36:00', NULL, 'pendiente', 0, 'pago_tienda'),
(28, 5, 'Viña del Mar - Showroom', 'Elena Valentina Salas', '17.432.109-8', 'elena.salas@mail.cl', '+56980900010', 'Avenida San Martín 800, Viña', '2025-10-18 19:38:00', NULL, 'pendiente', 0, 'pago_web'),
(29, 2, 'Bodega Maipu - Almacenamiento', 'Felipe Ignacio Araya', '18.321.098-7', 'felipe.araya@mail.cl', '+56990001020', 'Sector Lo Espejo, Maipú', '2025-10-18 19:40:00', NULL, 'pendiente', 0, 'pago_tienda'),
(30, 4, 'Punto de Venta Puerto Montt', 'Gloria Patricia Hermosilla', '19.210.987-6', 'gloria.h@mail.cl', '+56900010203', 'Sector Bosque Nativo, Puerto Varas', '2025-10-18 19:42:00', NULL, 'pendiente', 0, 'pago_web'),
-- Pedidos Mixtos (Proceso, Pendiente, Cancelado, Completado)
(31, 1, 'Santiago Centro - Retiro Express', 'Héctor Javier Ponce', '18.123.999-7', 'hector.ponce@mail.cl', '+56911122334', 'Retiro en Local 1', '2025-08-15 10:30:00', NULL, 'en_proceso', 0, 'pago_web'),
(32, 3, 'Sede Concepción Sur', 'Irene Elisa Lagos', '17.876.888-K', 'irene.lagos@mail.cl', '+56998877665', 'Calle La Paz 300, Concepción', '2025-08-16 14:45:00', NULL, 'pendiente', 0, 'pago_tienda'),
(33, 5, 'Viña del Mar - Showroom', 'Jorge Alberto Muñoz', '16.555.777-2', 'jorge.munoz@mail.cl', '+56922233445', 'Av. Borgoño 1500, Reñaca', '2025-08-17 09:00:00', NULL, 'cancelado', 0, 'pago_web'),
(34, 2, 'Bodega Maipu - Almacenamiento', 'Karen Daniela Rojas', '19.444.666-1', 'karen.rojas@mail.cl', '+56933344556', 'Villa Los Aromos, Maipú', '2025-08-18 16:15:00', '2025-08-25 09:45:00', 'completado', 0, 'pago_tienda'),
(35, 4, 'Punto de Venta Puerto Montt', 'Luis Fernando Sáez', '15.987.555-2', 'luis.saez@mail.cl', '+56944455667', 'Chinquihue Alto, Puerto Montt', '2025-08-19 11:50:00', NULL, 'pendiente', 0, 'pago_web'),
(36, 1, 'Santiago Centro - Retiro Express', 'Macarena Ignacia Soto', '14.321.444-9', 'macarena.soto@mail.cl', '+56955566778', 'Retiro en Local 1', '2025-08-20 12:00:00', NULL, 'en_proceso', 0, 'pago_web'),
(37, 3, 'Sede Concepción Sur', 'Nicolás Andrés Díaz', '18.777.333-4', 'nicolas.diaz@mail.cl', '+56966677889', 'Los Carrera 123, Concepción', '2025-08-21 15:30:00', NULL, 'pendiente', 0, 'pago_web'),
(38, 5, 'Viña del Mar - Showroom', 'Octavio Jesús Paredes', '17.111.222-0', 'octavio.paredes@mail.cl', '+56977788990', 'Avenida Concón 400, Concón', '2025-08-22 17:00:00', '2025-08-29 12:00:00', 'completado', 0, 'pago_tienda'),
(39, 2, 'Bodega Maipu - Almacenamiento', 'Pamela Soledad Rojas', '16.000.123-5', 'pamela.rojas@mail.cl', '+56988899001', 'Calle Poniente 10, Maipú', '2025-08-23 08:30:00', NULL, 'cancelado', 0, 'pago_web'),
(40, 4, 'Punto de Venta Puerto Montt', 'Quirina Antonia Castro', '19.222.098-3', 'quirina.castro@mail.cl', '+56999001122', 'Sector Pelluco, Puerto Montt', '2025-08-24 10:45:00', '2025-08-31 10:45:00', 'completado', 0, 'pago_web');


-- =================================================================================================
-- 10. control_detallepedido (Detalles de Pedidos)
-- =================================================================================================

INSERT INTO control_detallepedido (id, pedido_id, content_type_id, object_id, nombre_producto, precio_unitario, cantidad, subtotal) VALUES
(1, 1, 10, 43, 'Kit Vivienda Familiar - 60m2', 6800000.00, 1, 0.00),
(2, 2, 12, 1, 'Panel SIP 160mm - Standard', 16500.00, 10, 0.00),
(3, 2, 12, 11, 'Panel SIP 110mm - Estándar Divisorio', 12500.00, 5, 0.00),
(4, 3, 10, 47, 'Kit Vivienda Económica - 55m2', 5900000.00, 1, 0.00),
(5, 3, 12, 8, 'Panel SIP 160mm - Grande (Stock)', 16990.00, 2, 0.00),
(6, 3, 12, 21, 'Panel SIP 100mm - Pedido Estándar', 11000.00, 1, 0.00),
(7, 4, 12, 30, 'Panel SIP 100mm - Pedido Kit Ahorro', 11500.00, 15, 0.00),
(8, 5, 10, 61, 'Kit Mansión SIP - 150m2 (Pedido)', 16000000.00, 1, 0.00),
(9, 6, 12, 2, 'Panel SIP 160mm - Reforzado', 18990.00, 8, 0.00),
(10, 7, 10, 53, 'Kit Casa Moderna - 85m2', 9200000.00, 1, 0.00),
(11, 8, 12, 4, 'Panel SIP 160mm - Losa', 21500.00, 20, 0.00),
(12, 8, 12, 23, 'Panel SIP 200mm - Pedido Extremo', 35000.00, 4, 0.00),
(13, 9, 10, 50, 'Kit Vivienda Grande - 100m2', 11000000.00, 1, 0.00),
(14, 10, 12, 16, 'Panel SIP 110mm - Alto Rendimiento', 17000.00, 12, 0.00),
(15, 11, 12, 3, 'Panel SIP 160mm - Ignífugo', 25500.00, 5, 0.00),
(16, 12, 10, 55, 'Kit Oficina en Casa - 35m2', 3800000.00, 1, 0.00),
(17, 13, 12, 22, 'Panel SIP 150mm - Pedido Ignífugo', 23000.00, 1, 0.00),
(18, 14, 10, 64, 'Kit Taller Industrial - 200m2 (Pedido)', 25000000.00, 1, 0.00),
(19, 15, 12, 10, 'Panel SIP 160mm - Techo', 19500.00, 10, 0.00),
(20, 16, 12, 18, 'Panel SIP 110mm - Económico', 11000.00, 15, 0.00),
(21, 17, 10, 52, 'Kit Vacacional - 50m2', 5200000.00, 1, 0.00),
(22, 18, 12, 24, 'Panel SIP 100mm - Pedido Compacto', 10500.00, 5, 0.00),
(23, 19, 10, 59, 'Kit Vivienda Rápida - 72m2', 7700000.00, 1, 0.00),
(24, 20, 12, 25, 'Panel SIP 150mm - Pedido Techo Curvo', 27000.00, 10, 0.00),
(25, 21, 12, 19, 'Panel SIP 110mm - Rápido Montaje', 13000.00, 20, 0.00),
(26, 22, 10, 41, 'Kit Cabaña Estándar - 30m2', 3200000.00, 1, 0.00),
(27, 23, 12, 26, 'Panel SIP 200mm - Pedido Losa', 38000.00, 5, 0.00),
(28, 24, 10, 60, 'Kit Básico 4 Dormitorios - 88m2', 9100000.00, 1, 0.00),
(29, 25, 12, 7, 'Panel SIP 160mm - Premium', 32000.00, 3, 0.00),
(30, 26, 12, 27, 'Panel SIP 100mm - Pedido Económico', 9500.00, 10, 0.00),
(31, 27, 10, 45, 'Kit Duplex - 90m2', 9500000.00, 1, 0.00),
(32, 28, 12, 31, 'Panel SIP 150mm - Pedido Muro Exterior', 20000.00, 5, 0.00),
(33, 29, 10, 58, 'Kit Familiar Lujo - 110m2', 12500000.00, 1, 0.00),
(34, 30, 12, 32, 'Panel SIP 200mm - Pedido Reforzado', 45000.00, 2, 0.00),
(35, 31, 12, 15, 'Panel SIP 110mm - Compacto', 13500.00, 10, 0.00),
(36, 32, 10, 42, 'Kit Cabaña Premium - 45m2', 4500000.00, 1, 0.00),
(37, 33, 12, 33, 'Panel SIP 100mm - Pedido Baño/Cocina', 13000.00, 5, 0.00),
(38, 34, 10, 49, 'Kit Vivienda Urbana - 80m2', 8800000.00, 1, 0.00),
(39, 35, 12, 20, 'Panel SIP 110mm - Reversible', 14500.00, 12, 0.00),
(40, 36, 10, 62, 'Kit Diseño Arquitecto - 120m2 (Pedido)', 14500000.00, 1, 0.00),
(41, 37, 12, 6, 'Panel SIP 160mm - Acústico', 24000.00, 5, 0.00),
(42, 38, 10, 44, 'Kit Vivienda Clásica - 75m2', 7990000.00, 1, 0.00),
(43, 39, 12, 34, 'Panel SIP 150mm - Pedido Gran Formato', 22500.00, 10, 0.00),
(44, 40, 10, 56, 'Kit Chalet Montaña - 95m2', 10500000.00, 1, 0.00);

-- =================================================================================================
-- 11. CÁLCULOS Y ACTUALIZACIONES FINALES (Corregido el error 1093)
-- =================================================================================================

-- 11.1. Calcular Subtotales en DetallePedido
UPDATE control_detallepedido
SET subtotal = precio_unitario * cantidad
WHERE subtotal = 0.0;

-- 11.2. Acumular Reservas en Inventario (Solo para pedidos NO CANCELADOS) - CORRECCIÓN DEL ERROR 1093
UPDATE store_inventario si
JOIN (
    -- Subconsulta anidada para aislar la tabla temporal 'reservas_calculadas' y evitar el Error 1093
    SELECT
        reservas_calculadas.content_type_id,
        reservas_calculadas.object_id,
        reservas_calculadas.total_reservado
    FROM (
        SELECT cdp.content_type_id, cdp.object_id, SUM(cdp.cantidad) AS total_reservado
        FROM control_detallepedido cdp
        JOIN control_pedido cp ON cdp.pedido_id = cp.id
        WHERE cp.estado != 'cancelado'
        GROUP BY cdp.content_type_id, cdp.object_id
    ) AS reservas_calculadas
) AS reservas ON si.content_type_id = reservas.content_type_id AND si.object_id = reservas.object_id
SET si.reservado = si.reservado + reservas.total_reservado;


-- 11.3. Actualizar Stock Disponible (Disponible = Inicial - Reservado)
UPDATE store_inventario
SET disponible = GREATEST(disponible - reservado, 0)
WHERE modo_stock = 'stock';

-- 11.4. Actualizar Monto Total en Pedidos (Pedidos NO cancelados)
UPDATE control_pedido cp
JOIN (
    SELECT pedido_id, SUM(subtotal) AS total_pedido
    FROM control_detallepedido
    GROUP BY pedido_id
) AS totales ON cp.id = totales.pedido_id
SET cp.monto_total = totales.total_pedido
WHERE cp.estado != 'cancelado';

-- 11.5. Asegurar que los pedidos cancelados tengan monto_total (o el monto al cancelar)
UPDATE control_pedido cp
JOIN (
    SELECT pedido_id, SUM(subtotal) AS total_pedido
    FROM control_detallepedido
    GROUP BY pedido_id
) AS totales ON cp.id = totales.pedido_id
SET cp.monto_total = totales.total_pedido
WHERE cp.estado = 'cancelado';