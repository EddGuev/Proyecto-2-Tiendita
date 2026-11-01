from locust import HttpUser, task, between


class UsuarioTiendaCompleta(HttpUser):
    wait_time = between(0.2, 0.8)

    @task(3)
    def comprarProducto(self):
        with self.client.post("/productos/3", json={"producto_id": 3}, catch_response=True) as respuesta:
            if respuesta.status_code == 200:
                respuesta.success()
            elif respuesta.status_code == 400:
                respuesta.success()
            else:
                respuesta.failure(f"Código inesperado: {respuesta.status_code}")

    @task(1)
    def getProducto(self):
        self.client.get("/productos")
