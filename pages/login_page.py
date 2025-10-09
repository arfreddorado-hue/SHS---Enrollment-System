import tkinter as tk
from utils import display_background, make_layout, make_icon

def login_page():
    root = tk.Tk()
    make_layout(root)
    display_background(root)
    bg_color = '#800000'

    # icons
    rounded_stud_icon = make_icon("C:/Users/User/Downloads/graduated.png")
    rounded_admin_icon = make_icon("C:/Users/User/Downloads/admin.png")
    rounded_addStudent_icon = make_icon("C:/Users/User/Downloads/add_student.png")
    rounded_locked_icon = make_icon("C:/Users/User/Downloads/locked.png")

    # mini window
    root.title("SHS - Enrollment System")
    welcome_page_fm = tk.Frame(root, highlightbackground='maroon', highlightthickness=3, background='white')
    heading_lb = tk.Label(
        welcome_page_fm, text="Login",
        bg=bg_color, fg="white",
        font=("Bold", 22), width=100
    )
    heading_lb.place(relx=0.5, y=0, anchor='n')

    login_frame = tk.Frame(welcome_page_fm, bg="white")

    def go_to_student_login():
        root.destroy()
        from pages.studentlogin_page import studentlogin_page
        studentlogin_page()

    def go_to_admin_login():
        root.destroy()
        from pages.adminlogin_page import adminlogin_page
        adminlogin_page()

    def go_to_signup():
        root.destroy()
        from pages.signup_page import signup_page
        signup_page()

    # helper for rows (arranges)
    def add_row(frame, icon, text, command):
        row = tk.Frame(frame, bg="white")
        row.pack(pady=15)

        tk.Label(row, image=icon, bg="white").pack(side="left", padx=10)

        btn = tk.Button(
            row, text=text,
            bg=bg_color, fg="white",
            font=("Bold", 12), bd=0,
            width=15,  # makes all same width
            height=2,
            command=command  # Passes the command to the button
        )
        btn.pack(side="left", padx=10)

    # rows
    add_row(login_frame, rounded_stud_icon, "Login Student", command=go_to_student_login)
    add_row(login_frame, rounded_admin_icon, "Login Admin", command=go_to_admin_login)
    add_row(login_frame, rounded_addStudent_icon, "Create Account", command=go_to_signup)

    # Place frame in the middle
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # window config
    parent = welcome_page_fm.master
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    welcome_page_fm.grid(row=0, column=0)
    welcome_page_fm.grid_propagate(False)
    welcome_page_fm.configure(width=320, height=400)

    root.mainloop()