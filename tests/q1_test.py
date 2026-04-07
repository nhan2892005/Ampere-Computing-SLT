class TestQ1:
    def test_returns_200(self, client):
        assert client.get("/q1").status_code == 200

    def test_shows_all_tables(self, client):
        r = client.get("/q1")
        for name in [b"supplier", b"product", b"warehouse", b"consumption"]:
            assert name in r.data

    def test_shows_supplier_data(self, client):
        r = client.get("/q1")
        assert b"North" in r.data
        assert b"Central" in r.data
        assert b"South" in r.data

    def test_shows_product_data(self, client):
        r = client.get("/q1")
        assert b"APW" in r.data
        assert b"VNM" in r.data

    def test_shows_warehouse_data(self, client):
        r = client.get("/q1")
        assert b"2026-03-01" in r.data

    def test_shows_consumption_data(self, client):
        r = client.get("/q1")
        assert b"2025-11-01" in r.data