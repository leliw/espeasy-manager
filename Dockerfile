# ------ Stage 1: Angular project ------
    FROM node:lts-slim AS angular-build
    WORKDIR /app
    
    COPY frontend/package.json frontend/package-lock.json ./
    RUN npm install
    
    COPY frontend/ .
    RUN npm run build
    
# ------ Stage 2: Python/FastAPI project ------
    FROM python:3.12.10-slim-bookworm

    # The installer requires curl (and certificates) to download the release archive
    RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

    # Download the latest installer
    ADD https://astral.sh/uv/install.sh /uv-installer.sh

    # Run the installer then remove it
    RUN sh /uv-installer.sh && rm /uv-installer.sh

    # Ensure the installed binary is on the `PATH`
    ENV PATH="/root/.local/bin/:$PATH"

    
    # Keeps Python from generating .pyc files in the container
    ENV PYTHONDONTWRITEBYTECODE=1
    # Turns off buffering for easier container logging
    ENV PYTHONUNBUFFERED=1
    
    COPY ./backend/pyproject.toml ./backend/uv.lock /app/

    # Sync the project into a new environment, using the frozen lockfile
    WORKDIR /app
    RUN uv sync --frozen

    COPY ./backend/src /app
    # Copy Angular build to FastAPI static folder
    COPY --from=angular-build /app/dist/frontend /app/static
    
    # Creates a non-root user with an explicit UID and adds permission to access the /app folder
    RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
    RUN mkdir /app/data
    RUN chown -R appuser /app/data
    
    USER appuser
    EXPOSE 8080
    CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
    