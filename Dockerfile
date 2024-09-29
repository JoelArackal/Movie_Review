# Test web app that returns the name of the host/pod/container servicing req
FROM python:3.11-slim-buster

LABEL org.opencontainers.image.title="Hello Docker Learners!" \
      org.opencontainers.image.description="Web server showing host that responded" \
      org.opencontainers.image.authors="@joeljozarackal"


WORKDIR /app


# Copy app code (.) to /usr/src/app in container image
COPY . /app/

# Set working directory context

COPY requirements.txt /app/

# Install dependencies from package.json
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

# Command for container to execute
CMD [ "python", "run.py"]