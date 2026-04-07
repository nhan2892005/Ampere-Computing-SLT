class TestQ2:
    def test_get_returns_200(self, client):
        assert client.get("/q2").status_code == 200

    def test_get_has_form_inputs(self, client):
        r = client.get("/q2")
        assert b'name="name"' in r.data
        assert b'name="location"' in r.data

    def test_post_inserts_facility(self, client):
        r = client.post("/q2", data={"name": "SLT", "location": "Ho Chi Minh"})
        assert r.status_code in (200, 302)

    def test_post_slt_persists_in_db(self, client):
        client.post("/q2", data={"name": "SLT", "location": "Ho Chi Minh"})
        r = client.get("/q0")
        assert b"SLT" in r.data

    def test_post_duplicate_does_not_crash(self, client):
        client.post("/q2", data={"name": "SLT", "location": "Ho Chi Minh"})
        r = client.post("/q2", data={"name": "SLT", "location": "Ho Chi Minh"})
        assert r.status_code in (200, 302)