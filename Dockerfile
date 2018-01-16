# Hosts django project w/ uwsgi

#FROM python:3
FROM quanted/qed_py3:dev

# Install Python Dependencies
# COPY requirements.txt /tmp/
COPY . /src/
#RUN pip install --requirement /src/requirements.txt
#RUN for file in *_app/requirements.txt; do pip install --requirement /src/$file; done

# Install uWSGI
# RUN pip install uwsgi added to requirements.txt

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

# Copy the project code
#COPY . /src/
WORKDIR /src
EXPOSE 8080

# Ensure "docker_start" is executable
RUN chmod 755 /src/docker_start.sh
s
RUN pip freeze | grep Django

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH="/src"

# ENTRYPOINT ["sh /src/docker_start.sh"]
CMD ["sh", "/src/docker_start.sh"]
