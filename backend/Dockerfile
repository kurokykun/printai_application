FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Descargar ChromeDriver desde una fuente confiable
RUN apt-get update && apt-get install -y chromium-driver && \
    ln -s /usr/bin/chromedriver /usr/local/bin/chromedriver

# Verificar la instalación de ChromeDriver
RUN ls -l /usr/local/bin/chromedriver && /usr/local/bin/chromedriver --version

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir poetry

COPY . .

EXPOSE 7013

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7013"]
