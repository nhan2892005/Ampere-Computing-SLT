import json
import pytest


class TestIndex:
    def test_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_contains_welcome_text(self, client):
        r = client.get("/")
        assert b"Welcome" in r.data