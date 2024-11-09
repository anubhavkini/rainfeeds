FROM python:3-slim

WORKDIR /app
VOLUME ["/app/data"]

COPY ["src/", "src/"]
COPY ["LICENSE", "LICENSE"]
COPY ["setup.py", "setup.py"]

RUN ["pip", "install", "--no-cache-dir", "-e", "."]

CMD ["rainfeeds", "sync"]