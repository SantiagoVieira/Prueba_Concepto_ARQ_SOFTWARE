import os

from fastapi.testclient import TestClient

import main

main.DB = "test.db"
if os.path.exists("test.db"):
    os.remove("test.db")

c = TestClient(main.app)
H = {"Authorization": "Bearer demo-token"}


def test_salud():
    assert c.get("/salud").json() == {"estado": "ok"}


def test_sin_token():
    assert c.get("/v1/tareas").status_code == 401


def test_validacion():
    assert c.post("/v1/tareas", json={"titulo": "a"}, headers=H).status_code == 422


def test_flujo():
    r = c.post("/v1/tareas", json={"titulo": "Preparar exposición"}, headers=H)
    assert r.status_code == 201
    tid = r.json()["id"]
    assert c.patch(f"/v1/tareas/{tid}/completar", headers=H).json()["hecha"] is True
    assert len(c.get("/v1/tareas", headers=H).json()) >= 1


def test_404():
    assert c.patch("/v1/tareas/9999/completar", headers=H).status_code == 404
