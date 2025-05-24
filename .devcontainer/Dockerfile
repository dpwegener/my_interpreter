FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

WORKDIR /workspaces/personal_finance_tracker
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
#ADD . .

# Sync the project
#RUN --mount=type=cache,target=/root/.cache/uv \
#    uv sync --locked
