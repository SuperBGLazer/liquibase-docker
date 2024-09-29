# Custom Liquibase Docker Image

This custom Liquibase Docker image includes an API endpoint that allows pulling the latest changes from a GitHub repository and applying them to your database. The container uses SSH keys to securely communicate with GitHub. It runs a Flask server on port 5000 and exposes an endpoint to update the database schema automatically.

## Features
- API endpoint to pull changes from a GitHub repository and apply them to the database.
- Flask server running on port `5000`.
- Database updates triggered by making a request to the `/update-db` endpoint.
- SSH keys are securely mounted to the container for GitHub communication.
- Changelog files and `liquibase.properties` stored in a dedicated volume.

## Getting Started

### Pull the Docker Image

```bash
docker pull superlazer/liquibase-docker:latest
```

### Running the Container
To run the container, mount two volumes:
- One for the SSH keys (`/root/.ssh`)
- Another for the changelog and configuration files (`/changelog`).

```bash
docker run -d \
  -p 5000:5000 \
  -v /path/to/your/ssh-keys:/root/.ssh \
  -v /path/to/your/changelog:/changelog \
  superlazer/liquibase-docker:latest
```

### Required Files
1. **SSH Keys:** Stored at /root/.ssh. The container uses these keys to access your GitHub repository.
2. **Liquibase Changelog:** Stored at /changelog. This directory should include:
     - Liquibase changelog files (XML, YAML, or SQL).
     - A liquibase.properties file containing the necessary database connection details.

### API Endpoints
- **URL:** http://<your-container-ip>:5000/update-db
- **Method:** GET
- **Description:** Triggers a pull from the GitHub repository and applies any new database changes from the changelog files.