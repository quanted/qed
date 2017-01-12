# Hosts django project w/ uwsgi

#FROM python:2.7
FROM puruckertom/qed_py27

# Install Python Dependencies
#COPY requirements.txt /tmp/
COPY . /src/
RUN pip install --requirement /src/requirements.txt
#RUN for file in *_app/requirements.txt; do pip install --requirement /src/$file; done

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

# Copy the project code
#COPY . /src/
WORKDIR /src
EXPOSE 8080

# Ensure "docker_start" is executable
RUN chmod 755 /src/docker_start.sh

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH="/src"

CMD ["sh", "/src/docker_start.sh"]
#ENTRYPOINT ["/src/docker_start.sh"]
#CMD ["uwsgi", "/etc/uwsgi/uwsgi.ini"]  # ["python", "manage.py", "runserver", "0.0.0.0:8080"]