import os
import requests 
import json
import sqlite3 
from flask import Flask, render_template, redirect, url_for, request, session, flash, get_flashed_messages
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Configure server-side sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Check if SECRET_KEY was loaded. This is a good safety check.
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set. Set it as an environment variable or in a .env file.")


app.config['DEBUG'] = os.getenv('FLASK_DEBUG') == 'True' 

def get_db():
    conn = sqlite3.connect("vocabvault.db")
    conn.row_factory = sqlite3.Row  # enables name-based access
    return conn

@app.template_filter("loads")
def json_loads_filter(s):
    return json.loads(s)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        if not username or not password or not confirmation:
            flash("All fields are required")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords don't match.")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username already taken.")
            return redirect("/register")
        finally:
            db.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Please fill out both fields.")
            return redirect("/login")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            flash("Invalid username or password.")
            return redirect("/login")

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("user_id"):
        return redirect("/login")

    db = get_db()
    folders = db.execute("""
        SELECT folders.id, folders.name, folders.created_at, COUNT(saved_words.id) AS word_count
        FROM folders
        LEFT JOIN saved_words ON folders.id = saved_words.folder_id
        WHERE folders.user_id = ?
        GROUP BY folders.id
        ORDER BY folders.created_at DESC -- Added ordering for consistency
    """, (session["user_id"],)).fetchall() # Added ordering for consistency

    
    if request.method == "POST":
        word = request.form.get("word")
        # (You can add logic to look up the word here if needed)
        db.close()
        return render_template("index.html", folders=folders, word=word)

    db.close()
    return render_template("index.html", folders=folders)


@app.route("/search", methods=["POST"])
def search():
    if not session.get("user_id"):
        return redirect("/login")

    word = request.form.get("word")
    if not word:
        flash("Please enter a word.")
        return redirect("/")

    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code != 200:
        flash("Word not found.")
        return redirect("/")

    data = response.json()

    definitions = []

    # Loop through all entries returned by the API
    for entry in data:
        for meaning in entry.get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "")
            for d in meaning.get("definitions", []):
                example = d.get("example", "")
                # ✅ Check if the example contains the searched word
                if example and word.lower() in example.lower():
                    definitions.append({
                        "part_of_speech": part_of_speech,
                        "definition": d["definition"],
                        "example": example
                    })

    if not definitions:
        flash("No definitions with relevant examples found.")
        return redirect("/")

    result = {
        "word": word,
        "meanings": definitions
    }

    # Load folders for dropdown
    db = get_db()
    folders = db.execute("""
        SELECT folders.id, folders.name, folders.created_at, COUNT(saved_words.id) AS word_count
        FROM folders
        LEFT JOIN saved_words ON folders.id = saved_words.folder_id
        WHERE folders.user_id = ?
        GROUP BY folders.id
    """, (session["user_id"],)).fetchall()
    db.close()

    return render_template("index.html", result=result, folders=folders)

@app.route("/add-folder", methods=["POST"])
def add_folder():
    
    if not session.get("user_id"):
        return redirect("/login")

    folder_name = request.form.get("folder_name")

    if not folder_name:
        flash("Folder name required.")
        return redirect("/")

    db = get_db()
    db.execute("INSERT INTO folders (user_id, name) VALUES (?, ?)", (session["user_id"], folder_name))
    db.commit()
    db.close()

    flash(f"Folder '{folder_name}' created!")
    return redirect("/")

@app.route("/folder/<int:folder_id>")
def folder(folder_id):
    if not session.get("user_id"):
        return redirect("/login")

    db = get_db()

    folder = db.execute("SELECT * FROM folders WHERE id = ? AND user_id = ?",(folder_id, session["user_id"])).fetchone()
    if not folder:
        flash("Folder not found.")
        return redirect("/")

    words = db.execute("""
        SELECT * FROM saved_words
        WHERE folder_id = ? AND user_id = ?
        ORDER BY created_at DESC
    """, (folder_id, session["user_id"])).fetchall()

    # Convert JSON definitions in Python
    processed_words = []
    for word in words:
        definitions = json.loads(word["definitions"])
        processed_words.append({
            "id": word["id"],
            "word": word["word"],
            "definitions": definitions,
            "created_at": word["created_at"]
        })

    db.close()
    return render_template("folder.html", folder=folder, words=processed_words)

@app.route("/save", methods=["POST"])
def save_word():
    if not session.get("user_id"):
        return redirect("/login")

    word = request.form.get("word")
    folder_id = request.form.get("folder_id")
    definitions_raw = request.form.get("definitions")

    print("Raw definitions from form:", definitions_raw) #debug line

    # Basic validation
    try:
        definitions = json.loads(definitions_raw)  # Parse to check it’s valid
        definitions_json = json.dumps(definitions) # Convert it back to clean JSON
    except Exception as e:
        print("Error parsing JSON:", e)
        flash("Could not save word. Try again.")
        return redirect("/")

    if not word or not definitions_json or not folder_id:
        flash("Missing data.")
        return redirect("/")

    db = get_db()
    db.execute("""
        INSERT INTO saved_words (user_id, folder_id, word, definitions)
        VALUES (?, ?, ?, ?)
    """, (session["user_id"], folder_id, word, definitions_json))
    db.commit()
    db.close()

    flash(f'"{word}" saved successfully!')
    return redirect("/")

@app.route("/delete-word/<int:word_id>", methods=["POST"])
def delete_word(word_id):
    if not session.get("user_id"):
        return redirect("/login")

    db = get_db()

    # Verify ownership
    word = db.execute("SELECT * FROM saved_words WHERE id = ? AND user_id = ?", (word_id, session["user_id"])).fetchone()
    if word:
        db.execute("DELETE FROM saved_words WHERE id = ?", (word_id,))
        db.commit()
        flash(f'"{word["word"]}" deleted.')
    else:
        flash("Word not found or unauthorized.")

    db.close()
    return redirect(request.referrer or "/")

@app.route("/rename-folder/<int:folder_id>", methods=["POST"])
def rename_folder(folder_id):
    if not session.get("user_id"):
        return redirect("/login")

    new_name = request.form.get("new_name")
    if new_name:
        db = get_db()
        db.execute("UPDATE folders SET name = ? WHERE id = ? AND user_id = ?", (new_name, folder_id, session["user_id"]))
        db.commit()
        db.close()
        flash("Folder renamed.")
    return redirect("/")

@app.route("/delete-folder/<int:folder_id>", methods=["POST"])
def delete_folder(folder_id):
    if not session.get("user_id"):
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM saved_words WHERE folder_id = ? AND user_id = ?", (folder_id, session["user_id"]))
    db.execute("DELETE FROM folders WHERE id = ? AND user_id = ?", (folder_id, session["user_id"]))
    db.commit()
    db.close()

    flash("Folder and its contents deleted.")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)