import ctypes
import tkinter as tk
from tkinter import messagebox, ttk
import Backend as bk

# --- Fix High-DPI Scaling ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDpiAware()
    except Exception:
        pass


# ==============
# SWASTHSETHU
# ==============

window = tk.Tk()
window.title("SWASTHSETHU ")
window.geometry("1100x700")
window.resizable(False, False)
window.configure(bg="#F4F8FC")


# =========
# COLOURS
# =========

SIDEBAR = "#063B4C"
PRIMARY = "#08A6A6"
PRIMARY_DARK = "#087F8C"

BLUE = "#3182CE"
PURPLE = "#805AD5"
PINK = "#E85D75"
ORANGE = "#F59E0B"
GREEN = "#16A085"
WHITE = "#FFFFFF"
LIGHT = "#F4F8FC"
TEXT = "#0F0808"
GRAY = "#718096"

# Sidebar Button Colors (High Contrast & Visible)
SIDE_BTN_BG = "#063B4C"       # Matches sidebar background
SIDE_BTN_FG = "#FFFFFF"       # Bright white text
SIDE_BTN_HOVER = "#0C536B"    # Slightly lighter teal highlight on hover

# Global admin authentication state
is_admin_logged_in = False


# ==========
# UTILITY
# ==========

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def hover(button, normal, active):
    button.bind("<Enter>", lambda e: button.config(bg=active))
    button.bind("<Leave>", lambda e: button.config(bg=normal))


def app_button(parent, text, command, color=PRIMARY):
    btn = tk.Canvas(
        parent,
        width=190,
        height=45,
        bg="#111111",
        highlightthickness=0,
        bd=0,
        cursor="hand2"
    )

    btn.create_text(
        95,
        22,
        text=text,
        fill="white",
        font=("Arial", 12, "bold")
    )

    btn.bind("<Button-1>", lambda event: command())

    def enter(event):
        btn.configure(bg="#333333")

    def leave(event):
        btn.configure(bg="#111111")

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)

    return btn


# ==========================================================
# MAIN LAYOUT
# ==========================================================

