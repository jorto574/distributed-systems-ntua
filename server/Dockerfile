FROM python:3.10.14-alpine3.19

WORKDIR /usr/src/blockchat

RUN pip freeze > python_packages.txt
RUN pip install -r python_packages.txt

# TODO: fix exposed port
EXPOSE 3000

COPY . ./server

CMD ["python3", "app.py"]
