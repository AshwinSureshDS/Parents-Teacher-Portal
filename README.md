# Tiny Wonders Service Learning Web Application

A web application for managing service learning activities at Tiny Wonders School. The app features user authentication, teacher and parent portals, and database integration using Flask and SQLite.

## Features
- User authentication (login, sign-up, password reset)
- Teacher and parent portals
- Dynamic home page
- SQLite database integration
- Responsive UI with HTML templates

## Project Structure
```
├── app.py
├── altertable.py
├── makecontacttable.py
├── makemarkstable.py
├── makenoticetable.py
├── maketeacherstable.py
├── maketimetabletable.py
├── tiny_wonders.db
├── static/
│   └── images/
├── templates/
│   ├── home_page.html
│   ├── login.html
│   ├── sign_up.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   └── ...
```

## Getting Started

1. **Clone the repository:**
   ```powershell
   git clone <repository-url>
   cd <repository-folder>
   ```
2. **Install dependencies:**
   Ensure you have Python 3.x and Flask installed.
   ```powershell
   pip install flask
   ```
3. **Run the application:**
   ```powershell
   python app.py
   ```
4. **Access the app:**
   Open your browser and go to `http://localhost:5000`

## License
This project is for educational purposes at Tiny Wonders School.
