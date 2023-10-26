FROM python:3.11.6-slim-bullseye

ARG LOG_DIR

# Env. variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Labels
LABEL type=application
LABEL name=EventsAPI

# Set work directory
WORKDIR /usr/src/app

# Create log directory
RUN mkdir -p $LOG_DIR

# Install dependencies
RUN apt-get update
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
COPY ./entrypoint.sh .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements-dev.txt


# Copy source code
COPY . .

# Ports
EXPOSE 8000/tcp

# Entrypoint
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


