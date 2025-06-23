# VulnTrack Celery Worker

## ¿Qué es esto?
Este archivo describe cómo lanzar y probar el worker de Celery para procesar los escaneos en background usando Redis.

---

## 1. Lanzar el worker de Celery

Asegúrate de tener Redis corriendo en `localhost:6379`.

Desde la raíz del proyecto, ejecuta (en Windows, usa el pool solo):

```
E:/Universidad/vulntrack-legacy-backend/.venv/Scripts/python.exe -m celery -A app.worker worker --loglevel=info --pool=solo
```

O usando el script de worker incluido:

```
E:/Universidad/vulntrack-legacy-backend/.venv/Scripts/python.exe app/worker.py
```

---

## 2. Probar el flujo end-to-end

1. **Levanta tu API FastAPI normalmente** (por ejemplo, con Uvicorn):
   ```
   E:/Universidad/vulntrack-legacy-backend/.venv/Scripts/python.exe -m uvicorn app.main:app --reload
   ```
2. **Lanza el worker de Celery** (en otra terminal):
   ```
   E:/Universidad/vulntrack-legacy-backend/.venv/Scripts/python.exe -m celery -A app.worker worker --loglevel=info --pool=solo
   ```
3. **Haz una petición POST a `/api/v1/` o `/api/v1/batch`** para disparar un escaneo.
4. **Verifica en Supabase**:
   - El estado del scan cambia de `in_progress` a `completed` cuando el worker termina.
   - Se insertan resultados en las tablas `scan_results`, `vulnerabilities` y `notifications`.

---

## 3. Monitoreo de tareas con Flower

Puedes monitorear el estado de los tasks y workers con [Flower](https://flower.readthedocs.io/):

```
E:/Universidad/vulntrack-legacy-backend/.venv/Scripts/python.exe -m celery -A app.worker flower --pool=solo
```

Luego abre [http://localhost:5555](http://localhost:5555) en tu navegador para ver el dashboard.

---

## 4. Notas
- Si cambias la lógica de los tasks, reinicia el worker.
- El worker puede correr en cualquier máquina que tenga acceso a Redis y Supabase.
- En Windows, usa siempre `--pool=solo` para evitar errores de permisos.
