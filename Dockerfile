FROM python:3.9-slim

WORKDIR /iiq

COPY requirement.txt /iiq/

RUN pip3 install --no-cache-dir -r requirement.txt

COPY . /iiq/

EXPOSE 5000

CMD ["python", "be.py"]