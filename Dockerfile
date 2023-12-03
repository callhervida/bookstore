FROM tiangolo/uwsgi-nginx:python3.10
ENV UWSGI_INI uwsgi.ini
ENV TZ="Asia/Tehran"
WORKDIR /app
ADD . /app
RUN chmod g+w /app
RUN apt-get update && \
    apt-get install -y libmariadb-dev && \
      rm -rf /var/lib/apt/lists/*
#RUN python3 -m pip install -i http://p.docker-registry.ir/PyPi/simple --trusted-host p.docker-registry.ir -r requirements.txt
RUN python3 -m pip install -r requirements.txt