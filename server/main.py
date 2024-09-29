from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

def add_remote_keys():
    # Define the known_hosts path
    known_hosts_path = os.path.expanduser('~/.ssh/known_hosts')

    # Run ssh-keyscan and capture the output (without adding it to the file yet)
    result = subprocess.run(['ssh-keyscan', '-t', 'ed25519', 'github.com'], capture_output=True, text=True, check=True)

    # Check if the key is already in the known_hosts file
    # Check if the known_hosts file exists
    if not os.path.exists(known_hosts_path):
        # Create the known_hosts file if it doesn't exist
        with open(known_hosts_path, 'w') as known_hosts:
            known_hosts.write('')

    with open(known_hosts_path, 'r') as known_hosts:
        known_hosts_content = known_hosts.read()

    if result.stdout not in known_hosts_content:
        # If the key does not exist, append it to the known_hosts file
        with open(known_hosts_path, 'a') as known_hosts:
            known_hosts.write(result.stdout)
        print("Key added to known_hosts.")
    else:
        print("Key already exists in known_hosts.")

# Define the route to update the database
@app.route('/update-db', methods=['GET'])
def update_db():
    try:
        ssh_key_path = os.path.expanduser('~/.ssh/id_rsa')

        # Check if the SSH key exists
        if not os.path.exists(ssh_key_path):
            # Create the .ssh directory if it doesn't exist
            os.makedirs(os.path.dirname(ssh_key_path), exist_ok=True)
            
            # Generate the SSH key
            subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', ssh_key_path, '-N', ''], check=True)

        # Run 'git pull' to update the repository
        add_remote_keys()
        # Set the working directory to /changelog
        os.chdir('/changelog')
        
        subprocess.run(['git', 'pull'], check=True, text=True)
        
        # Run 'liquibase update' to apply the database changes
        liquibase_update = subprocess.run(['liquibase', 'update'], check=True, text=True, capture_output=True)
        liquibase_output = liquibase_update.stdout
        
        # Return success message along with outputs from the commands
        return jsonify({
            "status": "success",
            "liquibase_output": liquibase_output
        })
        
    except subprocess.CalledProcessError as e:
        # Return error details if the commands fail
        return jsonify({
            "status": "error",
            "message": str(e),
            "output": e.output
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
