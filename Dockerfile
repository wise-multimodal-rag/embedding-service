FROM python:3.9.13-slim

# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV PYTHONPATH=/home/wisenut/app:${PYTHONPATH}

# Install libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    vim \
    tzdata

# Set the working directory
WORKDIR /home/wisenut/app

# Copy necessary files and directory
COPY pyproject.toml version_info.py .env ./
COPY ./app ./app/

# Install Requirements
RUN pip install --upgrade pip && pip install --no-cache-dir .[test,lint]

# Expose the port
EXPOSE 8000

# Run the app
CMD ["python", "app/main.py"]