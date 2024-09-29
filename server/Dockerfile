FROM liquibase:alpine

# Expose the Gunicorn default port
EXPOSE 5000

USER root

# Install python, pip, git, ssh client, and gunicorn
RUN apk add --no-cache python3 py3-pip git openssh

# Create necessary directories and set ownership to liquibase
RUN mkdir /server /changelog


# Switch to non-root liquibase

RUN mkdir /root/.ssh

# Set the working directory to /server
WORKDIR /server

# Copy the application code to the /server folder and set correct ownership
COPY . /server

# Create and activate a Python virtual environment
RUN python3 -m venv venv

# Install required Python packages using the build script (ensure it handles dependencies)
RUN ./build.sh

# Ensure the user has access to /liquibase/changelog for Liquibase operations
RUN mkdir /liquibase/changelog
RUN git config --global --add safe.directory /changelog
WORKDIR /changelog

# Command to run the Flask app using Gunicorn with 4 workers
CMD ["/bin/sh", "-c", "source /server/venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:5000 main:app --chdir /server"]
