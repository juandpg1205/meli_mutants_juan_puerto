# mutant_api.py
import os
from flask import Flask, request, jsonify
from mutant_detector import is_mutant  # Import function to determine mutant DNA sequences
from flask_sqlalchemy import SQLAlchemy  # Import for database operations
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# Database Configuration
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")  # Google Cloud SQL connection name
DB_USER = os.getenv("DB_USER", "postgres")  # Database username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Database password
DB_NAME = os.getenv("DB_NAME", "mutantdb")  # Database name

# Set SQLAlchemy database URI with Cloud SQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
    f"?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking to save resources
db = SQLAlchemy(app)

# Database Model for storing DNA sequences
class DNASequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key ID
    dna = db.Column(db.String(255), unique=True, nullable=False)  # Unique DNA sequence string
    is_mutant = db.Column(db.Boolean, nullable=False)  # Boolean flag for mutant status

# Initialize the database with tables if they don’t already exist
with app.app_context():
    db.create_all()

# Endpoint to detect if a DNA sequence is from a mutant
@app.route('/mutant', methods=['POST'])
def detect_mutant():
    data = request.get_json()  # Get JSON data from request
    if not data or 'dna' not in data:  # Validate presence of 'dna' in request
        return jsonify({"error": "Invalid input, 'dna' key is required"}), 400

    dna = data['dna']
    # Transform DNA list to a single string for consistent storage and querying
    dna_string = ','.join(dna)

    # Check if DNA sequence already exists in the database
    existing_sequence = DNASequence.query.filter_by(dna=dna_string).first()
    if existing_sequence:
        is_mutant_flag = existing_sequence.is_mutant  # Use existing result if DNA is already in database
    else:
        # Determine if DNA is mutant and save the result
        is_mutant_flag = is_mutant(dna)
        new_sequence = DNASequence(dna=dna_string, is_mutant=is_mutant_flag)
        db.session.add(new_sequence)  # Add new sequence to session
        db.session.commit()  # Commit changes to save sequence

    # Return appropriate response based on mutant status
    if is_mutant_flag:
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Not a mutant"}), 403

# Endpoint to retrieve statistics about DNA sequences
@app.route('/stats', methods=['GET'])
def stats():
    count_mutant_dna = DNASequence.query.filter_by(is_mutant=True).count()  # Count mutant DNA sequences
    count_human_dna = DNASequence.query.filter_by(is_mutant=False).count()  # Count human (non-mutant) DNA sequences
    # Calculate mutant-to-human ratio, handling division by zero
    ratio = count_mutant_dna / count_human_dna if count_human_dna > 0 else 0
    return jsonify({
        "count_mutant_dna": count_mutant_dna,
        "count_human_dna": count_human_dna,
        "ratio": ratio
    })

# Start the Flask application on port 8080
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
