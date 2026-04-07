class TestQ3:
    def test_returns_200(self, client):
        assert client.get("/q3").status_code == 200

    def test_shows_expected_table(self, client):
        r = client.get("/q3")
        assert b"HN" in r.data
        assert b"DN" in r.data
        assert b"VNM" in r.data

    def test_hn_vnm_remain_50(self, client):
        r = client.get("/q3")
        assert b"50" in r.data

    def test_dn_vnm_remain_negative_200(self, client):
        r = client.get("/q3")
        assert b"-200" in r.data

    def test_dn_vnm_overdue_250(self, client):
        r = client.get("/q3")
        assert b"250" in r.data

    def test_need_import_yes_no(self, client):
        r = client.get("/q3")
        assert b"Yes" in r.data
        assert b"No" in r.data