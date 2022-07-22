FROM python:3.8.13
WORKDIR /app
COPY ./ ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip --default-timeout=1000 install -r requirements.txt
CMD python -u app.py
