FROM python:3.12-slim

WORKDIR /app

# System deps for psycopg + PostGIS client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps first (better layer caching)
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        "fastapi[standard]==0.115.4" \
        "uvicorn[standard]==0.32.0" \
        "sqlalchemy==2.0.36" \
        "psycopg[binary]==3.2.3" \
        "alembic==1.14.0" \
        "pydantic==2.9.2" \
        "pydantic-settings==2.6.1" \
        "geoalchemy2==0.16.0" \
        "passlib[bcrypt]==1.7.4" \
        "python-jose[cryptography]==3.3.0" \
        "python-multipart==0.0.17"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
