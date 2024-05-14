FROM python:3.8.5-alpine3.12

# Set work directory
WORKDIR /usr/src/backend

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.cargo/bin:${PATH}"

# Install dependencies and Rust in one layer to reduce image size
RUN apk add --no-cache curl gcc g++ make bash dos2unix \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && pip install --upgrade pip

# Install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Prepare entrypoint script
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN dos2unix /usr/src/app/entrypoint.sh && chmod 755 /usr/src/app/entrypoint.sh

# Run the application
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
