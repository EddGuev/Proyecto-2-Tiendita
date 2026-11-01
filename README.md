# Proyecto 2 — Simulador de Venta Relámpago (FastAPI & Locust)

Gestión de transacciones concurrentes, resolución de condiciones de carrera con `asyncio.Lock()` y pruebas de estrés con Locust.

## Estructura

```
Proyecto-2-Tiendita/
├── backend/
│   └── main.py          # API con FastAPI y lógica del inventario
├── frontend/
│   ├── index.html       # Interfaz del cliente
│   └── app.js           # Consumo de la API con fetch
└── locust.py            # Escenario de carga para la venta relámpago
```

## Inventario (simulación en memoria)

| ID | Producto        | Precio | Stock |
|----|-----------------|--------|-------|
| 1  | Galletas Maria  | 12     | 30    |
| 2  | Fanta           | 18     | 25    |
| 3  | Jugo de Naranja | 22     | **1** |
| 4  | Chocolate       | 25     | 20    |
| 5  | Agua Mineral    | 10     | 50    |
| 6  | Pan Blanco      | 15     | 12    |

## Endpoints

| Método | Ruta                       | Descripción |
|--------|----------------------------|-------------|
| GET    | `/productos`               | Consulta catálogo completo |
| GET    | `/productos/{producto_id}` | Consulta un producto por ID |
| POST   | `/productos`               | Crea producto (201) |
| POST   | `/productos/{producto_id}` | Venta relámpago: descuenta una unidad |
| DELETE | `/productos/{producto_id}` | Elimina producto |
| GET    | `/prueba-asyncio`          | Espera asíncrona de 5 segundos |
| GET    | `/prueba-asyncio-3segundos`| Espera asíncrona de 3 segundos |
| GET    | `/prueba-asyncio-1segundo` | Espera asíncrona de 1 segundo |

## Cómo ejecutar

### API (puerto 8000)

```bash
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Cliente (puerto 3000)

```bash
cd frontend
python -m http.server 3000 --bind 127.0.0.1
```

Abrir http://127.0.0.1:3000

### Pruebas de carga con Locust

```bash
pip install locust
locust -f locust.py --host http://127.0.0.1:8000
```

Interfaz web en http://127.0.0.1:8089

## Experimentos de carga

- **Escenario A (sin lock):** comentar temporalmente `async with lock:` dentro de `comprarProducto`, reiniciar la API y correr Locust con 100 usuarios durante 20 segundos. En este caso se observa sobreventa y el stock puede terminar en negativo.
- **Escenario B (con lock):** restaurar `async with lock:`, reiniciar la API y repetir la misma carga. Con el candado activo, el stock del producto 3 se detiene en 0 y solo la primera compra resulta exitosa.
