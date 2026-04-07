class TestIndex:
    def test_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_contains_welcome_text(self, client):
        r = client.get("/")
        assert b"Welcome" in r.data

class TestQ0:
    def test_returns_200(self, client):
        assert client.get("/q0").status_code == 200

    def test_shows_facility_table(self, client):
        r = client.get("/q0")
        assert b"HN" in r.data
        assert b"DN" in r.data
        assert b"HCM" in r.data