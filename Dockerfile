FROM python:3.11-slim

# Evita buffering de logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala uv
RUN pip install --no-cache-dir uv

# Copia apenas arquivos de dependência primeiro (cache)
COPY pyproject.toml uv.lock* ./

# Instala dependências
RUN uv pip install --system -r pyproject.toml

# Copia o resto da aplicação
COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
