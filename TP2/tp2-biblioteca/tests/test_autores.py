def test_crud_autor(client):
    # Crear
    res = client.post("/autores", json={"nombre": "Cortázar", "nacionalidad": "Argentina"})
    assert res.status_code == 201
    assert res.json()["nombre"] == "Cortázar"

    # Listar y obtener por ID
    assert len(client.get("/autores").json()) == 1
    assert client.get("/autores/1").status_code == 200

    # Modificar
    res_mod = client.put(
        "/autores/1", json={"nombre": "Julio Cortázar", "nacionalidad": "Argentina"}
    )
    assert res_mod.status_code == 200
    assert res_mod.json()["nombre"] == "Julio Cortázar"

    # Borrar
    assert client.delete("/autores/1").status_code == 204
    assert client.get("/autores/1").status_code == 404


def test_autor_inexistente_404(client):  # Regla 7
    assert client.get("/autores/99").status_code == 404
    assert (
        client.put("/autores/99", json={"nombre": "X", "nacionalidad": "Y"}).status_code == 404
    )
    assert client.delete("/autores/99").status_code == 404