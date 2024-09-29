from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

# Define the route to update the database
@app.route('/update-db', methods=['GET'])
def update_db():
    try:
        # Run 'git pull' to update the repository
        git_pull = subprocess.run(['git', 'pull'], check=True, text=True, capture_output=True)
        git_output = git_pull.stdout
        
        # Run 'liquibase update' to apply the database changes
        liquibase_update = subprocess.run(['liquibase', 'update'], check=True, text=True, capture_output=True)
        liquibase_output = liquibase_update.stdout
        
        # Return success message along with outputs from the commands
        return jsonify({
            "status": "success",
            "git_output": git_output,
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
