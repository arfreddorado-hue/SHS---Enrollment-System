from database.db_config import db_config

def seed_program():
    conn = db_config()
    try:
        with conn.cursor() as cursor:
            select_program_query = "SELECT * FROM `program`"
            cursor.execute(select_program_query)
            program_data = cursor.fetchall()

            # Do nothing if program table has records
            if len(program_data) != 0:
                return

            # Save programs to the database if program table has no records
            programs = [
                {
                    "id": 1,
                    "name": "HUMSS",
                },
                {
                    "id": 2,
                    "name": "STEM",
                },
                {
                    "id": 3,
                    "name": "ABM",
                },
                {
                    "id": 4,
                    "name": "TVL",
                }
            ]

            for program in programs:
                sql = "INSERT INTO `program` (`id`, `name`) VALUES (%s, %s)"
                cursor.execute(sql, (program['id'], program['name']))
                print("Programs has been inserted!")

        conn.commit()
    except Exception as e:
        print("Failed to insert data into programs table:", e)
    finally:
        conn.close()