import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from services.admin_service import fetch_students, approve_student_request, reject_student_approval
from utils import make_layout, make_icon


def admin_dashboard(admin_data=None):
    root = tk.Tk()
    root.title("Admin Dashboard - SHS Enrollment System")
    make_layout(root)

    root.state('zoomed')

    bg_color = '#800000'

    student_data = fetch_students()

    # Main window frame - now fills entire window
    dashboard_frame = tk.Frame(root, highlightbackground='maroon',
                               highlightthickness=3, background='white')
    dashboard_frame.pack(fill='both', expand=True)

    # Header
    heading_lb = tk.Label(
        dashboard_frame,
        text="ADMIN DASHBOARD",
        bg=bg_color, fg="white",
        font=("Bold", 20)
    )
    heading_lb.pack(fill='x')

    # Welcome message
    welcome_lb = tk.Label(
        dashboard_frame,
        text=f"Welcome, {admin_data.get('name')}!",
        bg=bg_color, fg="white",
        font=("Arial", 12)
    )
    welcome_lb.pack(fill='x')

    # Main content frame
    content_frame = tk.Frame(dashboard_frame, bg="white")
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Top controls
    controls_frame = tk.Frame(content_frame, bg="white")
    controls_frame.pack(fill='x', pady=(0, 10))

    # Filter buttons
    filter_label = tk.Label(controls_frame, text="Filter:", font=("Bold", 11), bg="white")
    filter_label.pack(side='left', padx=(0, 10))

    filter_var = tk.StringVar(value="all")

    def apply_filter():
        refresh_student_list()

    all_btn = tk.Radiobutton(controls_frame, text="All", variable=filter_var, value="all",
                             font=("Arial", 10), bg="white", command=apply_filter)
    all_btn.pack(side='left', padx=5)

    pending_btn = tk.Radiobutton(controls_frame, text="Pending", variable=filter_var, value="pending",
                                 font=("Arial", 10), bg="white", command=apply_filter)
    pending_btn.pack(side='left', padx=5)

    approved_btn = tk.Radiobutton(controls_frame, text="Approved", variable=filter_var, value="approved",
                                  font=("Arial", 10), bg="white", command=apply_filter)
    approved_btn.pack(side='left', padx=5)

    rejected_btn = tk.Radiobutton(controls_frame, text="Rejected", variable=filter_var, value="rejected",
                                  font=("Arial", 10), bg="white", command=apply_filter)
    rejected_btn.pack(side='left', padx=5)

    # Logout button
    logout_btn = tk.Button(
        controls_frame,
        text="Logout",
        font=('Arial', 10),
        bg='#dc3545',
        fg='white',
        command=lambda: logout(root),
        bd=0,
        cursor='hand2'
    )
    logout_btn.pack(side='right', padx=5)

    # Table header
    table_header = tk.Frame(content_frame, bg="white")
    table_header.pack(fill='x', pady=(0, 5))

    tk.Label(table_header, text="ID", bg='#800000', fg='white',
             font=("Bold", 10), width=5, anchor='center').pack(side='left', padx=1)
    tk.Label(table_header, text="NAME", bg='#800000', fg='white',
             font=("Bold", 10), width=15, anchor='w', padx=5).pack(side='left', padx=1)
    tk.Label(table_header, text="EMAIL", bg='#800000', fg='white',
             font=("Bold", 10), width=18, anchor='w', padx=5).pack(side='left', padx=1)
    tk.Label(table_header, text="STATUS", bg='#800000', fg='white',
             font=("Bold", 10), width=10, anchor='center').pack(side='left', padx=1)
    tk.Label(table_header, text="ACTIONS", bg='#800000', fg='white',
             font=("Bold", 10), width=26, anchor='center').pack(side='left', padx=1)

    # Scrollable frame for students
    canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind('<Configure>', on_canvas_configure)

    canvas.configure(yscrollcommand=scrollbar.set)

    def approve_student(student_id, student_name):
        """Approve student enrollment"""
        result = messagebox.askyesno(
            "Confirm Approval",
            f"Are you sure you want to approve {student_name}'s enrollment?",
            icon='question'
        )
        if result:
            # Update student status
            approved_student = approve_student_request(student_id)

            if approved_student:
                messagebox.showinfo("Success", f"{student_name} has been approved!")
                refresh_student_list()
                update_stats()
            else:
                messagebox.showerror("Error", f"Failed to approve student {student_name}")
                return

    def reject_student(student_id, student_name):
        result = messagebox.askyesno(
            "Confirm Approval",
            f"Are you sure you want to reject {student_name}'s enrollment?",
            icon='question'
        )

        if result:
            approved_student = reject_student_approval(student_id)

            if approved_student:
                messagebox.showinfo("Success", f"{student_name} has been approved!")
                refresh_student_list()
                update_stats()
            else:
                messagebox.showerror("Error", f"Failed to approve student {student_name}")
                return

    def refresh_student_list():
        """Refresh the student list based on filter"""
        # Clear current list
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Get filter value
        filter_value = filter_var.get()

        # Filter students
        filtered_students = fetch_students()

        match filter_value:
            case "pending":
                filtered_students = [s for s in filtered_students if s['approval_status'] == 'pending']
            case "approved":
                filtered_students = [s for s in filtered_students if s['approval_status'] == 'approved']
            case "rejected":
                filtered_students = [s for s in filtered_students if s['approval_status'] == 'rejected']

        # Display students
        if not filtered_students:
            no_students_label = tk.Label(
                scrollable_frame,
                text="No students found.",
                font=("Arial", 12),
                bg="white",
                fg="gray",
                pady=50
            )
            no_students_label.pack()
        else:
            for student in filtered_students:
                row_frame = tk.Frame(scrollable_frame, bg="white",
                                     highlightbackground='#ddd', highlightthickness=1)
                row_frame.pack(fill='x', pady=2)

                # ID
                tk.Label(row_frame, text=str(student['id']),
                         bg='white', font=("Arial", 9), width=5,
                         anchor='center').pack(side='left', padx=1)

                # Name
                tk.Label(row_frame, text=student['full_name'],
                         bg='white', font=("Arial", 9), width=20,
                         anchor='w', padx=5).pack(side='left', padx=1)

                # Email
                tk.Label(row_frame, text=student['email_address'],
                         bg='white', font=("Arial", 9), width=20,
                         anchor='w', padx=5).pack(side='left', padx=1)

                # Status
                status_color = '#28a745' if student['approval_status'] == 'approved' else '#ffc107'
                status_label = tk.Label(row_frame, text=student['approval_status'].upper(),
                                        bg=status_color, fg='white', font=("Bold", 8),
                                        width=10, anchor='center')
                status_label.pack(side='left', padx=1)

                # Actions
                actions_frame = tk.Frame(row_frame, bg='white')
                actions_frame.pack(side='left', padx=1)

                match student['approval_status']:
                    case 'pending':
                        approve_btn = tk.Button(
                            actions_frame,
                            text="✓ Approve",
                            font=('Arial', 8),
                            bg='#28a745',
                            fg='white',
                            command=lambda sid=student['id'], sname=student['full_name']: approve_student(sid, sname),
                            bd=0,
                            cursor='hand2',
                            width=12
                        )
                        approve_btn.pack(side='left', padx=2)

                        reject_btn = tk.Button(
                            actions_frame,
                            text="✗ Reject",
                            font=('Arial', 8),
                            bg='#dc3545',
                            fg='white',
                            command=lambda sid=student['id'], sname=student['full_name']: reject_student(sid, sname),
                            bd=0,
                            cursor='hand2',
                            width=12
                        )
                        reject_btn.pack(side='left', padx=2)
                    case 'approved':
                        tk.Label(actions_frame, text="Approved ✔",
                                 bg='white', fg='#28a745', font=("Arial", 9),
                                 width=15).pack(side='left')
                    case 'rejected':
                        tk.Label(actions_frame, text="Rejected ✖",
                                 bg='white', fg='#28a745', font=("Arial", 9),
                                 width=15).pack(side='left')

    # Initial load
    refresh_student_list()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Statistics at bottom
    stats_frame = tk.Frame(content_frame, bg="#f8f9fa", relief='solid', borderwidth=1)
    stats_frame.pack(fill='x', pady=(10, 0))

    def update_stats():
        total = len(student_data)
        pending = len([s for s in student_data if s['approval_status'] == 'pending'])
        approved = len([s for s in student_data if s['approval_status'] == 'approved'])
        rejected = len([s for s in student_data if s['approval_status'] == 'rejected'])

        stats_text = f"Total Students: {total} \n Pending: {pending}  |  Approved: {approved} | Rejected: {rejected}"
        stats_label.config(text=stats_text)

    stats_label = tk.Label(stats_frame, text="", font=("Arial", 10), bg="#f8f9fa", fg="#333", pady=8)
    stats_label.pack()
    update_stats()

    root.mainloop()


def logout(root):
    """Handle logout action"""
    result = messagebox.askyesno(
        "Confirm Logout",
        "Are you sure you want to logout?",
        icon='question'
    )

    if result:
        root.destroy()
        from pages.adminlogin_page import adminlogin_page
        adminlogin_page()


# Example usage:
if __name__ == "__main__":
    admin_dashboard()
