def test_crear_y_obtener_socio(client, socio):
    assert socio["nombre"] == "Ana"
    assert client.get("/socios/1").status_code == 200
    assert len(client.get("/socios").json()) == 1


def test_email_duplicado_409(client, socio):  # Regla 8
    res = client.post("/socios", json={"nombre": "Otra Ana", "email": "ana@gmail.com"})
    assert res.status_code == 409


def test_email_invalido_422(client):
    res = client.post("/socios", json={"nombre": "Ana", "email": "no-es-un-email"})
    assert res.status_code == 422


def test_modificar_socio(client, socio):
    res = client.put(
        "/socios/1", json={"nombre": "Ana Modificada", "email": "ana@gmail.com", "activo": False}
    )
    assert res.status_code == 200
    assert res.json()["activo"] is False


def test_modificar_socio_email_duplicado_409(client, socio):  # Regla 8
    client.post("/socios", json={"nombre": "Juan", "email": "juan@gmail.com"})
    res = client.put(
        "/socios/2", json={"nombre": "Juan", "email": "ana@gmail.com", "activo": True}
    )
    assert res.status_code == 409


def test_borrar_socio(client, socio):
    assert client.delete("/socios/1").status_code == 204
    assert client.get("/socios/1").status_code == 404


def test_borrar_socio_con_prestamos_409(client, socio, libro):
    client.post("/prestamos", json={"socio_id": 1, "libro_id": 1})
    assert client.delete("/socios/1").status_code == 409


def test_socio_inexistente_404(client):  # Regla 7
    assert client.get("/socios/99").status_code == 404
    assert (
        client.put(
            "/socios/99", json={"nombre": "X", "email": "x@gmail.com", "activo": True}
        ).status_code
        == 404
    )
    assert client.delete("/socios/99").status_code == 404