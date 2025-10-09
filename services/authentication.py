from database.db_config import db_config

def authenticate(student_id_num, password):
    """
    Authenticate student and return their full data including subjects
    Returns student data dict if authenticated, None otherwise
    """
    db = db_config()
    try:
        with db.cursor() as cursor:
            sql = """
                  SELECT s.id,
                         s.full_name,
                         s.email_address,
                         s.profile_picture,
                         s.gender,
                         s.age,
                         s.contact_number,
                         s.student_id_num,
                         s.program_id,
                         s.approval_status
                        
                  FROM students s
                  LEFT JOIN program p ON s.program_id = p.id
                  WHERE TRIM(s.student_id_num) = %s
                    AND TRIM(s.password) = %s
                  """
            cursor.execute(sql, (student_id_num.strip(), password.strip()))
            student = cursor.fetchone()

            if not student:
                return None

            student_data = {
                'id': student.get('id'),
                'full_name': student.get('full_name'),
                'gender': student.get('gender'),
                'age': student.get('age'),
                'contact_number': student.get('contact_number'),
                'program_id': student.get('program_id'),
                'email_address': student.get('email_address'),
                'profile_picture': student.get('profile_picture'),
                'student_id_num': student.get('student_id_num'),
                'approval_status': student.get('approval_status')
            }

            return student_data
    except Exception as e:
        print('Unable to login:', e)
        return None
    finally:
        db.close()
