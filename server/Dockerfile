FROM liquibase:alpine

# Expose the Gunicorn default port
EXPOSE 5000

USER root

# Create a liquibase user and group with limited privileges
RUN addgroup -S liquibasegroup && adduser -S liquibaseuser -G liquibasegroup

# Install python, pip, git, ssh client, and gunicorn
RUN apk add --no-cache python3 py3-pip git openssh

# Create necessary directories and set ownership to liquibaseuser
RUN mkdir /server /liquibase/changelog && \
    chown -R liquibaseuser:liquibasegroup /server /liquibase/changelog

# Switch to non-root liquibaseuser
USER liquibaseuser

# Set the working directory to /server
WORKDIR /server

# Copy the application code to the /server folder and set correct ownership
COPY --chown=liquibaseuser:liquibasegroup . /server

# Create and activate a Python virtual environment
RUN python3 -m venv venv

# Install required Python packages using the build script (ensure it handles dependencies)
RUN ./build.sh

# Ensure the user has access to /liquibase/changelog for Liquibase operations
WORKDIR /liquibase/changelog

# Command to run the Flask app using Gunicorn with 4 workers
CMD ["/bin/sh", "-c", "source /server/venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:5000 main:app --chdir /server"]
