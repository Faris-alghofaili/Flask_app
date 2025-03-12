from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime , date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import PrimaryKeyConstraint ,ForeignKeyConstraint



app = Flask(__name__)
CORS(app)

# Configuration NEEDS TO BE UPDATED
app.config['SECRET_KEY'] = 'your_secret_key'        
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models correct upto data_base_V3.sql 

class User(db.Model):
    __tablename__ = "user"
    User_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)  # Changed TINYTEXT to Text for better compatibility
    is_admin = db.Column(db.Boolean, nullable=False)  # Changed TINYINT to Boolean
    created_at = db.Column(db.Date, nullable=False, default=date.today)

class Voice(db.Model):
    __tablename__ = 'voices'  # ✅ Matches MySQL table name
    voice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)  # ✅ Changed TINYTEXT to Text
    file_path = db.Column(db.Text, nullable=False)  # ✅ Changed TINYTEXT to Text
    created_at = db.Column(db.Date, default=datetime.utcnow, nullable=False)

class QuranVersion(db.Model):
    __tablename__ = 'quranversions'  # ✅ Matches MySQL table
    Version_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=datetime.utcnow, nullable=False)

class Project(db.Model):
    __tablename__ = "Projects"
    Project_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    User_id = db.Column(db.Integer, db.ForeignKey("user.User_id"), primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    voice_id = db.Column(db.Integer, db.ForeignKey("voices.voice_id"), nullable=False)
    quranversions_Version_id = db.Column(db.Integer, db.ForeignKey("quranversions.Version_id"), nullable=False)
    # Relationships (optional but helpful)
    user = db.relationship("User", backref=db.backref("projects", lazy=True))
    voice = db.relationship("Voice", backref=db.backref("projects", lazy=True))
    quran_version = db.relationship("QuranVersion", backref=db.backref("projects", lazy=True))

class AudioRequest(db.Model):
    __tablename__ = "audiorequests"

    request_id = db.Column(db.Integer, nullable=False,autoincrement=True)
    Projects_id = db.Column(db.Integer, nullable=False)
    Projects_user_User_id = db.Column(db.Integer, nullable=False)
    
    status = db.Column(db.String(20), nullable=False)
    audio_file_path = db.Column(db.Text, nullable=False)  # Changed TINYTEXT to Text for compatibility
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    start_verse = db.Column(db.Integer, nullable=False)
    end_verse = db.Column(db.Integer, nullable=False)
    include_tags = db.Column(db.Boolean, nullable=False)  # Fixed typo from `inculde_tags` to `include_tags`

    # Define Composite Primary Key
    __table_args__ = (
        PrimaryKeyConstraint("request_id", "Projects_id", "Projects_user_User_id"),
        ForeignKeyConstraint(
            ["Projects_id", "Projects_user_User_id"],
            ["Projects.Project_id", "Projects.User_id"]
        ),
    )

    # Relationships
    project = db.relationship(
        "Project",
        backref=db.backref("audiorequests", lazy=True),
        primaryjoin="and_(AudioRequest.Projects_id == Project.Project_id, "
                    "AudioRequest.Projects_user_User_id == Project.User_id)"
    )

class Surah(db.Model):
    __tablename__ = "surahs"
    sutrah_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    surah_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    arabic_name = db.Column(db.String(255), nullable=False)
    number_of_ayahs = db.Column(db.Integer, nullable=False)
    QuranVersions_Version_id = db.Column(db.Integer, db.ForeignKey("quranversions.Version_id"), primary_key=True, nullable=False)
    # Relationship to QuranVersions Table
    quran_version = db.relationship("QuranVersion", backref=db.backref("surahs", lazy=True))

class Tag(db.Model):
    __tablename__ = "tag"
    tag_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)  # Changed TINYTEXT to Text for better compatibility

class Verse(db.Model):
    __tablename__ = "verses"
    verse_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    verse_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)  # Changed MEDIUMTEXT to Text for better compatibility
    Surahs_sutrah_id = db.Column(db.Integer, db.ForeignKey("surahs.sutrah_id"), primary_key=True, nullable=False)
    # Relationship to Surahs Table
    surah = db.relationship("Surah", backref=db.backref("verses", lazy=True))

