import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from utils import display_background, make_layout, make_icon
from tkinter import messagebox
from pages.admin_dashboard import admin_dashboard

def adminlogin_page():
    root = tk.Tk()
    root.title("SHS - Enrollment System")
    make_layout(root)
    display_background(root)
    bg_color = '#800000'

    rounded_admin_icon = make_icon("C:/Users/User/Downloads/admin.png")
    locked_icon = tk.PhotoImage(file="C:/Users/User/Downloads/locked.png")
    unlocked_icon = tk.PhotoImage(file="C:/Users/User/Downloads/unlocked.png")

    root.rounded_admin_icon = rounded_admin_icon
    root.locked_icon = locked_icon
    root.unlocked_icon = unlocked_icon

    # new window
    adminlogin_frame = tk.Frame(root, highlightbackground='maroon', highlightthickness=3, background='#F0F0F0')
    heading_lb = tk.Label(adminlogin_frame,
                          text="Login",
                          bg=bg_color, fg="white",
                          font=("Bold", 22), width=100)
    heading_lb.place(relx=0.5, y=0, anchor='n')

    # ONLY ADDITION: Back button
    def go_back():
        root.destroy()
        from pages.login_page import login_page
        login_page()

    back_btn = tk.Button(adminlogin_frame, text=" ↩ ", font=('Arial Bold', 12),
                         bg='lightgray', fg='black', command=go_back, bd=0)
    back_btn.place(x=5, y=5, width=50, height=20)

    adminlogin_frame.place(relx=0.5, rely=0.5, anchor="center")

    # icon in the middle
    student_icon_lb = tk.Label(adminlogin_frame, image=root.rounded_admin_icon)
    student_icon_lb.place(x=150, y=60)

    id_number_lb = tk.Label(adminlogin_frame, text='Enter Username: ',
                            font=("Bold", 10), fg=bg_color)
    id_number_lb.place(x=80, y=140)

    # text box 1
    admin_username = tk.Entry(adminlogin_frame, font=('Bold', 12),
                               justify=tk.CENTER, highlightcolor=bg_color, highlightbackground="gray",
                               highlightthickness=2)
    admin_username.place(x=80, y=165)

    password_lb = tk.Label(adminlogin_frame, text='Enter Password: ',
                           font=("Bold", 10), fg=bg_color)
    password_lb.place(x=80, y=240)

    # text box 2
    admin_password = tk.Entry(adminlogin_frame, font=('Bold', 12),
                              justify=tk.CENTER, highlightcolor=bg_color, highlightbackground="gray",
                              highlightthickness=2, show='*')
    admin_password.place(x=80, y=265)

    # --- Show/Hide Password Function ---
    def show_hide_password():
        if admin_password['show'] == '*':
            admin_password.configure(show='')
            root.current_icon = unlocked_icon  # keep reference
            show_hide_button.config(image=root.current_icon)
        else:
            admin_password.configure(show='*')
            root.current_icon = locked_icon
            show_hide_button.config(image=root.current_icon)

    # --- Hides Password Button ---
    show_hide_button = tk.Button(adminlogin_frame, image=root.locked_icon, bd=0, command=show_hide_password)
    show_hide_button.place(x=270, y=250)

    def login_admin():
        if not admin_username.get():
            messagebox.showwarning('Error', 'Username is required')
            return
        
        if not admin_password.get():
            messagebox.showwarning('Error', 'Password is required')
            return

        if admin_username.get() != 'admin' and admin_password.get() != 'apedgwapo':
            messagebox.showwarning('Error', 'Incorrect email or password')
            return

        admin_data = {'name': 'Arfred Durado'}

        root.destroy()
        admin_dashboard(admin_data)

    login_btn = tk.Button(adminlogin_frame, text="Login", font=('Bold', 12), bg=bg_color, fg="white", command=login_admin)
    login_btn.place(x=174, y=340, width=150, height=30, anchor="center")

    forget_password_btn = tk.Button(adminlogin_frame, text='⚠\nForget Password?',
                                    fg=bg_color, bd=0)
    forget_password_btn.place(x=174, y=380, width=120, height=30, anchor="center")

    # window config
    parent = adminlogin_frame.master
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    adminlogin_frame.grid(row=0, column=0)
    adminlogin_frame.grid_propagate(False)
    adminlogin_frame.configure(width=350, height=420)

    root.mainloop()
