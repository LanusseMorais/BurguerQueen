FROM python:3.8
WORKDIR /src
COPY src .
RUN pip install -r app/requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]
