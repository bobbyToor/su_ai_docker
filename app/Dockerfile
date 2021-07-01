FROM tiangolo/uvicorn-gunicorn:python3.8

COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY . .

EXPOSE 3001

CMD ["python3", "main.py"]