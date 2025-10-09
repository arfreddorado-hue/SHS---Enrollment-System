import tkinter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from utils import display_background, make_layout, make_icon
import random  # Import random module for ID generation
import re  # Import regex module for email validation
from database.db_config import db_config
from services.account_service import save_account
from services.program_service import get_programs
from pages.studentlogin_page import studentlogin_page


def signup_page():
    root = tk.Tk()
    root.title("Tkinter Hub (Student Management && Registration System)")
    make_layout(root)
    display_background(root)
    bg_color = '#800000'
    # Variable to store uploaded image path
    uploaded_image_path = None

    # New window
    signup_frame = tk.Frame(root, highlightbackground='maroon', highlightthickness=3, background='white')
    heading_lb = tk.Label(signup_frame,
                          text="Tkinter Hub (Student Management && Registration System)",
                          bg=bg_color, fg="white",
                          font=("Bold", 16))
    heading_lb.pack(fill='x')

    # Main content frame
    content_frame = tk.Frame(signup_frame, bg="white")
    content_frame.pack(fill='both', expand=True, padx=25, pady=25)

    # Left side - Student Photo
    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.grid(row=0, column=0, padx=(0, 30), sticky='n')

    # Photo frame that will be clickable
    photo_frame = tk.Frame(left_frame, width=180, height=210, bg='lightgray',
                           highlightbackground='black', highlightthickness=2,
                           cursor='hand2')
    photo_frame.pack(pady=10)
    photo_frame.pack_propagate(False)

    # Label to display the image - fills the entire frame
    photo_label = tk.Label(photo_frame, bg='lightgray', width=180, height=210)
    photo_label.pack(fill='both', expand=True)

    # Function to upload and display image
    def upload_image(event=None):
        nonlocal uploaded_image_path
        file_path = filedialog.askopenfilename(
            title="Select Student Photo",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")]
        )

        if file_path:
            uploaded_image_path = file_path
            try:
                # Open image
                img = Image.open(file_path)

                # Frame dimensions (accounting for border)
                frame_width = 176  # 180 - 4 (2px border on each side)
                frame_height = 206  # 210 - 4 (2px border on each side)

                # Get image aspect ratio
                img_ratio = img.width / img.height
                frame_ratio = frame_width / frame_height

                # Resize to fill the frame completely (crop if necessary)
                if img_ratio > frame_ratio:
                    # Image is wider, fit to height and crop width
                    new_height = frame_height
                    new_width = int(new_height * img_ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    # Crop to center
                    left = (new_width - frame_width) // 2
                    img = img.crop((left, 0, left + frame_width, frame_height))
                else:
                    # Image is taller, fit to width and crop height
                    new_width = frame_width
                    new_height = int(new_width / img_ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    # Crop to center
                    top = (new_height - frame_height) // 2
                    img = img.crop((0, top, frame_width, top + frame_height))

                photo = ImageTk.PhotoImage(img)

                # Update the label with new image
                photo_label.config(image=photo, bg='white')
                photo_label.image = photo  # Keep a reference

                # Reset photo frame background if it was highlighted
                photo_frame.config(bg='lightgray')
                photo_label.config(bg='lightgray')
            except Exception as e:
                print(f"Error loading image: {e}")

    # Try to load default image
    try:
        default_img = Image.open("C:/Users/User/Downloads/graduated.png")
        # Maintain aspect ratio for default image too
        default_img.thumbnail((176, 206), Image.Resampling.LANCZOS)

        # Create background and center the image
        final_default = Image.new('RGB', (176, 206), 'lightgray')
        x = (176 - default_img.width) // 2
        y = (206 - default_img.height) // 2
        final_default.paste(default_img, (x, y))

        default_photo = ImageTk.PhotoImage(final_default)
        photo_label.config(image=default_photo, bg='white')
        photo_label.image = default_photo
    except:
        # If default image not found, show placeholder text
        photo_label.config(text="Click to\nUpload Photo",
                           font=("Arial", 12),
                           fg='gray',
                           bg='lightgray')

    # Bind click event to photo frame and label
    photo_frame.bind("<Button-1>", upload_image)
    photo_label.bind("<Button-1>", upload_image)

    # Add upload instruction text
    upload_instruction = tk.Label(left_frame,
                                  text="Click photo to upload student image",
                                  font=("Arial", 9), bg="white", fg="gray")
    upload_instruction.pack(pady=(5, 0))

    # Student Full Name
    tk.Label(left_frame, text="Enter Student Full Name:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(5, 2))
    name_entry = tk.Entry(left_frame, font=("Arial", 11), width=30)
    name_entry.pack(fill='x')

    # Student Gender
    tk.Label(left_frame, text="Select Student Gender:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    gender_frame = tk.Frame(left_frame, bg="white")
    gender_frame.pack(fill='x')
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male",
                   font=("Arial", 10), bg="white").pack(side='left', padx=(0, 20))
    tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female",
                   font=("Arial", 10), bg="white").pack(side='left')

    # Student Age
    tk.Label(left_frame, text="Enter Student Age:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    age_entry = tk.Entry(left_frame, font=("Arial", 11), width=30)
    age_entry.pack(fill='x')

    # Contact Phone Number
    tk.Label(left_frame, text="Enter Contact Phone Number:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    phone_entry = tk.Entry(left_frame, font=("Arial", 11), width=30)
    phone_entry.pack(fill='x')

    # Student Class
    tk.Label(left_frame, text="Select Program to Enroll:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    class_combo = ttk.Combobox(left_frame, font=("Arial", 10), width=28, state='readonly')

    program_dict = {p["name"]: p["id"] for p in get_programs()}
    class_combo['values'] = [p["name"] for p in get_programs()]

    selected_program_id = None
    def on_select_program(event):
        nonlocal selected_program_id
        selected_name = class_combo.get()
        selected_program_id = program_dict[selected_name]

    class_combo.bind("<<ComboboxSelected>>", on_select_program)
    class_combo.pack(fill='x')

    # Right side - Student ID and other info
    right_frame = tk.Frame(content_frame, bg="white")
    right_frame.grid(row=0, column=1, sticky='n', padx=(50, 0))

    # Generate a random 6-digit student ID number
    student_id = str(random.randint(100000, 999999))

    # Student ID Number
    id_frame = tk.Frame(right_frame, bg="white")
    id_frame.pack(fill='x', pady=(70, 5))
    tk.Label(id_frame, text="Student ID Number:",
             font=("Arial", 11), bg="white").pack(side='left')
    id_label = tk.Label(id_frame, text=student_id,
                        font=("Arial Bold", 16), bg="white")
    id_label.pack(side='left', padx=5)

    id_info = tk.Label(right_frame,
                       text="Automatically Generated ID Number\n! Remember Using This ID Number\nStudent will Login Account.",
                       font=("Arial", 9), bg="white", fg="gray", justify='left')
    id_info.pack(fill='x', pady=(0, 15))

    # Student Email Address
    tk.Label(right_frame, text="Enter Student Email Address:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    email_entry = tk.Entry(right_frame, font=("Arial", 11), width=30)
    email_entry.pack(fill='x')

    email_info = tk.Label(right_frame,
                          text="Via Email Address Student\nCan Recover Account\n! In Case Forgetting Password And Also\nStudent will get Future Notifications.",
                          font=("Arial", 9), bg="white", fg="gray", justify='left')
    email_info.pack(fill='x', pady=(5, 15))

    # Create Account Password
    tk.Label(right_frame, text="Create Account Password:",
             font=("Arial", 11), bg="white", anchor='w').pack(fill='x', pady=(10, 2))
    password_entry = tk.Entry(right_frame, font=("Arial", 11), width=30, show='*')
    password_entry.pack(fill='x')

    password_info = tk.Label(right_frame,
                             text="Via Student Created Password\nAnd Provided Student ID Number\nStudent Can Login Account.",
                             font=("Arial", 9), bg="white", fg="gray", justify='left')
    password_info.pack(fill='x', pady=(5, 20))

    # Buttons
    button_frame = tk.Frame(right_frame, bg="white")
    button_frame.pack(pady=20)

    def go_home():
        result = messagebox.askyesno("Confirm Exit",
                                     "Are you sure you want to go back to Home?\nAny unsaved data will be lost.",
                                     icon='warning')
        if result:
            root.destroy()
            from pages.login_page import login_page
            login_page()

    def submit_form():
        # Reset all field backgrounds to white
        name_entry.config(bg='white')
        age_entry.config(bg='white')
        phone_entry.config(bg='white')
        class_combo.config(background='white')
        email_entry.config(bg='white')
        password_entry.config(bg='white')
        photo_frame.config(bg='lightgray')
        photo_label.config(bg='lightgray')

        # Check for missing fields
        missing_fields = []

        if not name_entry.get().strip():
            missing_fields.append("Student Full Name")
            name_entry.config(bg='#ffcccc')

        if not age_entry.get().strip():
            missing_fields.append("Student Age")
            age_entry.config(bg='#ffcccc')

        if not phone_entry.get().strip():
            missing_fields.append("Contact Phone Number")
            phone_entry.config(bg='#ffcccc')

        if not class_combo.get():
            missing_fields.append("Program to Enroll")
            class_combo.config(background='#ffcccc')

        if not email_entry.get().strip():
            missing_fields.append("Student Email Address")
            email_entry.config(bg='#ffcccc')

        if not password_entry.get().strip():
            missing_fields.append("Account Password")
            password_entry.config(bg='#ffcccc')

        if not uploaded_image_path:
            missing_fields.append("Student Photo")
            photo_frame.config(bg='#ffcccc')
            photo_label.config(bg='#ffcccc')

        # If there are missing fields, show error message
        if missing_fields:
            messagebox.showerror("Missing Information",
                                 f"Please fill in the following required fields:\n\n• " +
                                 "\n• ".join(missing_fields))
            return

        # Validate age (must be a number and ≥ 17)
        try:
            age_value = int(age_entry.get().strip())
            if age_value < 17:
                messagebox.showerror("Invalid Age", "Student age must be 17 or older.")
                age_entry.config(bg='#ffcccc')
                return
        except ValueError:
            messagebox.showerror("Invalid Age", "Please enter a valid numeric age.")
            age_entry.config(bg='#ffcccc')
            return


        # Validate email format
        email = email_entry.get().strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Invalid Email",
                                 "Please enter a valid email address.\n\nExample: arfredPOGI@gmail.com")
            email_entry.config(bg='#ffcccc')
            return

        # If all fields are filled, proceed with submission
        # Save data if fields has no validation errors
        is_account_saved = save_account(
            full_name = name_entry.get(),
            gender = gender_var.get(),
            age = age_entry.get(),
            contact_number= phone_entry.get(),
            program= selected_program_id,
            email_address= email_entry.get(),
            password= password_entry.get(),
            profile_picture= uploaded_image_path,
            student_id_num = student_id
        )

        if is_account_saved:
            messagebox.showinfo("Success", "Student registration submitted successfully!")
            root.destroy()
            studentlogin_page()
        else:
            messagebox.showerror("Error", "Oops, something went wrong!")

    home_btn = tk.Button(button_frame, text="Home", font=('Arial Bold', 14),
                         bg='#dc3545', fg='white', command=go_home,
                         width=10, bd=0, cursor='hand2')
    home_btn.pack(side='left', padx=5)

    submit_btn = tk.Button(button_frame, text="Submit", font=('Arial Bold', 14),
                           bg='#1e3a5f', fg='white', command=submit_form,
                           width=10, bd=0, cursor='hand2')
    submit_btn.pack(side='left', padx=5)




    signup_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=650)

    root.mainloop()