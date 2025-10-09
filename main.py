from pages.admin_dashboard import admin_dashboard
from pages.login_page import login_page
from pages.signup_page import signup_page
from pages.adminlogin_page import adminlogin_page
from pages.studentlogin_page import studentlogin_page
from pages.practice import practice
from pages.student_dashboard import student_dashboard
from database.db_config import db_config
from database.seeder import seed_program
from services.program_service import get_programs


def main():     
    try:
        conn = db_config()
        seed_program()
        get_programs()
        conn.close()
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)

    login_page()
if __name__ == "__main__":
    main()