# mutant_api.py
import os
from flask import Flask, request, jsonify
from mutant_detector import is_mutant
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
#DB Config
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "mutantdb")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
    f"?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#DB Model
class DNASequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dna = db.Column(db.String(255), unique=True, nullable=False)
    is_mutant = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/mutant', methods=['POST'])
def detect_mutant():
    data = request.get_json()
    if not data or 'dna' not in data:
        return jsonify({"error": "Invalid input, 'dna' key is required"}), 400

    dna = data['dna']
    #Transform DNA
    dna_string = ','.join(dna)

    #Check DB
    existing_sequence = DNASequence.query.filter_by(dna=dna_string).first()
    if existing_sequence:
        is_mutant_flag = existing_sequence.is_mutant
    else:
        #Mutant or not
        is_mutant_flag = is_mutant(dna)
        #Save the secuences in DB
        new_sequence = DNASequence(dna=dna_string, is_mutant=is_mutant_flag)
        db.session.add(new_sequence)
        db.session.commit()

    if is_mutant_flag:
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Not a mutant"}), 403

@app.route('/stats', methods=['GET'])
def stats():
    count_mutant_dna = DNASequence.query.filter_by(is_mutant=True).count()
    count_human_dna = DNASequence.query.filter_by(is_mutant=False).count()
    ratio = count_mutant_dna / count_human_dna if count_human_dna > 0 else 0
    return jsonify({
        "count_mutant_dna": count_mutant_dna,
        "count_human_dna": count_human_dna,
        "ratio": ratio
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
