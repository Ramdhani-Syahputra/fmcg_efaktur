FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Basmi opencv-python bawaan ultralytics biar sisa yang headless doang
RUN pip uninstall -y opencv-python

RUN pip install opencv-python-headless

COPY . .

CMD ["tail", "-f", "/dev/null"]