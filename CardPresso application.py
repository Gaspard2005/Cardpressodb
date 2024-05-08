import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

def connect_to_database(user, password, database, root_conn):
    if not database:
        messagebox.showerror("Error", "Please enter the database name.")
        return
    try:
        conn = pymysql.connect(user=user, password=password, database=database)
        messagebox.showinfo("Success", "Connected to the database")
        root_conn.destroy()
        manage_data_window(conn)
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the database: {e}")

def manage_data_window(conn):
    def display_data():
        cursor = conn.cursor()
        cursor.execute(
            "SELECT people.IDPerson, people.IDCard, people.Lastname, people.Firstname, site.Name AS Site, department.Name AS Department, people.IDSAP FROM people LEFT JOIN site ON people.Site = site.IDSite LEFT JOIN department ON people.Department = department.IDDepartment")
        rows = cursor.fetchall()
        for row in treeview.get_children():
            treeview.delete(row)
        for row in rows:
            treeview.insert("", "end", values=row)

    def add_person():
        id_card = id_card_entry.get()
        lastname = lastname_entry.get()
        firstname = firstname_entry.get()
        site = site_entry.get()
        department = department_entry.get()
        idsap = idsap_entry.get()

        if not all([id_card, lastname, firstname, site, department, idsap]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT IDPerson FROM people WHERE IDCard = %s", (id_card,))
        if cursor.fetchone():
            messagebox.showerror("Error", f"A person with IDCard '{id_card}' already exists.")
            return

        cursor.execute("SELECT IDPerson FROM people WHERE IDSAP = %s", (idsap,))
        if cursor.fetchone():
            messagebox.showerror("Error", f"A person with IDSAP '{idsap}' already exists.")
            return

        try:
            cursor.execute(
                "INSERT INTO people (IDCard, Lastname, Firstname, Site, Department, IDSAP) VALUES (%s, %s, %s, %s, %s, %s)",
                (int(id_card), lastname, firstname, int(site), int(department), int(idsap)))
            conn.commit()
            messagebox.showinfo("Success", "Person added successfully")
            display_data()
            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding person to the database: {e}")

    def delete_person():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a person to delete.")
            return
        id_person = treeview.item(selected_item)['values'][0]
        cursor = conn.cursor()
        cursor.execute("DELETE FROM people WHERE IDPerson = %s", (id_person,))
        conn.commit()
        messagebox.showinfo("Success", "Person deleted successfully")
        display_data()

    def edit_person():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a person to edit.")
            return
        id_person = treeview.item(selected_item)['values'][0]
        edit_window = tk.Toplevel(root_manage)
        edit_window.title("Edit Person")

        def update_person():
            new_id_card = id_card_entry.get()
            new_lastname = lastname_entry.get()
            new_firstname = firstname_entry.get()
            new_site = site_entry.get()
            new_department = department_entry.get()
            new_idsap = idsap_entry.get()

            if not all([new_id_card, new_lastname, new_firstname, new_site, new_department, new_idsap]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            try:
                cursor = conn.cursor()

                # Check for duplicate IDCard
                cursor.execute("SELECT IDPerson FROM people WHERE IDCard = %s AND IDPerson != %s",
                               (new_id_card, id_person))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"A person with IDCard '{new_id_card}' already exists.")
                    return

                # Check for duplicate IDSAP
                cursor.execute("SELECT IDPerson FROM people WHERE IDSAP = %s AND IDPerson != %s",
                               (new_idsap, id_person))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"A person with IDSAP '{new_idsap}' already exists.")
                    return

                cursor.execute(
                    "UPDATE people SET IDCard = %s, Lastname = %s, Firstname = %s, Site = %s, Department = %s, IDSAP = %s WHERE IDPerson = %s",
                    (int(new_id_card), new_lastname, new_firstname, int(new_site), int(new_department), int(new_idsap),
                     id_person))
                conn.commit()
                messagebox.showinfo("Success", "Person updated successfully")
                display_data()
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating person: {e}")

        tk.Label(edit_window, text="ID Card:").grid(row=0, column=0)
        id_card_entry = tk.Entry(edit_window)
        id_card_entry.grid(row=0, column=1)
        tk.Label(edit_window, text="Lastname:").grid(row=1, column=0)
        lastname_entry = tk.Entry(edit_window)
        lastname_entry.grid(row=1, column=1)
        tk.Label(edit_window, text="Firstname:").grid(row=2, column=0)
        firstname_entry = tk.Entry(edit_window)
        firstname_entry.grid(row=2, column=1)
        tk.Label(edit_window, text="Site:").grid(row=3, column=0)
        site_entry = tk.Entry(edit_window)
        site_entry.grid(row=3, column=1)
        tk.Label(edit_window, text="Department:").grid(row=4, column=0)
        department_entry = tk.Entry(edit_window)
        department_entry.grid(row=4, column=1)
        tk.Label(edit_window, text="IDSAP:").grid(row=5, column=0)
        idsap_entry = tk.Entry(edit_window)
        idsap_entry.grid(row=5, column=1)

        edit_button = tk.Button(edit_window, text="Update", command=update_person, bg="lightgreen")
        edit_button.grid(row=6, column=0, columnspan=2)

        # Fetch person's current data and populate the entry fields
        cursor = conn.cursor()
        cursor.execute("SELECT IDCard, Lastname, Firstname, Site, Department, IDSAP FROM people WHERE IDPerson = %s", (id_person,))
        person_data = cursor.fetchone()
        id_card_entry.insert(0, person_data[0])
        lastname_entry.insert(0, person_data[1])
        firstname_entry.insert(0, person_data[2])
        site_entry.insert(0, person_data[3])
        department_entry.insert(0, person_data[4])
        idsap_entry.insert(0, person_data[5])

    def display_info():
        department_info = "Department IDs:\n"
        cursor = conn.cursor()
        cursor.execute("SELECT IDDepartment, Name FROM department")
        departments = cursor.fetchall()
        for department in departments:
            department_info += f"{department[1]}: {department[0]}\n"

        site_info = "\nSite IDs:\n"
        cursor.execute("SELECT IDSite, Name FROM site")
        sites = cursor.fetchall()
        for site in sites:
            site_info += f"{site[1]}: {site[0]}\n"

        messagebox.showinfo("Information", department_info + "\n" + site_info)

    def clear_entries():
        id_card_entry.delete(0, 'end')
        lastname_entry.delete(0, 'end')
        firstname_entry.delete(0, 'end')
        site_entry.delete(0, 'end')
        department_entry.delete(0, 'end')
        idsap_entry.delete(0, 'end')

    root_manage = tk.Tk()
    root_manage.title("Manage Data")
    root_manage.geometry("1500x500")

    treeview = ttk.Treeview(root_manage, columns=('ID', 'IDCard', 'Lastname', 'Firstname', 'Site', 'Department', 'IDSAP'), show='headings')
    treeview.heading('ID', text='ID')
    treeview.heading('IDCard', text='ID Card')
    treeview.heading('Lastname', text='Lastname')
    treeview.heading('Firstname', text='Firstname')
    treeview.heading('Site', text='Site')
    treeview.heading('Department', text='Department')
    treeview.heading('IDSAP', text='IDSAP')
    treeview.pack(fill='both', expand=True)

    display_data()

    display_data_button = tk.Button(root_manage, text="Display Data", command=display_data, bg="lightblue")
    display_data_button.pack(side='left', padx=5, pady=5)

    tk.Label(root_manage, text="ID Card:").pack(side='left', padx=5, pady=5)
    id_card_entry = tk.Entry(root_manage)
    id_card_entry.pack(side='left', padx=5, pady=5)
    tk.Label(root_manage, text="Lastname:").pack(side='left', padx=5, pady=5)
    lastname_entry = tk.Entry(root_manage)
    lastname_entry.pack(side='left', padx=5, pady=5)
    tk.Label(root_manage, text="Firstname:").pack(side='left', padx=5, pady=5)
    firstname_entry = tk.Entry(root_manage)
    firstname_entry.pack(side='left', padx=5, pady=5)
    tk.Label(root_manage, text="Site:").pack(side='left', padx=5, pady=5)
    site_entry = tk.Entry(root_manage)
    site_entry.pack(side='left', padx=5, pady=5)
    tk.Label(root_manage, text="Department:").pack(side='left', padx=5, pady=5)
    department_entry = tk.Entry(root_manage)
    department_entry.pack(side='left', padx=5, pady=5)
    tk.Label(root_manage, text="IDSAP:").pack(side='left', padx=5, pady=5)
    idsap_entry = tk.Entry(root_manage)
    idsap_entry.pack(side='left', padx=5, pady=5)

    add_person_button = tk.Button(root_manage, text="Add Person", command=add_person, bg="lightgreen")
    add_person_button.pack(side='left', padx=5, pady=5)
    delete_person_button = tk.Button(root_manage, text="Delete Person", command=delete_person, bg="salmon")
    delete_person_button.pack(side='left', padx=5, pady=5)
    edit_person_button = tk.Button(root_manage, text="Edit Person", command=edit_person, bg="lightyellow")
    edit_person_button.pack(side='left', padx=5, pady=5)

    info_button = tk.Button(root_manage, text="ℹ", command=display_info, bg="lightyellow")
    info_button.pack(side='left', padx=5, pady=5)

    root_manage.mainloop()

def connect_window():
    default_host = "127.0.0.1"

    root_conn = tk.Tk()
    root_conn.title("Connect to Database")
    root_conn.geometry("300x200")

    tk.Label(root_conn, text="User:").grid(row=0, column=0)
    tk.Label(root_conn, text="Password:").grid(row=1, column=0)
    tk.Label(root_conn, text="Database:").grid(row=2, column=0)

    user_entry = tk.Entry(root_conn)
    user_entry.grid(row=0, column=1)
    password_entry = tk.Entry(root_conn, show="*")
    password_entry.grid(row=1, column=1)
    database_entry = tk.Entry(root_conn)
    database_entry.grid(row=2, column=1)

    connect_button = tk.Button(root_conn, text="Connect",
                               command=lambda: connect_to_database(user_entry.get(), password_entry.get(),
                                                                   database_entry.get(), root_conn), bg="lightblue")
    connect_button.grid(row=3, column=0, columnspan=2)

    root_conn.mainloop()

if __name__ == "__main__":
    connect_window()
