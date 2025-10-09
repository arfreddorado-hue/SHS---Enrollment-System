from database.db_config import db_config

def save_account(full_name, gender, age, contact_number, program, email_address, password, profile_picture, student_id_num):
    db = db_config()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO students (`full_name`, `gender`,`age`,`contact_number`, `program_id`, `email_address`, `password`, `profile_picture`, `student_id_num`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            rows_affected = cursor.execute(sql, (full_name, gender, age, contact_number, program, email_address, password, profile_picture, student_id_num))
        db.commit()

        if rows_affected == 1:
            print("Student account saved successfully!")
            return True
        return False
    except Exception as e:
        print("Failed to insert data into people table:", e)
        return False
    finally:
        db.close()
