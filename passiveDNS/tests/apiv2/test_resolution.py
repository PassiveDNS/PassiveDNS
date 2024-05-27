import unittest
from fastapi.testclient import TestClient

from db.database import get_db
from models.user import User
from models.domain_name import DomainName
from main import app

client = TestClient(app)

class AuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = get_db()

        cls.user1 = User.new("TestUser1", "user1", "user1@test.com")
        cls.user1.insert()

        client.post("/token", json={"identity":"TestUser1", "password":"user1"})
        client.post("/dn/dns.google.com")
        cls.dn1 = DomainName.get("dns.google.com")
        cls.ip1 = cls.dn1.resolve()
    
    @classmethod
    def tearDownClass(cls) -> None:
        client.delete("/dn/dns.google.com")
        client.get("/logout")
        cls.user1.delete()

#/resolution/{dn} get
    def test_get_resolution(self) -> None:
        response = client.get("/resolution/dns.google.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("resolution", response.json())
    
    def test_get_resolution_not_found(self) -> None:
        response = client.get("/resolution/example.com")
        self.assertEqual(response.status_code, 404)

#/resolution/{dn}/history get
    def test_get_resolution_history(self) -> None:
        response = client.get("/resolution/dns.google.com/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn("history", response.json())
    
    def test_get_resolution_history_not_found(self) -> None:
        response = client.get("/resolution/example.com/history")
        self.assertEqual(response.status_code, 404)

#/reverse/{ip} get
    def test_get_reverse(self) -> None:
        response = client.get(f"/reverse/{self.ip1}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("resolution_list", response.json())
    
    def test_get_reverse_not_found(self) -> None:
        response = client.get("/reverse/1.2.3.4")
        self.assertEqual(response.status_code, 404)

#/reverse/{ip}/history get
    def test_get_reverse_history(self) -> None:
        response = client.get(f"/reverse/{self.ip1}/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn("history", response.json())
    
    def test_get_resolution_history_not_found(self) -> None:
        response = client.get("/resolution/1.2.3.4/history")
        self.assertEqual(response.status_code, 404)