class VerseTag(db.Model):
    __tablename__ = "versetags"

    verse_tag_id = db.Column(db.Integer, nullable=False ,autoincrement=True)
    start_word_index = db.Column(db.Integer, nullable=False)
    end_word_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=date.today)

    # Foreign keys
    verses_verse_id = db.Column(db.Integer, nullable=False)
    tag_tag_id = db.Column(db.Integer, nullable=False)
    Projects_Project_id = db.Column(db.Integer, nullable=False)
    Projects_User_id = db.Column(db.Integer, nullable=False)

    # Define Composite Primary Key
    __table_args__ = (
        PrimaryKeyConstraint("verse_tag_id", "verses_verse_id", "tag_tag_id"),
        ForeignKeyConstraint(
            ["verses_verse_id"],
            ["verses.verse_id"]
        ),
        ForeignKeyConstraint(
            ["tag_tag_id"],
            ["tag.tag_id"]
        ),
        ForeignKeyConstraint(
            ["Projects_Project_id", "Projects_User_id"],
            ["Projects.Project_id", "Projects.User_id"]
        ),
    )

    # Relationships
    verse = db.relationship("Verse", backref=db.backref("versetags", lazy=True))
    tag = db.relationship("Tag", backref=db.backref("versetags", lazy=True))
    project = db.relationship(
        "Project",
        backref=db.backref("versetags", lazy=True),
        primaryjoin="and_(VerseTag.Projects_Project_id == Project.Project_id, "
                    "VerseTag.Projects_User_id == Project.User_id)"
    )

# Ensure tables exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']

        # Fetch all projects belonging to the logged-in user
        projects = Project.query.filter_by(User_id=user_id).all()

        # Prepare a list to store project details, including QuranVersions and Voices
        project_data = []
        
        for project in projects:
            quran_version = QuranVersions.query.get(project.quranversions_Version_id)
            voice = Voices.query.get(project.voice_id)
            
            project_data.append({
                "project_name": project.name,
                "quran_version": quran_version.name if quran_version else "Unknown",
                "language": quran_version.language if quran_version else "Unknown",
                "voice": voice.name if voice else "Unknown"
            })

        return render_template("Home.html", 
                            username=session.get('username', 'Guest'),
                            project_data=project_data)

    return redirect(url_for('sign_in'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("Sign_up.html")
    
    # If it's a POST request, check if it's JSON...
    data = {}
    if request.is_json:
        data = request.get_json()
    else:
        # ✅ Parse form data (application/x-www-form-urlencoded)
        data["first_name"] = request.form.get("name")
        data["username"] = request.form.get("username")
        data["email"] = request.form.get("email")
        data["password"] = request.form.get("password")
        data["confirm_password"] = request.form.get("confirm password")  # match the 'name' attribute

    # Now 'data' has the fields whether from JSON or form
    # Validate them just like before
    missing = [field for field in ["first_name", "username", "email", "password", "confirm_password"] if not data.get(field)]
    if missing:
        return jsonify({"message": f"Missing required fields: {', '.join(missing)}"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"message": "Passwords do not match!"}), 400

    # Check duplicates
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered!"}), 400
    if User.query.filter_by(Username=data["username"]).first():
        return jsonify({"message": "Username already registered!"}), 400

    hashed = generate_password_hash(data["password"], method='pbkdf2:sha256')

    new_user = User(
        first_name=data["first_name"],
        Username=data["username"],
        email=data["email"],
        password_hash=hashed,
        is_admin=False
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!", "redirect": url_for('sign_in')}), 201
    except Exception as e:
        db.session.rollback()
        print("Server Error:", str(e))
        return jsonify({"message": "Server error occurred."}), 500


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate presence
        if not email or not password:
            return jsonify({"message": "Please enter both email and password."}), 400

        # Look up user by email
        user = User.query.filter_by(email=email).first()

        # Check password
        if user and check_password_hash(user.password_hash, password):
            # Authentication success
            session['user_id'] = user.User_id
            # Use 'Username' from your model (capital U)
            session['username'] = user.Username

            # Return JSON with redirect URL (e.g., to your home route)
            return jsonify({"redirect": url_for('home')}), 200
        else:
            # Failed authentication
            return jsonify({"message": "Invalid email or password."}), 401

    # If GET, render your sign-in page
    return render_template("sign_in.html")


#@app.route('/add_project', methods=['GET', 'POST'])
#def add_project():
#    if 'user_id' in session:
#        if request.method == 'POST':
#            name = request.form.get('Projects.name')
#            Q_name = request.form.get('QuranVersions.name')
#            language = request.form.get('language')
#            asd
#            new_project = Projects()

@app.route('/create_project', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    project_name = request.form.get('Project_name')
    selected_version_id = request.form.get('version_id')
    selected_language = request.form.get('language')
    
    if not project_name or not selected_version_id or not selected_language:
        return jsonify({"message": "All fields are required!"}), 400

    try:
        new_project = Projects(User_id=session['user_id'],
        name=project_name,
        Version_id=selected_version_id,  
        language = selected_language )
        db.session.add(new_project)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print("Error creating project:", str(e))
        return jsonify({"message": "Error creating project", "error": str(e)}), 500
    
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True)

