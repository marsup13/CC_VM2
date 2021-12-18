FROM mysql
# Add a database
ENV MYSQL_DATABASE flask
ENV MYSQL_ROOT_PASSWORD root
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./ /docker-entrypoint-initdb.d/