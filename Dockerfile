FROM python:3.10

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./periodic_lambda_app /code/periodic_lambda_app

CMD ["uvicorn", "periodic_lambda_app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
