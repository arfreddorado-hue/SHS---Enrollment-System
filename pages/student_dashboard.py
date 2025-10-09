import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils import display_background, make_layout


def student_dashboard(student_data=None):
    root = tk.Tk()
    root.title("Student Dashboard - SHS Enrollment System")
    make_layout(root)
    display_background(root)
    bg_color = '#800000'

    # Main window frame
    dashboard_frame = tk.Frame(root, highlightbackground='maroon',
                               highlightthickness=3, background='white')

    # Header
    heading_lb = tk.Label(
        dashboard_frame,
        text=f"{student_data.get('grade_level')} & {student_data.get('section')}",
        bg=bg_color, fg="white",
        font=("Bold", 18)
    )
    heading_lb.pack(fill='x')

    # Adviser name
    adviser_lb = tk.Label(
        dashboard_frame,
        text=f"({student_data.get('adviser')})",
        bg=bg_color, fg="white",
        font=("Arial", 12)
    )
    adviser_lb.pack(fill='x')

    # Main content frame
    content_frame = tk.Frame(dashboard_frame, bg="white")
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Left side - Student Info
    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side='left', fill='y', padx=(0, 20))

    # Profile picture frame
    photo_frame = tk.Frame(left_frame, width=150, height=180, bg='lightgray',
                           highlightbackground='black', highlightthickness=2)
    photo_frame.pack(pady=10)
    photo_frame.pack_propagate(False)

    photo_label = tk.Label(photo_frame, bg='lightgray')
    photo_label.pack(fill='both', expand=True)

    # Load profile picture
    try:
        profile_pic_path = student_data.get('profile_picture')
        img = Image.open(profile_pic_path)

        # Resize to fit frame
        img.thumbnail((146, 176), Image.Resampling.LANCZOS)

        # Center image in frame
        final_img = Image.new('RGB', (146, 176), 'lightgray')
        x = (146 - img.width) // 2
        y = (176 - img.height) // 2
        final_img.paste(img, (x, y))

        photo = ImageTk.PhotoImage(final_img)
        photo_label.config(image=photo, bg='white')
        photo_label.image = photo
    except:
        photo_label.config(text="No Photo", font=("Arial", 12), fg='gray')

    # Student name
    name_label = tk.Label(
        left_frame,
        text=student_data.get('full_name'),
        font=("Bold", 14),
        bg="white",
        wraplength=150
    )
    name_label.pack(pady=(10, 5))

    # Student email
    email_label = tk.Label(
        left_frame,
        text=student_data.get('email_address'),
        font=("Arial", 10),
        bg="white",
        fg="gray",
        wraplength=150
    )
    email_label.pack(pady=(0, 15))

    # Status indicator
    status = student_data.get('approval_status')
    status_color = '#28a745' if status == 'approved' else '#ffc107'
    status_text = ''

    match status:
        case 'pending':
            status_text = 'PENDING'
        case 'approved':
            status_text = 'APPROVED'
        case 'rejected':
            status_text = 'REJECTED'

    status_label = tk.Label(
        left_frame,
        text=status_text,
        font=("Bold", 11),
        bg=status_color,
        fg="white",
        padx=10,
        pady=5
    )
    status_label.pack(pady=(0, 10))

    # Buttons
    edit_btn = tk.Button(
        left_frame,
        text="Edit Profile",
        font=('Arial', 11),
        bg='#800000',
        fg='white',
        command=lambda: edit_profile(student_data),
        width=15,
        bd=0,
        cursor='hand2'
    )
    edit_btn.pack(pady=5)

    dropout_btn = tk.Button(
        left_frame,
        text="Drop Out",
        font=('Arial', 11),
        bg='#dc3545',
        fg='white',
        command=lambda: drop_out(student_data),
        width=15,
        bd=0,
        cursor='hand2'
    )
    dropout_btn.pack(pady=5)

    logout_btn = tk.Button(
        left_frame,
        text="Logout",
        font=('Arial', 11),
        bg='#6c757d',
        fg='white',
        command=lambda: logout(root),
        width=15,
        bd=0,
        cursor='hand2'
    )
    logout_btn.pack(pady=5)

    # Right side - Subjects Table
    right_frame = tk.Frame(content_frame, bg="white")
    right_frame.pack(side='left', fill='both', expand=True)

    # Table header
    table_header = tk.Frame(right_frame, bg="white")
    table_header.pack(fill='x', pady=(0, 10))

    tk.Label(table_header, text="VIEW SUBJECTS ▼", bg='#800000', fg='white',
             font=("Bold", 11), width=20, anchor='w', padx=5).pack(side='left', fill='x', expand=True)
    tk.Label(table_header, text="SCHEDULE", bg='#800000', fg='white',
             font=("Bold", 11), width=20, anchor='w', padx=5).pack(side='left', fill='x', expand=True)
    tk.Label(table_header, text="TEACHER", bg='#800000', fg='white',
             font=("Bold", 11), width=20, anchor='w', padx=5).pack(side='left', fill='x', expand=True)


    canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0, height=400)
    scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Bind canvas width to scrollable frame
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind('<Configure>', on_canvas_configure)

    canvas.configure(yscrollcommand=scrollbar.set)

    status = student_data.get('approval_status')

    # If status is pending, show empty table rows ONLY - NO TEXT
    if status == 'pending':
        # Create empty table rows to show structure - increased to 10 rows
        for i in range(10):
            row_frame = tk.Frame(scrollable_frame, bg="white", height=40)
            row_frame.pack(fill='x', pady=0)
            row_frame.pack_propagate(False)

            # Three columns with equal width and borders
            col1_frame = tk.Frame(row_frame, bg='white',
                                  highlightbackground='#cccccc', highlightthickness=1)
            col1_frame.pack(side='left', fill='both', expand=True)
            tk.Label(col1_frame, text="", bg='white', font=("Arial", 10),
                     anchor='w', padx=5).pack(fill='both', expand=True)

            col2_frame = tk.Frame(row_frame, bg='white',
                                  highlightbackground='#cccccc', highlightthickness=1)
            col2_frame.pack(side='left', fill='both', expand=True)
            tk.Label(col2_frame, text="", bg='white', font=("Arial", 10),
                     anchor='w', padx=5).pack(fill='both', expand=True)

            col3_frame = tk.Frame(row_frame, bg='white',
                                  highlightbackground='#cccccc', highlightthickness=1)
            col3_frame.pack(side='left', fill='both', expand=True)
            tk.Label(col3_frame, text="", bg='white', font=("Arial", 10),
                     anchor='w', padx=5).pack(fill='both', expand=True)



    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Footer note REMOVED - grid extends to fill the space

    dashboard_frame.place(relx=0.5, rely=0.5, anchor="center", width=900, height=600)

    root.mainloop()


def edit_profile(student_data):
    """Handle edit profile action"""
    messagebox.showinfo("Edit Profile",
                        "Edit profile functionality will be implemented here.")


def drop_out(student_data):
    """Handle drop out action"""
    result = messagebox.askyesno(
        "Confirm Drop Out",
        "Are you sure you want to drop out?\nThis action cannot be undone.",
        icon='warning'
    )
    if result:
        messagebox.showinfo("Drop Out", "Drop out request submitted.")


def logout(root):
    """Handle logout action"""
    result = messagebox.askyesno(
        "Confirm Logout",
        "Are you sure you want to logout?",
        icon='question'
    )
    if result:
        root.destroy()
        from pages.login_page import login_page
        login_page()


# Example usage:
if __name__ == "__main__":
    # Can now call without arguments for testing
    student_dashboard()