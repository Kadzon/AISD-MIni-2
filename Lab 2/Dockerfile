FROM tensorflow/tensorflow:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

COPY connect.py .
COPY base_iris_lab2.py .
COPY iris_extended_encoded.csv .

EXPOSE 4000

# Define environment variable
ENV FLASK_ENV=development
ENV FLASK_APP=connect.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=4000
ENV FLASK_DEBUG=1

# Run app.py when the container launches
CMD ["flask", "run"]