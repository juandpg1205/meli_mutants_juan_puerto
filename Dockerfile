FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Puerto sera el 8080 Flask
EXPOSE 8080

#Comando de Ejecucion
CMD ["python", "mutant_api.py"]
