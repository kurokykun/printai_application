# Documentación del Proyecto

## Instrucciones de Configuración y Ejecución

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd printai_application
   ```

3. Ejecuta el proyecto con Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Accede a los servicios:
   - **Frontend**: [http://localhost:8080](http://localhost:8080)
   - **Backend (FastAPI)**: [http://localhost:18000/docs](http://localhost:18000/docs) (Swagger UI)
   - **n8n**: [http://localhost:5678](http://localhost:5678)

## Comandos para Ejecutar Pruebas

### Backend
Ejecuta las pruebas del backend:
```bash
   docker-compose exec backend pytest
```

### Frontend
Ejecuta las pruebas del frontend:
```bash
   docker-compose exec frontend npm test
```

## Ejemplos de Consultas y Respuestas

### Endpoint `/books/search`
**Consulta**:
```http
GET /books/search?title=python
```
**Respuesta**:
```json
[
  {
    "title": "Learn Python Programming",
    "price": 19.99,
    "category": "Programming",
    "image_url": "https://..."
  }
]
```

### Endpoint `/headlines`
**Consulta**:
```http
GET /headlines
```
**Respuesta**:
```json
[
  {
    "title": "Breaking News",
    "url": "https://...",
    "score": 150
  }
]
```

## Esquema de Redis
- **Claves**:
  - `book:<id>`: Almacena información de libros en formato JSON.
    ```json
    {
      "title": "Book Title",
      "price": 19.99,
      "category": "Fiction",
      "image_url": "https://..."
    }
    ```