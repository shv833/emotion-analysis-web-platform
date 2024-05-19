FROM python:3.8.5-alpine3.12

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.cargo/bin:${PATH}"

RUN apk add --no-cache curl gcc g++ make bash dos2unix \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN dos2unix /usr/src/app/entrypoint.sh && chmod 755 /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
