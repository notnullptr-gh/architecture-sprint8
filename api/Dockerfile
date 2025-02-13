FROM python

RUN pip install flask Authlib PyJWT
COPY server.py /opt
WORKDIR /opt
CMD ["python", "server.py"]
