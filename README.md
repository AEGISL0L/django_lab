# Django Lab (migración desde Flask)

Proyecto Django para migrar el módulo de **solicitudes de fórmulas magistrales** desde una app Flask a Django, reutilizando templates y replicando el flujo principal.

## Estado actual

Implementado/decidido hasta ahora:

- Proyecto Django creado con estructura `config/` + `apps/`.
- App única: `apps/formulations` (sin inventario, sin categoría).
- Formulario público para solicitar fórmulas **sin login**.
- Panel interno para ver/gestionar solicitudes **con autenticación Django**.
- `requiere_rele` se definió como **booleano** (checkbox).
- Templates adaptados a DTL:
  - `templates/base.html` (simplificado)
  - `templates/lab/solicitar_formula.html`

Pendiente de adaptar:
- `lista_formulas.html`
- `ver_formula.html`
- `formula_timeline.html`

## Estructura del proyecto

```text
django_lab/
├─ manage.py
├─ config/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
└─ apps/
   ├─ __init__.py
   └─ formulations/
      ├─ __init__.py
      ├─ admin.py
      ├─ apps.py
      ├─ migrations/
      │  └─ __init__.py
      ├─ models.py
      ├─ forms.py
      ├─ views.py
      └─ tests.py
```

> Recomendado (cuando toque): crear también `apps/formulations/urls.py`, y carpetas `templates/`, `static/`, `media/`.

## Configuración (`config/settings.py`)

Ajustes relevantes:

- Se añadió la app:
  - `INSTALLED_APPS += ['apps.formulations']`
- Templates globales:
  - `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']`
- Static/media:
  - `STATIC_URL = 'static/'`
  - `STATICFILES_DIRS = [BASE_DIR / 'static']`
  - `MEDIA_URL = 'media/'`
  - `MEDIA_ROOT = BASE_DIR / 'media'`
- Auth redirects:
  - `LOGIN_URL = 'login'`
  - `LOGIN_REDIRECT_URL = 'formulations:lista_formulas'`
  - `LOGOUT_REDIRECT_URL = 'formulations:solicitar_formula'`

## Formularios (`apps/formulations/forms.py`)

Implementado:

- Generación de `petition_id` tipo: `FRM-YYYYMMDDHHMM-XXXX`
- `FormulaRequestCreateForm` (`ModelForm`) con:
  - `petition_id` mostrado como campo deshabilitado
  - `requiere_rele` booleano (checkbox)
  - widgets Bootstrap (`form-control`, `form-check-input`)
- En `save()` se asegura que `petition_id` exista aunque el campo esté deshabilitado y no viaje en POST.

## Templates

### `templates/base.html` (DTL, simplificado)

- Migrado de Flask a Django:
  - `{% load static %}`
  - `url_for('static', ...)` → `{% static '...' %}`
  - `current_user.is_authenticated` → `user.is_authenticated`
  - `flash/get_flashed_messages` → Django `messages`
- Navbar simplificado:
  - Link a solicitar fórmula (público)
  - Login/Logout (según autenticación)
  - Gestión fórmulas visible solo para autenticados

### `templates/lab/solicitar_formula.html` (DTL)

- Reemplazado:
  - `{{ form.csrf_token }}` → `{% csrf_token %}`
- Checkbox para `requiere_rele` usando `form-check` (Bootstrap)
- Manejo de errores por campo (`form.<field>.errors`)

## Instalación / comandos usados (venv)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

python -m pip install --upgrade pip
python -m pip install 'Django>=5.0' Pillow

python -m django startproject config .
mkdir -p apps
python manage.py startapp formulations
mv formulations apps/formulations
touch apps/__init__.py

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Próximos pasos

1. Completar `models.py` (si no está ya creado) con:
   - `FormulaRequest`
   - (opcional) `AuditLog` para timeline
2. Crear `apps/formulations/urls.py` y conectar en `config/urls.py`:
   - rutas públicas + panel
   - `django.contrib.auth.urls` para login/logout
3. Servir media en desarrollo (`MEDIA_URL/MEDIA_ROOT`).
4. Adaptar templates pendientes:
   - `lista_formulas.html`
   - `ver_formula.html`
   - `formula_timeline.html`

## Notas sobre diferencias Flask → Django

- `petition_id` en Django:
  - se muestra en UI, pero al estar `disabled` no se envía en POST
  - se asegura en el servidor en `form.save()`
- Subida de imágenes:
  - Flask guardaba `filename` en DB y archivo en `UPLOAD_FOLDER`
  - Django usa `ImageField(upload_to=...)` y gestiona la ruta en `MEDIA_ROOT`

---
Si quieres, añade aquí capturas o enlaces a los templates Flask originales para acelerar la adaptación de los tres templates restantes.
