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

    if selection == "Report1":
        query = """
            SELECT
                ap.MajorProgramCode AS MajorCode,
                ap.ProgramName      AS MajorName,
                COUNT(s.StudentID)  AS StudentCount
            FROM AcademicProgram ap
            JOIN Student s
                ON s.MajorProgramCode = ap.MajorProgramCode
            GROUP BY ap.MajorProgramCode, ap.ProgramName
            ORDER BY StudentCount DESC;
        """
    elif selection == "Report2":
        query = """SELECT
    AcademicLevel,
    AVG(CumulativeGPA) AS AvgGPA
FROM Student
GROUP BY AcademicLevel
HAVING AVG(CumulativeGPA) >= 3.0
ORDER BY AvgGPA DESC;"""
    elif selection == "Report3":
        query = """SELECT
    um.MemberID,
    um.FirstName,
    um.LastName,
    s.StudentID
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE um.LastName LIKE 'C%';"""
    elif selection == "Report4":
        query = """SELECT
    s.StudentID,
    um.FirstName,
    um.LastName,
    s.CumulativeGPA
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.CumulativeGPA BETWEEN 2.50 AND 3.50
ORDER BY s.CumulativeGPA DESC;"""
    elif selection == "Report5":
        query = """SELECT
    s.StudentID,
    um.FirstName,
    um.LastName,
    s.MajorProgramCode
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.MajorProgramCode IN ('MIS', 'CS', 'FIN')
ORDER BY s.MajorProgramCode, um.LastName, um.FirstName;"""
    elif selection == "Report6":
        query = """SELECT
    s.StudentID,
    um.FirstName,
    um.LastName
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.StudentID NOT IN (
    SELECT sh.StudentID
    FROM StudentHold sh
    WHERE sh.ActiveFlag = 'Y'
)
ORDER BY s.StudentID;"""
    elif selection == "Report7":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName,
    ap.ProgramName                      AS MajorName
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
JOIN AcademicProgram ap
    ON s.MajorProgramCode = ap.MajorProgramCode;"""
    elif selection == "Report8":
         query = """SELECT
    um.FirstName || ' ' || um.LastName AS StudentName,
    c.CourseID,
    c.Title                            AS CourseTitle,
    t.Name                             AS Term,
    e.FinalGrade
FROM Enrollment e
JOIN Student s
    ON e.StudentID = s.StudentID
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
JOIN Section sec
    ON e.SectionID = sec.SectionID
JOIN Course c
    ON sec.CourseID = c.CourseID
JOIN Term t
    ON sec.TermID = t.TermID
ORDER BY t.TermID, c.CourseID, StudentName;"""
    elif selection == "Report9":
        query = """SELECT
    s.StudentID,
    stu_um.FirstName || ' ' || stu_um.LastName AS StudentName,
    aa.AdvisorID,
    adv_um.FirstName || ' ' || adv_um.LastName AS AdvisorName
FROM Student s
JOIN UniversityManager stu_um
    ON s.MemberID = stu_um.MemberID
LEFT JOIN AdvisorAssignment aa
    ON aa.StudentID = s.StudentID
   AND aa.AssignedEndDate IS NULL
LEFT JOIN Advisor adv
    ON aa.AdvisorID = adv.AdvisorID
LEFT JOIN UniversityManager adv_um
    ON adv.MemberID = adv_um.MemberID
ORDER BY StudentName;"""
    elif selection == "Report10":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName,
    e.SectionID,
    e.FinalGrade
FROM Student s, Enrollment e, UniversityManager um
WHERE s.StudentID = e.StudentID
  AND s.MemberID  = um.MemberID;"""
    elif selection == "Report11":
        query = """SELECT
    c.CourseID,
    c.Title                      AS CourseTitle,
    c.PrereqID,
    p.Title                      AS PrereqTitle
FROM Course c
LEFT JOIN Course p
    ON c.PrereqID = p.CourseID
ORDER BY c.CourseID;"""
    elif selection == "Report12":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName,
    s.MajorProgramCode,
    s.CumulativeGPA
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.CumulativeGPA >
      (
        SELECT AVG(s2.CumulativeGPA)
        FROM Student s2
        WHERE s2.MajorProgramCode = s.MajorProgramCode
      )
ORDER BY s.MajorProgramCode, s.CumulativeGPA DESC;"""
    elif selection == "Report13":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName,
    s.CumulativeGPA
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.CumulativeGPA >
      (SELECT AVG(CumulativeGPA) FROM Student)
ORDER BY s.CumulativeGPA DESC;"""
    elif selection == "Report14":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE EXISTS (
    SELECT 1
    FROM StudentHold sh
    WHERE sh.StudentID = s.StudentID
      AND sh.ActiveFlag = 'Y'
);"""
    elif selection == "Report15":
        query = """SELECT
    c.CourseID,
    c.Title
FROM Course c
WHERE NOT EXISTS (
    SELECT 1
    FROM Section sec
    WHERE sec.CourseID = c.CourseID
      AND sec.TermID  = 2
);"""
    elif selection == "Report16":
        query = """SELECT
    um.MemberID,
    um.FirstName || ' ' || um.LastName AS PersonName,
    'Student'                           AS Role
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID

UNION

SELECT
    um.MemberID,
    um.FirstName || ' ' || um.LastName AS PersonName,
    'Advisor'                           AS Role
FROM Advisor a
JOIN UniversityManager um
    ON a.MemberID = um.MemberID
ORDER BY PersonName;"""
    elif selection == "Report17":
        query = """SELECT
    s.StudentID,
    um.FirstName || ' ' || um.LastName AS StudentName,
    s.AcademicStanding,
    s.TotalCredits
FROM Student s
JOIN UniversityManager um
    ON s.MemberID = um.MemberID
WHERE s.AcademicStanding = 'Disqualified'
   OR (s.AcademicStanding = 'Probation' AND s.TotalCredits > 60)
ORDER BY s.AcademicStanding, s.TotalCredits DESC;
"""
    elif selection == "Report18":
        query = """SELECT
    sec.SectionID,
    c.CourseID,
    c.Title AS CourseTitle,
    COUNT(e.StudentID) AS EnrolledCount
FROM Section sec
JOIN Course c
    ON sec.CourseID = c.CourseID
LEFT JOIN Enrollment e
    ON e.SectionID = sec.SectionID
GROUP BY sec.SectionID, c.CourseID, c.Title
HAVING COUNT(e.StudentID) >= 1
ORDER BY EnrolledCount DESC;"""
    elif selection == "Report19":
        query = """SELECT
    sec.SectionID,
    c.CourseID,
    c.Title          AS CourseTitle,
    sec.MeetingDateStart,
    sec.MeetingDateEnd
FROM Section sec
JOIN Course c
    ON sec.CourseID = c.CourseID
WHERE sec.MeetingDateStart <= '2025-12-31'
  AND sec.MeetingDateEnd   >= '2025-01-01'
ORDER BY sec.MeetingDateStart;"""
    elif selection == "Report20":
        query = """SELECT
    sec.SectionID,
    c.CourseID || '-' || sec.SectionNumber AS SectionLabel,
    sgi.ItemNo,
    sgi.ItemName,
    sgi.WeightPercentage AS WeightPct
FROM SectionGradedItem sgi
JOIN Section sec
    ON sgi.SectionID = sec.SectionID
JOIN Course c
    ON sec.CourseID = c.CourseID
ORDER BY sec.SectionID, sgi.ItemNo;"""
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

