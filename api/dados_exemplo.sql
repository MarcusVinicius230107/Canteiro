-- Carga opcional de dados de exemplo (rode depois do schema.sql)
INSERT INTO plantas (nome_popular, nome_cientifico, categoria, luminosidade, preco, estoque, data_entrada, pet_seguro, observacoes) VALUES
('Samambaia',           'Nephrolepis exaltata',    'interior',  'meia_sombra',  39.90, 12, '2026-10-20', TRUE,  'Gosta de umidade'),
('Jiboia',              'Epipremnum aureum',       'interior',  'meia_sombra',  29.90, 25, '2026-10-22', FALSE, 'Tóxica para pets'),
('Espada-de-são-jorge', 'Dracaena trifasciata',    'interior',  'sombra',       45.00,  8, '2026-10-25', FALSE, NULL),
('Echeveria',           'Echeveria elegans',       'suculenta', 'sol_pleno',    18.50, 40, '2026-11-01', TRUE,  'Regar a cada 10 dias'),
('Lavanda',             'Lavandula angustifolia',  'aromatica', 'sol_pleno',    22.00, 15, '2026-11-02', TRUE,  NULL),
('Manjericão',          'Ocimum basilicum',        'aromatica', 'sol_pleno',    12.00, 30, '2026-11-03', TRUE,  'Ótimo para cozinha'),
('Limoeiro',            'Citrus limon',            'frutifera', 'sol_pleno',   120.00,  4, '2026-10-15', TRUE,  'Muda com 60 cm'),
('Hortênsia',           'Hydrangea macrophylla',   'jardim',    'meia_sombra',  55.00,  9, '2026-10-28', FALSE, NULL);
