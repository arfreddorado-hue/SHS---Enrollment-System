from database.db_config import db_config

def get_programs():
    db = db_config()

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM program")
            programs = cursor.fetchall()

            prog_names = []
            for program in programs:
                prog_names.append(program)

        return prog_names
    except Exception as e:
        print("Failed to fetch programs from program table:", e)
    finally:
        db.close()
