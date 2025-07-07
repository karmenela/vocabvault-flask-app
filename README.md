# 🗝 VocabVault: Your personal vault of words
#### Video Demo:  <https://youtu.be/01unCEzwO5M>
## Description:

**VocabVault** VocabVault is a dynamic web application designed to help users expand and organize their vocabulary. It serves as a smart dictionary where users can look up words, view their definitions and relevant examples, and then save these words into personalized folders for later review. This project was developed as the final project for CS50x, Harvard University's Introduction to Computer Science, demonstrating proficiency in web development principles, database management, and API integration.

The primary motivation behind VocabVault was to create a practical tool that goes beyond a simple dictionary. By allowing users to curate their own vocabulary lists within custom folders, it transforms passive word lookup into an active learning experience. This application aims to provide a seamless and intuitive interface for language learners, writers, or anyone looking to systematically improve their lexicon. It's built with Python's Flask framework, ensuring a lightweight yet powerful backend, complemented by a responsive frontend for an optimal user experience across devices.

🔗 **Live App:** [https://vocabvault-flask-app.onrender.com](https://vocabvault-flask-app.onrender.com)

---

## ✨ Features

- **User Authentication**: Secure registration, login, and logout to manage individual user accounts.
- **Word Search**: Search any English word via an external dictionary API to retrieve definitions and parts of speech.
- **Example-Based Filtering**: Only shows definitions with clear example sentences to support better understanding.
- **Vocabulary Folder Management**: Create, rename, and delete folders to organize saved words by topic, difficulty, or custom categories.
- **Word Saving**: Save searched words with their definitions and examples into selected folders.
- **Word Deletion**: Easily remove saved words when no longer needed.
- **User Profile Indicator**: Navbar displays a profile icon that shows the logged-in user's username on hover.
- **Live Web Deployment**: Fully deployed on Render, accessible via any internet-connected browser.
- **macOS Desktop Application**: A standalone desktop wrapper (via Nativefier) enables local desktop access to the web app.

---

## ⚙️ Technologies

### 🧠 Backend

- **Python**: The core programming language for the application logic.
- **Flask**: A lightweight Python web framework, providing the foundation for routes, requests, and responses.
- **Gunicorn**: A production-ready WSGI HTTP server used to run the Flask application efficiently on Render.
- **Flask-Session**: Manages server-side sessions to maintain user login states securely.
- **Werkzeug**: A comprehensive WSGI utility library, a core dependency of Flask.
- **Requests**: An elegant and simple HTTP library for making API calls (e.g., to the Dictionary API).
- **python-dotenv**: Used for loading environment variables from a `.env` file during local development, ensuring sensitive information is kept out of the codebase.

### 🗃️ Database

- **SQLite3**: A lightweight, file-based relational database used for storing user accounts, vocabulary folders, and saved words. Ideal for its simplicity and ease of setup.

### 🎨 Frontend

- **HTML5**: Structures the content of the web pages.
- **CSS3**: Styles the application, providing a clean and modern aesthetic.
- **Bootstrap 5**: A popular CSS framework used for responsive design and pre-built UI components, ensuring a mobile-friendly and visually appealing layout.
- **Jinja2**: Flask's default templating engine, used for rendering dynamic HTML content.
- **Font Awesome**: Provides scalable vector icons for a consistent visual language within the UI.

### 🌐 APIs

- **Dictionary API** ([dictionaryapi.dev](https://dictionaryapi.dev)): An external RESTful API used to fetch word definitions, parts of speech, and examples.

### 🚀 Deployment & Tools

- **Render**: Cloud platform used for live hosting and continuous deployment of the Flask web application from GitHub.
- **Git & GitHub**: Version control system for collaborative development and code hosting.
- **Nativefier**: A Node.js tool used to wrap the live web application into a standalone macOS desktop application.

---

## 🗂️ File Structure Overview

```plaintext
app.py             # Core Flask app with all routes and logic
init_db.py         # Sets up users, folders, saved_words tables
vocabvault.db      # SQLite database for user and word data

templates/
├── index.html         # Dashboard after login
├── folder.html        # View words in a specific folder
├── login.html         # User login
├── register.html      # User registration
├── layout.html        # Base layout for logged-in users
└── auth_layout.html   # Layout for auth pages

static/
└── styles.css         # Custom styling

.flask_session/        # Stores server-side session data
.env                   # Environment variables (SECRET_KEY, etc.)
.gitignore             # Excludes .env, __pycache__, etc.
Procfile               # Render deployment config
requirements.txt       # Python dependencies
```

---

## 🧠 Key Design Choices & Rationales

Throughout the development of VocabVault, several intentional design decisions were made, often reflecting trade-offs and educational goals aligned with CS50x.

### 🔧 Flask Framework (CS50x Context)

**Decision**: Flask was selected for its lightweight, flexible nature—ideal for learning web development fundamentals. As a microframework, it offers hands-on exposure to routing, request handling, templating, and WSGI, without the complexity of full-stack frameworks like Django.

---

### 🖋️ Templating Engine: Jinja2

**Decision**: Jinja2 was used due to its tight integration with Flask and intuitive syntax. It enables embedding logic into HTML templates, allowing dynamic rendering while keeping the presentation separate from backend logic—an important concept taught in CS50x.

---

### 🗃️ Database: SQLite3

**Decision**: SQLite3 was chosen for its simplicity and file-based architecture. For a course project, it removed the need for server setup, allowing focus on learning SQL and practicing relational database interactions in a self-contained environment.

---

### 🔐 Environment Variable Management

**Debate**: Hardcoded credentials vs. environment variables  
**Decision**: `python-dotenv` was used to manage sensitive variables like `SECRET_KEY`. This aligns with security best practices and allows the same codebase to run in both development and production without exposing secrets.

---

### 🚀 Production Server: Gunicorn

**Debate**: Flask’s built-in dev server vs. a WSGI production server  
**Decision**: Gunicorn was used for deployment on Render. Unlike Flask’s development server, Gunicorn is capable of handling concurrent requests and is designed for production, ensuring a stable live deployment.

---

### 🎨 UI Design & Theme

**Decision**: The UI was designed to be clean, responsive, and slightly “magical” to reflect the app's educational nature. Bootstrap 5 provided a solid foundation for responsiveness and layout, with customizations layered on top for personality and usability.

- **Color Palette**: Soft, calm colors improve readability and maintain focus. Bootstrap’s primary blue is used for CTAs, while light backgrounds reduce eye strain.
- **Accessibility**: Flash messages and buttons are color-coded using Bootstrap's alert system.
- **User-Centric Flow**: Features like collapsible cards, folder organization, and a profile hover icon enhance clarity and engagement.

---

### 🌐 API Integration: Dictionary API

**Decision**: [dictionaryapi.dev](https://dictionaryapi.dev) was selected for its clean RESTful design and reliable data. Integration with Python's `requests` library was seamless. Filtering logic was added to prioritize definitions that include example sentences, improving usefulness for learners.

---

### 🗂️ Session Management: Flask-Session

**Decision**: Flask-Session stores sessions on the server side, enhancing security compared to storing session data in browser cookies. This helps protect user login data and prevents tampering.

---

## ☁️ Deployment Strategy

### Render

- **Decision**: Render was chosen for its ease of deployment and GitHub integration. It automatically rebuilds and redeploys the app upon commits, enabling continuous deployment with minimal configuration.

### UptimeRobot

- **Decision**: UptimeRobot was integrated to keep the Render-hosted app awake and available. It pings the app every 5 minutes and alerts on downtime, ensuring a more reliable demo experience.

---

### 🖥️ Nativefier (macOS Desktop App)

**Debate**: Native Python-based app vs. web wrapper  
**Challenges**: Using tools like PyInstaller and PyWebView introduced dependency issues—especially with libraries like Pillow and NumPy on pre-release Python versions.

**Decision**: Switched to Nativefier for a quick and robust solution. It wraps the deployed web app into a macOS-compatible desktop shell.

**Implication**: While the result isn’t offline-capable, it provides a polished desktop experience for demonstration and use, fulfilling project goals within deadline constraints.

---

## 🎨 UI & UX Considerations

* **Design Theme**: A clean and calming aesthetic that supports long-term use without fatigue.
* **Card-Based Display**: Words are shown in collapsible cards for readability.
* **Responsive Design**: Layout adapts seamlessly across screen sizes via Bootstrap.
* **Hover Feedback**: Navbar icon shows logged-in username for personalization.
* **Minimalist Approach**: Visual simplicity encourages focus on content.
* **Alert Messages**: Alert messages that dissapear after 20 seconds by JavaScript's timer feature.

---

## 💻 Desktop Experience

Using **Nativefier**, the app is packaged as a macOS desktop wrapper. While it relies on an internet connection (as it simply loads the live web version), this approach avoids the complexity of bundling the full backend locally and ensures a native-like interface.

---

## 🚀 Deployment Details

* **Live Deployment**: Hosted on [Render](https://render.com) with continuous integration from GitHub.
* **Procfile**: Configures the app to run via Gunicorn in production.
* **Uptime Monitoring**: Services like UptimeRobot ensure app availability.

---

## 🔧 Setup Instructions

### Local Development

```bash
# Clone the repo
git clone https://github.com/karmenela/vocabvault-flask-app.git
cd vocabvault-flask-app

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up the database
python init_db.py

# Create and configure .env
touch .env
# Add:
# SECRET_KEY=your_random_string
# FLASK_DEBUG=True

# Run the app
python app.py
```

Access the app at `http://127.0.0.1:5000/`

---

## 📌 License

MIT License — Feel free to fork and build upon this project for educational or personal use.

---

## 🙌 Credits

* **Harvard CS50x** – For the foundational knowledge
* **dictionaryapi.dev** – For the free word data
* **Flask & Bootstrap teams** – For their powerful tools

---

Thank you for checking out **VocabVault**! 🌟 If you have feedback, ideas, or want to collaborate, feel free to open an issue or fork the project.
