FROM python:3.12.3
EXPOSE 5000
WORKDIR /app
COPY requaerment.txt .
RUN pip install -r requaerment.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]