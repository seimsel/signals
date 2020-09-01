FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["uvicorn", "--reload", "--port", "80", "signals.server:app" ]
