from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "StudentCourses.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    selection = request.form.get("selection", "")

    if selection == "Students":
        query = "SELECT StudentID, FirstName, LastName, Major FROM Students"
    elif selection == "Courses":
        query = "SELECT CourseID, CourseName, Instructor, Credits FROM Courses"
    elif selection == "Enrollments":
        query = "SELECT EnrollmentID, StudentID, CourseID, Semester, Grade FROM Enrollments"
    else:
        return "Invalid selection"

    print("DB path =>", DB_PATH, "exists?", os.path.exists(DB_PATH))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [d[0] for d in cur.description]
    conn.close()

    return render_template("result.html", colnames=colnames, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
