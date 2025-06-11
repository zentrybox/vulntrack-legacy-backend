# Running the Application with Uvicorn

## Development Server

Start the development server with auto-reload:

```bash
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Production Server

For production deployment:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Access Points

Once the server is running:

- **API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Documentation (ReDoc)**: http://127.0.0.1:8000/redoc  
- **Health Check**: http://127.0.0.1:8000/health
- **API Base URL**: http://127.0.0.1:8000/api/v1

## Uvicorn Options

Common uvicorn options:

- `--reload`: Enable auto-reload on code changes (development only)
- `--host`: Bind socket to this host (0.0.0.0 for all interfaces)
- `--port`: Bind socket to this port
- `--workers`: Number of worker processes (production)
- `--log-level`: Log level (debug, info, warning, error, critical)
- `--access-log`: Enable access log

Example with all options:
```bash
poetry run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log
```
