import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils import display_background, make_layout, make_icon


def practice(student_data):
    """
    Student Dashboard Window

    student_data should contain:
    - full_name: Student's full name
    - email: Student's email
    - profile_picture: Path to profile picture
    - grade_level: Grade level (e.g., "Grade 11")
    - section: Section name
    - adviser: Adviser's name
    - subjects: List of subject dictionaries with 'name', 'schedule', 'teacher'
    - status: 'approved' or 'pending'
    """
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
        text=f"{student_data.get('grade_level', 'Grade Level')} & {student_data.get('section', 'Section')}",
        bg=bg_color, fg="white",
        font=("Bold", 18)
    )
    heading_lb.pack(fill='x')

    # Adviser name
    adviser_lb = tk.Label(
        dashboard_frame,
        text=f"({student_data.get('adviser', 'Adviser Name')})",
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
        profile_pic_path = student_data.get('profile_picture',
                                            "C:/Users/User/Downloads/graduated.png")
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
        text=student_data.get('full_name', 'Student Name'),
        font=("Bold", 14),
        bg="white",
        wraplength=150
    )
    name_label.pack(pady=(10, 5))

    # Student email
    email_label = tk.Label(
        left_frame,
        text=student_data.get('email', 'student@email.com'),
        font=("Arial", 10),
        bg="white",
        fg="gray",
        wraplength=150
    )
    email_label.pack(pady=(0, 15))

    # Status indicator
    status = student_data.get('status', 'pending')
    status_color = '#28a745' if status == 'approved' else '#ffc107'
    status_text = 'APPROVED' if status == 'approved' else 'PENDING'

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

    # Scrollable frame for subjects
    canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Add subjects to table
    subjects = student_data.get('subjects', [])

    if not subjects:
        # Show placeholder if no subjects
        no_subjects_label = tk.Label(
            scrollable_frame,
            text="No subjects assigned yet.\nPlease wait for approval.",
            font=("Arial", 12),
            bg="white",
            fg="gray",
            pady=50
        )
        no_subjects_label.pack()
    else:
        for subject in subjects:
            row_frame = tk.Frame(scrollable_frame, bg="white",
                                 highlightbackground='#ddd', highlightthickness=1)
            row_frame.pack(fill='x', pady=2)

            tk.Label(row_frame, text=subject.get('name', 'Subject'),
                     bg='white', font=("Arial", 10), width=20,
                     anchor='w', padx=5).pack(side='left', fill='x', expand=True)
            tk.Label(row_frame, text=subject.get('schedule', 'TBA'),
                     bg='white', font=("Arial", 10), width=20,
                     anchor='w', padx=5).pack(side='left', fill='x', expand=True)
            tk.Label(row_frame, text=subject.get('teacher', 'TBA'),
                     bg='white', font=("Arial", 10), width=20,
                     anchor='w', padx=5).pack(side='left', fill='x', expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Footer note
    footer_note = tk.Label(
        right_frame,
        text="(List of Fixed subjects per program)    (Schedule for subjects)    (Fixed list of professor per subjects)",
        font=("Arial", 8),
        bg="white",
        fg="gray"
    )
    footer_note.pack(pady=(10, 0))

    # Logout button in bottom right
    logout_indicator = tk.Label(
        dashboard_frame,
        text="LOGOUT",
        bg='#28a745',
        fg='white',
        font=("Bold", 9),
        padx=10,
        pady=5,
        cursor='hand2'
    )
    logout_indicator.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)
    logout_indicator.bind("<Button-1>", lambda e: logout(root))

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
    # Sample student data
    sample_data = {
        'full_name': 'Juan Dela Cruz',
        'email': 'juan.delacruz@email.com',
        'profile_picture': 'C:/Users/User/Downloads/graduated.png',
        'grade_level': 'Grade 11',
        'section': 'STEM-A',
        'adviser': 'Mrs. Maria Santos',
        'status': 'approved',  # or 'pending'
        'subjects': [
            {'name': 'Mathematics', 'schedule': 'MWF 8:00-9:00 AM', 'teacher': 'Mr. Pedro Reyes'},
            {'name': 'English', 'schedule': 'TTH 10:00-11:30 AM', 'teacher': 'Ms. Ana Lopez'},
            {'name': 'Science', 'schedule': 'MWF 1:00-2:30 PM', 'teacher': 'Dr. Carlos Mendoza'},
            {'name': 'Filipino', 'schedule': 'TTH 2:00-3:30 PM', 'teacher': 'Mrs. Rosa Garcia'},
            {'name': 'PE', 'schedule': 'F 3:00-5:00 PM', 'teacher': 'Coach Miguel Torres'},
        ]
    }

    practice(sample_data)