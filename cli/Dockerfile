FROM python:3.10.14-alpine3.19

WORKDIR /usr/src/blockchat

RUN pip freeze > python_packages.txt
RUN pip install -r python_packages.txt

# TODO: fix exposed port
EXPOSE 3001

COPY . ./cli

# TODO: check the directory of blockchat.py file
CMD ["python3", "blockchat.py"]