sidebar = tk.Frame(window, bg=SIDEBAR, width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(window, bg=LIGHT)
content.pack(side="right", fill="both", expand=True)


# ========
# SIDEBAR
# ========

logo_frame = tk.Frame(sidebar, bg=SIDEBAR)
logo_frame.pack(pady=30)

logo = tk.Canvas(
    logo_frame,
    width=65,
    height=65,
    bg=SIDEBAR,
    highlightthickness=0
)
logo.pack()

logo.create_oval(5, 5, 60, 60, fill=PRIMARY, outline="")
logo.create_text(
    32, 32,
    text="+",
    font=("Arial", 32, "bold"),
    fill="white"
)

tk.Label(
    sidebar,
    text="SWASTHSETHU",
    font=("Arial", 18, "bold"),
    bg=SIDEBAR,
    fg="white"
).pack()

tk.Label(
    sidebar,
    text="Healthcare Platform",
    font=("Arial", 9),
    bg=SIDEBAR,
    fg="#A9D6DF"
).pack(pady=(2, 30))


# ===============
# SIDEBAR BUTTON
# ===============

def side_button(text, command):
    btn = tk.Button(
        sidebar,
        text=text,
        command=command,
        anchor="w",
        padx=25,
        font=("Arial", 11, "bold"),
        bg=SIDE_BTN_BG,
        fg=SIDE_BTN_FG,
        activebackground=PRIMARY,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        height=2
    )

    btn.pack(fill="x", padx=10, pady=3)
    hover(btn, SIDE_BTN_BG, SIDE_BTN_HOVER)

    return btn


# =======
# FORMS
# ========

def display_results(title, data, columns=None):
    result_window = tk.Toplevel(window)
    result_window.title(title)
    result_window.geometry("750x450")
    result_window.configure(bg=LIGHT)

    tk.Label(
        result_window,
        text=title,
        font=("Arial", 20, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(pady=15)

    if not data:
        tk.Label(
            result_window,
            text="No records found.",
            font=("Arial", 13),
            bg=LIGHT,
            fg=GRAY
        ).pack(pady=30)
        return

    num_cols = len(data[0])
    if not columns or len(columns) != num_cols:
        columns = [f"Column {i+1}" for i in range(num_cols)]

    frame = tk.Frame(result_window, bg=WHITE)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    for row in data:
        tree.insert("", tk.END, values=row)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# ==================
# BOOK APPOINTMENT
# ==================

def book_appointment_form():
    form = tk.Toplevel(window)
    form.title("Book Appointment")
    form.geometry("760x520")
    form.configure(bg=LIGHT)

    tk.Label(
        form,
        text="📅  Book Appointment",
        font=("Arial", 22, "bold"),
        bg="#FDFEFF",
        fg="#000000"
    ).pack(pady=20)

    body = tk.Frame(form, bg=LIGHT)
    body.pack(fill="both", expand=True, padx=20)

    # ---- LEFT SIDE: FORM FIELDS ----
    left = tk.Frame(body, bg=LIGHT)
    left.pack(side="left", fill="both", expand=True)

    fields = {}
    doctor_entry_holder = {}

    for label in ["Doctor Name", "Patient Name", "Gender (M/F)", "Age"]:
        tk.Label(
            left,
            text=label,
            font=("Arial", 10, "bold"),
            bg=LIGHT,
            fg=TEXT
        ).pack(anchor="w", padx=10)

        entry = tk.Entry(
            left,
            font=("Arial", 11),
            width=32,
            relief="solid",
            bd=1
        )
        entry.pack(pady=(5, 15), padx=10, anchor="w")

        fields[label] = entry

        if label == "Doctor Name":
            doctor_entry_holder["entry"] = entry

    # ---- RIGHT SIDE: DOCTOR LIST ----
    right = tk.Frame(body, bg=WHITE, width=260)
    right.pack(side="right", fill="y", padx=(15, 0))
    right.pack_propagate(False)

    tk.Label(
        right,
        text="👨‍⚕️ Available Doctors",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(15, 5), padx=10, anchor="w")

    list_frame = tk.Frame(right, bg=WHITE)
    list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    doctor_listbox = tk.Listbox(
        list_frame,
        font=("Arial", 11),
        relief="solid",
        bd=1,
        activestyle="none",
        selectbackground=PRIMARY,
        selectforeground="white"
    )

    scrollbar = ttk.Scrollbar(
        list_frame,
        orient="vertical",
        command=doctor_listbox.yview
    )

    doctor_listbox.configure(yscrollcommand=scrollbar.set)
    doctor_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    try:
        doctor_rows = bk.view_doc()
        doctor_names = [row[0] for row in doctor_rows]
    except Exception as e:
        doctor_names = []
        messagebox.showerror("Database Error", str(e))

    for name in doctor_names:
        doctor_listbox.insert(tk.END, name)

    def fill_doctor(event):
        selection = doctor_listbox.curselection()
        if selection:
            name = doctor_listbox.get(selection[0])
            doctor_entry_holder["entry"].delete(0, tk.END)
            doctor_entry_holder["entry"].insert(0, name)

    doctor_listbox.bind("<<ListboxSelect>>", fill_doctor)

    # ---- SUBMIT ----
    def submit():
        doctor = fields["Doctor Name"].get()
        patient = fields["Patient Name"].get()
        gender = fields["Gender (M/F)"].get()
        age = fields["Age"].get()

        if not doctor or not patient or not gender or not age:
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror(
                "Invalid Age",
                "Age must be a number."
            )
            return

        try:
            bk.book_appt(doctor, patient, gender, age)
            messagebox.showinfo(
                "Success",
                "Appointment booked successfully!"
            )
            form.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    app_button(
        form,
        "BOOK APPOINTMENT",
        submit,
        PRIMARY
    ).pack(padx=20, fill="x", pady=15)


# ==============
# VIEW DOCTORS
# ==============

def view_doctors():
    try:
        doctors = bk.view_doc()
        display_results("AVAILABLE DOCTORS", doctors)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ==================
# SHOW TREATMENTS
# ==================

def view_treatments():
    try:
        treatments = bk.show_treatments()
        display_results("TREATMENT NAMES", treatments)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# =================
# MY APPOINTMENTS
# =================

def my_appointments_form():
    form = tk.Toplevel(window)
    form.title("My Appointments")
    form.geometry("450x330")
    form.configure(bg=LIGHT)

    tk.Label(
        form,
        text="📋  My Appointments",
        font=("Arial", 21, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(pady=30)

    tk.Label(
        form,
        text="Patient Name",
        font=("Arial", 10, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack()

    entry = tk.Entry(form, width=32, font=("Arial", 11))
    entry.pack(pady=12)

    def search():
        patient = entry.get()
        if not patient:
            messagebox.showwarning(
                "Missing Information",
                "Enter patient name."
            )
            return

        try:
            appointments = bk.my_appts(patient)
            if not appointments:
                messagebox.showinfo("Result", "No appointments found.")
            else:
                display_results("MY APPOINTMENTS", appointments)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    app_button(
        form,
        "SEARCH APPOINTMENTS",
        search,
        BLUE
    ).pack(padx=70, fill="x", pady=20)


# ======================
# PATIENT REGISTRATION
# ======================

def registration_form():
    form = tk.Toplevel(window)
    form.title("Patient Registration")
    form.geometry("450x400")
    form.configure(bg=LIGHT)

    tk.Label(
        form,
        text="📝  Patient Registration",
        font=("Arial", 21, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(pady=25)

    tk.Label(
        form,
        text="Patient Name",
        font=("Arial", 10, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack()

    name = tk.Entry(form, width=32, font=("Arial", 11))
    name.pack(pady=8)

    tk.Label(
        form,
        text="Mobile Number",
        font=("Arial", 10, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack()

    mobile = tk.Entry(form, width=32, font=("Arial", 11))
    mobile.pack(pady=8)

    def register():
        patient = name.get()
        mob = mobile.get()

        if not patient or not mob:
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:
            serial = bk.regn(patient, mob)
            messagebox.showinfo(
                "Registration Successful",
                f"Patient registered successfully!\n\nSerial Number: {serial}"
            )
            form.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    app_button(
        form,
        "REGISTER PATIENT",
        register,
        ORANGE
    ).pack(padx=70, fill="x", pady=25)


# ===================
# CURRENT BOOKINGS
# ===================

def current_bookings():
    try:
        bookings = bk.current_bookings()
        display_results("CURRENT BOOKINGS", bookings)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ================
# PATIENT HISTORY
# ================

def patient_history_form():
    form = tk.Toplevel(window)
    form.title("Patient History")
    form.geometry("450x330")
    form.configure(bg=LIGHT)

    tk.Label(
        form,
        text="📚  Patient History",
        font=("Arial", 21, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(pady=30)

    tk.Label(
        form,
        text="Patient Serial Number",
        font=("Arial", 10, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack()

    entry = tk.Entry(form, width=32, font=("Arial", 11))
    entry.pack(pady=12)

    def search():
        value = entry.get()

        try:
            serial = int(value)
            history = bk.patnt_hist(serial)

            if not history:
                messagebox.showinfo("Result", "Patient not found.")
            else:
                display_results("PATIENT HISTORY", history)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid serial number."
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    app_button(
        form,
        "SEARCH HISTORY",
        search,
        PURPLE
    ).pack(padx=70, fill="x", pady=20)


# ============
# DASHBOARD
# ============

def dashboard():
    clear_content()

    # HEADER
    header = tk.Frame(content, bg=LIGHT)
    header.pack(fill="x", padx=35, pady=(30, 10))

    tk.Label(
        header,
        text="Good day 👋",
        font=("Arial", 14),
        bg=LIGHT,
        fg=GRAY
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Welcome to SWASTHSETHU",
        font=("Arial", 27, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(anchor="w")

    # HERO CARD
    hero = tk.Frame(content, bg=PRIMARY, height=150)
    hero.pack(fill="x", padx=35, pady=20)
    hero.pack_propagate(False)

    tk.Label(
        hero,
        text="Your health is our priority ❤️",
        font=("Arial", 22, "bold"),
        bg=PRIMARY,
        fg="white"
    ).pack(anchor="w", padx=30, pady=(25, 5))

    tk.Label(
        hero,
        text="Book appointments, find doctors and manage patient care.",
        font=("Arial", 11),
        bg=PRIMARY,
        fg="#E5FFFF"
    ).pack(anchor="w", padx=30)

    # STAT CARDS
    cards = tk.Frame(content, bg=LIGHT)
    cards.pack(fill="x", padx=35)

    def stat_card(parent, icon, title, subtitle, color):
        frame = tk.Frame(parent, bg=WHITE, width=190, height=115)
        frame.pack(side="left", padx=(0, 15))
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=icon,
            font=("Arial", 25),
            bg=WHITE,
            fg=color
        ).pack(anchor="w", padx=18, pady=(12, 0))

        tk.Label(
            frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", padx=18)

        tk.Label(
            frame,
            text=subtitle,
            font=("Arial", 9),
            bg=WHITE,
            fg=GRAY
        ).pack(anchor="w", padx=18)

    stat_card(cards, "👨‍⚕️", "Doctors", "Find available doctors", BLUE)
    stat_card(cards, "📅", "Appointments", "Manage appointments", PRIMARY)
    stat_card(cards, "❤️", "Patient Care", "Healthcare services", PINK)

    # QUICK ACTIONS
    tk.Label(
        content,
        text="Quick Actions",
        font=("Arial", 18, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(anchor="w", padx=35, pady=(30, 15))

    actions = tk.Frame(content, bg=LIGHT)
    actions.pack(padx=35, fill="x")

    action1 = app_button(
        actions,
        "📅  Book Appointment",
        book_appointment_form,
        PRIMARY
    )
    action1.pack(side="left", padx=(0, 10), ipadx=10)

    action2 = app_button(actions, "👨‍⚕️  Find Doctors", view_doctors, BLUE)
    action2.pack(side="left", padx=10, ipadx=10)

    action3 = app_button(
        actions,
        "📋  My Appointments",
        my_appointments_form,
        PURPLE
    )
    action3.pack(side="left", padx=10, ipadx=10)

    action4 = app_button(
        actions,
        "💊  Show Treatment Names",
        view_treatments,
        GREEN
    )
    action4.pack(side="left", padx=10, ipadx=10)


# ===========
# USER PAGE
# ===========

def user_page():
    clear_content()

    tk.Label(
        content,
        text="👤 User Services",
        font=("Arial", 27, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(anchor="w", padx=40, pady=(40, 10))

    tk.Label(
        content,
        text="Everything you need to manage your healthcare.",
        font=("Arial", 11),
        bg=LIGHT,
        fg="#000000"
    ).pack(anchor="w", padx=40)

    services = tk.Frame(content, bg=LIGHT)
    services.pack(padx=40, pady=35, fill="x")

    def service_card(icon, title, description, command, color):
        card = tk.Frame(services, bg=WHITE, width=300, height=150)
        card.pack(side="left", padx=(0, 20))
        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Arial", 30),
            bg=WHITE
        ).pack(anchor="w", padx=20, pady=(15, 0))

        tk.Label(
            card,
            text=title,
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", padx=20)

        tk.Label(
            card,
            text=description,
            font=("Arial", 9),
            bg=WHITE,
            fg=GRAY
        ).pack(anchor="w", padx=20)

        btn = tk.Button(
            card,
            text="Open →",
            command=command,
            bg=color,
            fg="#000000",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn.pack(anchor="w", padx=20, pady=8)

    service_card(
        "📅",
        "Book Appointment",
        "Schedule your doctor visit.",
        book_appointment_form,
        PRIMARY
    )
    service_card(
        "👨‍⚕️",
        "Find Doctors",
        "View available doctors.",
        view_doctors,
        BLUE
    )


# ===================
# ADMIN LOGIN PAGE
# ===================

def admin_login_page():
    clear_content()

    # Center card frame
    card = tk.Frame(content, bg=WHITE, bd=1, relief="solid")
    card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=360)

    tk.Label(
        card,
        text="🔒 Admin Login",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(35, 10))

    tk.Label(
        card,
        text="Enter password to access administrator controls.",
        font=("Arial", 9),
        bg=WHITE,
        fg=GRAY,
        wraplength=300
    ).pack(pady=(0, 20))

    tk.Label(
        card,
        text="Password",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=45)

    password_entry = tk.Entry(
        card,
        font=("Arial", 12),
        show="•",
        width=25,
        relief="solid",
        bd=1
    )
    password_entry.pack(pady=(5, 20), padx=45)
    password_entry.focus()

    def verify():
        global is_admin_logged_in
        pwd = password_entry.get()
        if pwd == "admin123":            #                                                          Set your admin password here
            is_admin_logged_in = True
            admin_page()
        else:
            messagebox.showerror(
                "Access Denied",
                "Incorrect password! Please try again."
            )
            password_entry.delete(0, tk.END)

    # Bind Enter key to submit
    password_entry.bind("<Return>", lambda e: verify())

    login_btn = tk.Button(
        card,
        text="LOGIN",
        font=("Arial", 15, "bold"),
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_DARK,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=verify
    )
    login_btn.pack(fill="x", padx=45, ipady=6)


# ============
# ADMIN PAGE
# ============

def admin_page():
    # Enforce login gate
    if not is_admin_logged_in:
        admin_login_page()
        return

    clear_content()

    header_frame = tk.Frame(content, bg=WHITE)
    header_frame.pack(fill="x", padx=40, pady=(40, 10))

    tk.Label(
        header_frame,
        text="⚙️ Admin Dashboard",
        font=("Arial", 27, "bold"),
        bg=LIGHT,
        fg=TEXT
    ).pack(side="left")

    # Logout Button
    def logout():
        global is_admin_logged_in
        is_admin_logged_in = False
        admin_login_page()

    logout_btn = tk.Button(
        header_frame,
        text="Logout 🚪",
        font=("Sans", 15, "bold"),
        bg="#E53E3E",
        fg="#000000",
        relief="flat",
        cursor="hand2",
        command=logout
    )
    logout_btn.pack(side="right")

    tk.Label(
        content,
        text="Manage patients, bookings and medical records.",
        font=("Arial", 11),
        bg=LIGHT,
        fg=GRAY
    ).pack(anchor="w", padx=40)

    actions = tk.Frame(content, bg=LIGHT)
    actions.pack(padx=40, pady=40)

    admin_items = [
        ("📝", "Patient Registration", registration_form, ORANGE),
        ("📊", "Current Bookings", current_bookings, PINK),
        ("📚", "Patient History", patient_history_form, PURPLE)
    ]

    for icon, title, command, color in admin_items:
        card = tk.Frame(actions, bg=WHITE, width=280, height=140)
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Arial", 30),
            bg=WHITE
        ).pack(pady=(12, 0))

        tk.Label(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack()

        btn = tk.Button(
            card,
            text="Open →",
            command=command,
            bg=color,
            fg="#000000",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn.pack(pady=8)


# ====================
# SIDEBAR NAVIGATION
# ====================

side_button("🏠   Dashboard", dashboard)
side_button("👤   User Services", user_page)
side_button("⚙️   Admin Panel", admin_page)

# Separator
tk.Frame(sidebar, bg="#17576A", height=1).pack(fill="x", padx=20, pady=25)

tk.Label(
    sidebar,
    text="QUICK ACCESS",
    font=("Arial", 8, "bold"),
    bg=SIDEBAR,
    fg="#78AAB5"
).pack(anchor="w", padx=25, pady=5)

side_button("📅   Book Appointment", book_appointment_form)
side_button("👨‍⚕️   View Doctors", view_doctors)
side_button("💊   Show Treatment Names", view_treatments)


# =========
# FOOTER
# =========

tk.Label(
    sidebar,
    text="SWASTHSETHU v1.0",
    font=("Arial", 8),
    bg=SIDEBAR,
    fg="#6F9BA5"
).pack(side="bottom", pady=20)


# ===================
# START DASHBOARD
# ===================

dashboard()

# ======
# RUN
# ======

window.mainloop()
