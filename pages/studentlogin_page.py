import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
from utils import display_background, make_layout, make_icon
from services.authentication import authenticate
from pages.student_dashboard import student_dashboard

def studentlogin_page():
    root = tk.Tk()
    root.title("SHS - Enrollment System")
    make_layout(root)
    display_background(root)
    bg_color = '#800000'

    # Icons
    rounded_stud_icon = tk.PhotoImage(file="C:/Users/User/Downloads/login_student_img.png")
    locked_icon = tk.PhotoImage(file="C:/Users/User/Downloads/locked.png")
    unlocked_icon = tk.PhotoImage(file="C:/Users/User/Downloads/unlocked.png")

    # Main frame
    studentlogin_frame = tk.Frame(root, highlightbackground='maroon', highlightthickness=3, background='#F0F0F0')
    heading_lb = tk.Label(
        studentlogin_frame,
        text="Login",
        bg=bg_color, fg="white",
        font=("Bold", 22), width=100
    )
    heading_lb.place(relx=0.5, y=0, anchor='n')

    # Back button
    def go_back():
        root.destroy()
        from pages.login_page import login_page
        login_page()

    back_btn = tk.Button(studentlogin_frame, text=" ↩", font=('Arial Bold', 12),
                         bg='lightgray', fg='black', command=go_back, bd=0)
    back_btn.place(x=5, y=5, width=50, height=20)

    studentlogin_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Student icon
    student_icon_lb = tk.Label(studentlogin_frame, image=rounded_stud_icon)
    student_icon_lb.place(x=135, y=40)

    # ID number label and entry
    id_number_lb = tk.Label(studentlogin_frame, text='Enter Student ID number: ',
                            font=("Bold", 10), fg=bg_color)
    id_number_lb.place(x=80, y=140)

    id_number_entry = tk.Entry(studentlogin_frame, font=('Bold', 12),
                               justify=tk.CENTER, highlightcolor=bg_color, highlightbackground="gray",
                               highlightthickness=2)
    id_number_entry.place(x=80, y=165)

    # Password label and entry
    password_lb = tk.Label(studentlogin_frame, text='Enter Student password: ',
                           font=("Bold", 10), fg=bg_color)
    password_lb.place(x=80, y=240)

    password_entry = tk.Entry(studentlogin_frame, font=('Bold', 12),
                              justify=tk.CENTER, highlightcolor=bg_color, highlightbackground="gray",
                              highlightthickness=2, show='*')
    password_entry.place(x=80, y=265)

    # Show/hide password function
    def show_hide_password():
        if password_entry['show'] == '*':
            password_entry.configure(show='')
            show_hide_button.config(image=unlocked_icon)
        else:
            password_entry.configure(show='*')
            show_hide_button.config(image=locked_icon)

    # Authenticate user function
    def authenticate_user():
        student_id = id_number_entry.get().strip()
        password = password_entry.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Student ID number is required.")
            return

        if not password:
            messagebox.showerror("Error", "Password is required.")
            return

        # Authenticate and get full student data
        student_data = authenticate(student_id, password)

        if student_data:  # dict is truthy if authentication succeeded
            root.destroy()
            # Pass student data to dashboard
            student_dashboard(student_data)
        else:
            messagebox.showwarning("Warning", "Student ID or password is incorrect. Please try again.")

    # Show/hide password button
    show_hide_button = tk.Button(studentlogin_frame, image=locked_icon, bd=0, command=show_hide_password)
    show_hide_button.place(x=270, y=250)

    # Login button
    login_btn = tk.Button(studentlogin_frame, text="Login", font=('Bold', 12), bg=bg_color, fg="white",
                          command=authenticate_user)
    login_btn.place(x=174, y=340, width=150, height=30, anchor="center")

    # Forget password button (non-functional placeholder)
    forget_password_btn = tk.Button(studentlogin_frame, text='⚠\nForget Password?',
                                    fg=bg_color, bd=0)
    forget_password_btn.place(x=174, y=380, width=120, height=30, anchor="center")

    # Window configuration
    parent = studentlogin_frame.master
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    studentlogin_frame.grid(row=0, column=0)
    studentlogin_frame.grid_propagate(False)
    studentlogin_frame.configure(width=350, height=420)

    root.mainloop()
