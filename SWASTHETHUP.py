
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Backend as bk

print("BACKEND FILE:", bk.__file__)
print("BOOK APPT FUNCTION:", bk.book_appt)


# ==================================================
# MAIN WINDOW
# ==================================================

window = tk.Tk()

window.title("SWASTHSETHU")
window.geometry("500x500")


# ==================================================
# CLEAR WINDOW
# ==================================================

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


# ==================================================
# DISPLAY RESULTS
# ==================================================

def display_results(title, data, columns=None):
    result_window = tk.Toplevel(window)
    result_window.title(title)
    result_window.geometry("600x400")

    tk.Label(
        result_window,
        text=title,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    if not data:
        tk.Label(
            result_window,
            text="No records found.",
            font=("Arial", 12)
        ).pack(pady=20)
        return

    num_cols = len(data[0])
    if not columns or len(columns) != num_cols:
        columns = [f"Col {i+1}" for i in range(num_cols)]

    tree_frame = tk.Frame(result_window)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for row in data:
        tree.insert("", tk.END, values=row)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
# ==================================================
# BOOK APPOINTMENT
# ==================================================

def book_appointment_form():

    form = tk.Toplevel(window)
    form.title("Book Appointment")
    form.geometry("400x400")

    tk.Label(
        form,
        text="BOOK APPOINTMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(form, text="Doctor Name").pack()

    doctor_entry = tk.Entry(form, width=30)
    doctor_entry.pack(pady=5)

    tk.Label(form, text="Patient Name").pack()

    patient_entry = tk.Entry(form, width=30)
    patient_entry.pack(pady=5)

    tk.Label(form, text="Gender (M/F)").pack()

    gender_entry = tk.Entry(form, width=30)
    gender_entry.pack(pady=5)

    tk.Label(form, text="Age").pack()

    age_entry = tk.Entry(form, width=30)
    age_entry.pack(pady=5)


    def submit():

        doctor = doctor_entry.get()
        patient = patient_entry.get()
        gender = gender_entry.get()
        age = age_entry.get()

        if doctor == "" or patient == "" or gender == "" or age == "":
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
            bk.book_appt(
                doctor,
                patient,
                gender,
                age
            )

            messagebox.showinfo(
                "Success",
                "Appointment request successful!"
            )

            form.destroy()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )


    tk.Button(
        form,
        text="SUBMIT",
        command=submit,
        width=15
    ).pack(pady=20)


# ==================================================
# VIEW DOCTORS
# ==================================================

def view_doctors():

    try:
        doctors = bk.view_doc()

        display_results(
            "AVAILABLE DOCTORS",
            doctors
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==================================================
# MY APPOINTMENTS
# ==================================================

def my_appointments_form():

    form = tk.Toplevel(window)
    form.title("My Appointments")
    form.geometry("400x250")

    tk.Label(
        form,
        text="MY APPOINTMENTS",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        form,
        text="Enter Patient Name"
    ).pack()

    patient_entry = tk.Entry(
        form,
        width=30
    )

    patient_entry.pack(pady=10)


    def search():

        patient = patient_entry.get()

        if patient == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter patient name."
            )
            return

        try:
            appointments = bk.my_appts(patient)

            if not appointments:
                messagebox.showinfo(
                    "Result",
                    "No appointments found."
                )
            else:
                display_results(
                    "MY APPOINTMENTS",
                    appointments
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )


    tk.Button(
        form,
        text="SEARCH",
        command=search,
        width=15
    ).pack(pady=10)


# ==================================================
# ADMIN REGISTRATION
# ==================================================

def registration_form():

    form = tk.Toplevel(window)
    form.title("Patient Registration")
    form.geometry("400x300")

    tk.Label(
        form,
        text="PATIENT REGISTRATION",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(
        form,
        text="Patient Name"
    ).pack()

    name_entry = tk.Entry(
        form,
        width=30
    )
    name_entry.pack(pady=5)

    tk.Label(
        form,
        text="Mobile Number"
    ).pack()

    mob_entry = tk.Entry(
        form,
        width=30
    )
    mob_entry.pack(pady=5)


    def register():

        name = name_entry.get()
        mob = mob_entry.get()

        if name == "" or mob == "":
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:
            serial_no = bk.regn(
                name,
                mob
            )

            messagebox.showinfo(
                "Registration Successful",
                "Patient registered successfully!\n"
                + "Serial Number: "
                + str(serial_no)
            )

            form.destroy()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )


    tk.Button(
        form,
        text="REGISTER",
        command=register,
        width=15
    ).pack(pady=20)


# ==================================================
# CURRENT BOOKINGS
# ==================================================

def current_bookings():

    try:
        bookings = bk.current_bookings()

        display_results(
            "CURRENT BOOKINGS",
            bookings
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==================================================
# PATIENT HISTORY
# ==================================================

def patient_history_form():

    form = tk.Toplevel(window)
    form.title("Patient History")
    form.geometry("400x250")

    tk.Label(
        form,
        text="PATIENT HISTORY",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        form,
        text="Enter Patient Serial Number"
    ).pack()

    serial_entry = tk.Entry(
        form,
        width=30
    )

    serial_entry.pack(pady=10)


    def search():

        serial = serial_entry.get()

        if serial == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter serial number."
            )
            return

        try:
            serial = int(serial)

            history = bk.patnt_hist(
                serial
            )

            if not history:
                messagebox.showinfo(
                    "Result",
                    "Patient not found."
                )
            else:
                display_results(
                    "PATIENT HISTORY",
                    history
                )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Serial number must be a number."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )


    tk.Button(
        form,
        text="SEARCH",
        command=search,
        width=15
    ).pack(pady=10)


# ==================================================
# USER OPTIONS
# ==================================================

def show_user_options():

    clear_window()

    tk.Label(
        window,
        text="USER OPTIONS",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="BOOK APPOINTMENT",
        command=book_appointment_form,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="VIEW DOCTORS",
        command=view_doctors,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="MY APPOINTMENTS",
        command=my_appointments_form,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="BACK",
        command=show_options,
        width=15
    ).pack(pady=20)


# ==================================================
# ADMIN OPTIONS
# ==================================================

def show_admin_options():

    clear_window()

    tk.Label(
        window,
        text="ADMIN OPTIONS",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="REGISTRATION",
        command=registration_form,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="CURRENT BOOKINGS",
        command=current_bookings,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="PATIENT HISTORY",
        command=patient_history_form,
        width=25
    ).pack(pady=5)

    tk.Button(
        window,
        text="BACK",
        command=show_options,
        width=15
    ).pack(pady=20)


# ==================================================
# USER / ADMIN OPTIONS
# ==================================================

def show_options():

    clear_window()

    tk.Label(
        window,
        text="AYURSETH",
        font=("Arial", 20, "bold")
    ).pack(pady=30)

    tk.Button(
        window,
        text="USER",
        command=show_user_options,
        width=20
    ).pack(pady=10)

    tk.Button(
        window,
        text="ADMIN",
        command=show_admin_options,
        width=20
    ).pack(pady=10)


# ==================================================
# FIRST SCREEN
# ==================================================

def open_application():

    clear_window()
    show_options()


button = tk.Button(
    window,
    text="Tap to open",
    command=open_application,
    width=20
)

button.pack(pady=150)


# ==================================================
# RUN
# ==================================================

window.mainloop()

