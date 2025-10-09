from database.db_config import db_config

def fetch_students():
    db = db_config()
    try:
        with db.cursor() as cursor:
            cursor.execute("""SELECT * FROM students""")
            student_data = cursor.fetchall()
        return student_data
    except Exception as e:
        print("Error fetching students data", e)
        return None
    finally:
        db.close()

def approve_student_request(id):
    db = db_config()
    try:
        with db.cursor() as cursor:
            cursor.execute("""SELECT full_name FROM students WHERE id = %s""", (id,))
            found_student = cursor.fetchone()

            if found_student:
                cursor.execute("""UPDATE students SET approval_status = 'approved' WHERE id = %s""", (id,))

        db.commit()
        return found_student
    except Exception as e:
        print("Error fetching students data", e)
        return None
    finally:
        db.close()

def reject_student_approval(id):
    db = db_config()
    try:
        with db.cursor() as cursor:
            cursor.execute("""SELECT full_name FROM students WHERE id = %s""", (id,))
            found_student = cursor.fetchone()

            if found_student:
                cursor.execute("""UPDATE students SET approval_status = 'rejected' WHERE id = %s""", (id,))

        db.commit()
        return found_student
    except Exception as e:
        print("Error fetching students data", e)
        return None
    finally:
        db.close()