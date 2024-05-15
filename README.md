# My diploma project
## Web Platform with Integrated Video Conferencing and Emotion Analysis of Students and Teachers

## Requirements for prod mode
- Docker
- Make

## Requirements for dev mode
- Docker
- Make
- Python
- Node.js

## Getting started with Windows 10/11

```
winget install ezwinports.make
```

```
git clone https://github.com/shv833/emotion-analysis-web-platform.git
```

```
cd .\emotion-analysis-web-platform
```

## Configure .env.dev or .env.prod for email notification
- Configure your email smtp
- Update env files with next info
```
EMAIL_USER=<your_email@gmail.com>
EMAIL_PASS=<your api token for email>
EMAIL_SENDER=<your_email@gmail.com>
```

## Running tests


## Running in prod mode
```
make prod
```
or for clean run(rebuild images and reinstall packages)
```
make cprod
```

## Running in dev mode
```
make dev
```
or for clean run(rebuild images and reinstall packages)
```
make cdev
```

## How to test app manually


## Short description of workflow


## Terraform `healthcheck`

```json
"healthCheck": {
    "command": [
        "CMD-SHELL",
        "curl --fail http://localhost:8000/admin/ || exit 1",
        "curl --fail http://localhost:3000/ || exit 1"
    ],
    "interval": 30,
    "retries": 3,
    "timeout": 5
}
```

## Environment variables
| Environment variables                  | Default Value                                 | Description                                                            |
|----------------------------------------|-----------------------------------------------|------------------------------------------------------------------------|
