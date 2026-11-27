import app.main as main_module


# ---------- Santé ----------

def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_base_indisponible(client, monkeypatch):
    class EngineCasse:
        def connect(self):
            raise RuntimeError("base indisponible")

    monkeypatch.setattr(main_module, "engine", EngineCasse())
    response = client.get("/health")
    assert response.status_code == 503


# ---------- Produits ----------

def test_liste_produits(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------- Commandes ----------

def test_commande_valide(client):
    response = client.post(
        "/api/orders",
        json={"customer_name": "Awa Diop", "product_id": 1, "quantity": 2},
    )
    assert response.status_code == 201
    assert response.json()["total"] == 30000

    produits = client.get("/api/products").json()
    assert produits[0]["stock"] == 8


def test_commande_produit_introuvable(client):
    response = client.post(
        "/api/orders",
        json={"customer_name": "Awa Diop", "product_id": 999, "quantity": 1},
    )
    assert response.status_code == 404


def test_commande_stock_insuffisant(client):
    response = client.post(
        "/api/orders",
        json={"customer_name": "Awa Diop", "product_id": 2, "quantity": 5},
    )
    assert response.status_code == 400


def test_commande_quantite_invalide(client):
    response = client.post(
        "/api/orders",
        json={"customer_name": "Awa Diop", "product_id": 1, "quantity": 0},
    )
    assert response.status_code == 422


def test_total_impose_par_client_ignore(client):
    response = client.post(
        "/api/orders",
        json={"customer_name": "Pirate", "product_id": 1, "quantity": 1, "total": 1},
    )
    assert response.status_code == 201
    assert response.json()["total"] == 15000


def test_liste_commandes_plus_recente_en_premier(client):
    client.post("/api/orders", json={"customer_name": "Awa", "product_id": 1, "quantity": 1})
    client.post("/api/orders", json={"customer_name": "Fatou", "product_id": 1, "quantity": 1})

    commandes = client.get("/api/orders").json()
    assert len(commandes) == 2
    assert commandes[0]["customer_name"] == "Fatou"