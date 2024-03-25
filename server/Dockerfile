FROM python:3.10.14-alpine3.19

WORKDIR /usr/src/blockchat/server

# TODO: package installation process
RUN pip install

COPY ../start_server.py /usr/src/blockchat/
COPY . /usr/src/blockchat/server/

EXPOSE 3000

CMD []
