FROM python:3.7-alpine
WORKDIR /app
RUN apk add --update python3 --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001
COPY . .
CMD python3 /app/app.py