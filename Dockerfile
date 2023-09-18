# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a directory to hold application code
RUN mkdir -p /home/app/code

# Set work directory
WORKDIR /home/app/code

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create a non-root user to run the application
RUN useradd -ms /bin/bash app

# Give ownership of the home directory to the app user
RUN chown -R app /home/app

# Switch to the app user
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
