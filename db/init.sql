-- ============================================
-- NestShop : initialisation de la base
-- ============================================

-- Table des produits
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    price       INTEGER NOT NULL CHECK (price > 0),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- Produits de départ (artisanat sénégalais, prix en FCFA)
INSERT INTO products (name, description, price, stock) VALUES
    ('Panier en osier tressé', 'Panier tressé à la main, idéal pour le marché', 15000, 20),
    ('Boubou brodé', 'Boubou en bazin avec broderies traditionnelles', 35000, 10),
    ('Sac en wax', 'Sac à main en tissu wax coloré', 12000, 25),
    ('Sandales en cuir', 'Sandales artisanales en cuir de Ngaye Mékhé', 18000, 15),
    ('Collier en perles', 'Collier fait main en perles colorées', 7500, 30),
    ('Statuette en bois', 'Statuette sculptée à la main en bois d''ébène', 25000, 8)
ON CONFLICT (name) DO NOTHING;


-- Table des commandes
CREATE TABLE IF NOT EXISTS orders (
    id            SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    product_id    INTEGER NOT NULL REFERENCES products(id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    total         INTEGER NOT NULL CHECK (total > 0),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);