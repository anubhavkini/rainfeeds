FROM python:3-slim

WORKDIR /app
VOLUME ["/app/data"]

COPY ["requirements.txt", "requirements.txt"]
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY ["src/", "src/"]

CMD ["python", "-m", "src.main"]