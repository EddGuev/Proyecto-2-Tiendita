from locust import HttpUser, task, between


class UsuarioTiendaCompleta(HttpUser):
    wait_time = between(0.2, 0.8)

    @task(3)
    def comprarProducto(self):
        # El experimento se centra en el producto 3 porque inicia con stock=1
        with self.client.post("/productos/3", json={"producto_id": 3}, catch_response=True) as respuesta:
            if respuesta.status_code == 200:
                respuesta.success()
            elif respuesta.status_code == 400:
                # Sin stock también es un resultado válido en la simulación
                respuesta.success()
            else:
                respuesta.failure(f"Código inesperado: {respuesta.status_code}")

    @task(1)
    def getProducto(self):
        # Lectura del catálogo para mezclar tráfico de escritura y consulta
        self.client.get("/productos")
