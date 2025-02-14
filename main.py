import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import Toplevel, messagebox
import sqlite3
import qrcode
from PIL import Image, ImageTk
from tkinter import Listbox
import segno
from segno import helpers
from io import BytesIO
import os
import pandas as pd
import shutil

selected_item = None

db_dir = 'Bakeshop-QRGen/Database'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

folderPath = "Bakeshop-QRGen/Bakeshop-QRs/"
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

url = "https://forms.office.com/Pages/ResponsePage.aspx?id=cXrbR3HIdUidk4ezLlV0o1c3J_XzFy9MhCrzloauXApUQU1OMVBVUzVCTDRFQzIzQ1kxQVhJNjY3RCQlQCN0PWcu&r702190766a284dfd9e368a99e6448fb9="

def show_message(title, message):
    messagebox.showinfo(
        title=title,
        message=message,
        parent=root 
    )

def delImageExist(img_name):
    if os.path.exists(folderPath+ img_name+".png"):
        os.remove(folderPath+ img_name+".png")
        return True
    
def dataToQr(filename, url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(folderPath+filename+".png")

def generateQr(url, bakeshop):
    newUrl = url + bakeshop
    dataToQr(bakeshop, newUrl)

def edit(event):
    global selected_item
    selected_item = treeview.focus()

# Save data from CSV list
def saveExtracted(storeCode, storeName, index):
    if storeCode and storeName:
        conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO stores (store_code, store_name) VALUES (?, ?)", (storeCode, storeName))
        conn.commit()
        conn.close()

        new_id = len(treeview.get_children()) + 1
        treeview.insert('', 'end', values=(new_id, storeCode, storeName))

        generateQr(url, storeName)
    else:
        if not storeCode:
            missing_field = "store code"
        elif not storeName:
            missing_field = "store name"
        else:
            missing_field = "store code and store name"
        messagebox.showwarning("Input Error", f"Empty store identified at row {index} due to missing {missing_field}.")

# Uploading CSV files
def upload_action():
    def process_csv_file(file_path):
        uploads_dir = "Bakeshop-QRGen/Uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        try:
            destination_path = os.path.join(uploads_dir, os.path.basename(file_path))
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("File Uploaded", f"CSV file successfully uploaded to {destination_path}")
            isUpload = True

            df = pd.read_csv(destination_path, skiprows=0)   
            for i in range(len(df)):
                if df.iloc[:, 0].fillna("").values[i] == "" or df.iloc[:, 1].fillna(""). values[i] == "":
                    # print(f"null value on index {i}")
                    isUpload = False
                    break
            if isUpload is not False:
                for i in range(len(df)):
                    status = inputTrapping(df.iloc[:, 0].values[i], df.iloc[:, 1].fillna("").values[i])
                    if status is not False:
                        saveExtracted(df.iloc[:, 0].values[i], df.iloc[:, 1].fillna("").values[i], i + 1)
                            
                show_message("Extract Bakeshops from CSV", "Bakeshops have been saved.")
                upload_window.destroy()
            else:
             messagebox.showwarning("Warning", "File upload failed due to the presence of incomplete information.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def open_file_dialog():
        file_path = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if file_path:
            if not file_path.endswith(".csv"):
                messagebox.showerror("Invalid File", "Please upload a CSV file only.")
            else:
                process_csv_file(file_path)

    upload_window = tk.Toplevel(root)
    upload_window.title("Upload CSV File")
    upload_window.geometry("400x200")
    
    upload_window.update_idletasks()
    screen_width = upload_window.winfo_screenwidth()
    screen_height = upload_window.winfo_screenheight()
    window_width = 400
    window_height = 200
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    upload_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    upload_window.lift()
    upload_window.grab_set()

    ttk.Label(upload_window, text="Upload a CSV file to proceed:", font=("Arial", 12)).pack(pady=10)
    ttk.Button(upload_window, text="Choose File", command=open_file_dialog).pack(pady=20)
# Store codes and names duplication trapping
def inputTrapping(store_code, store_name):
    try:
        conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
        cursor = conn.cursor()

        # Check for duplicate store code
        cursor.execute("SELECT COUNT(*) FROM stores WHERE store_code = ?", (store_code,))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Duplicate Entry", f"The store code '{store_code}' already exists.")
            return False        
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
# Double click open qr 
def on_row_click(event):
    global selected_item
    selected_item = treeview.focus()
    item_values = treeview.item(selected_item, 'values')
    store_name = item_values[2]
    store_url = url + store_name

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(store_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    img.save(folderPath + "temp_qr.png")

    qr_img = img.resize((300, 300), Image.Resampling.LANCZOS)
    
    modal = Toplevel(root)
    modal.title(f"QR Code for {store_name}")
    modal.geometry("350x350")

    modal.update_idletasks()
    screen_width = modal.winfo_screenwidth()
    screen_height = modal.winfo_screenheight()
    window_width = 350
    window_height = 400
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    modal.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    modal.lift()
    modal.grab_set()

    text_label = ttk.Label(modal, text=f"{store_name.upper()}", font=("Helvetica", 12, "bold"))
    text_label.pack(pady=(10, 10))  

    qr_image = ImageTk.PhotoImage(qr_img)
    
    label = ttk.Label(modal, image=qr_image)
    label.image = qr_image
    label.pack(pady=20)
# Save bakeshop data
def create_action():
    create_window = tk.Toplevel(root)
    create_window.title("Add Store")

    create_window.update_idletasks()
    screen_width = create_window.winfo_screenwidth()
    screen_height = create_window.winfo_screenheight()
    window_width = 250
    window_height = 160
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    create_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    create_window.lift()
    create_window.grab_set()

    # Store code
    store_code_label = tk.Label(create_window, text="Store Code:")
    store_code_label.pack(pady=5, padx=10, anchor='w')
    store_code_entry = tk.Entry(create_window)
    store_code_entry.pack(pady=0, padx=10, anchor='w')

    # Store name
    store_name_label = tk.Label(create_window, text="Store Name:")
    store_name_label.pack(pady=10, padx=10, anchor='w')
    store_name_entry = tk.Entry(create_window)
    store_name_entry.pack(pady=0, padx=10, anchor='w')

    def submit_create():
        store_name = store_name_entry.get()
        store_code = store_code_entry.get()
        if store_name and store_code:
            conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
            cursor = conn.cursor()
            
            status = inputTrapping(store_code, store_name)
            if status != False:
                cursor.execute("INSERT INTO stores (store_code, store_name) VALUES (?, ?)", (store_code, store_name,))
                conn.commit()
                conn.close()

                generateQr(url, store_name)
                show_message("Create Bakeshop QR", "Bakeshop has been saved.")
            
                new_id = len(treeview.get_children()) + 1
                treeview.insert('', 'end', values=(new_id, store_code, store_name))

                create_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a Store Name")

    submit_button = tk.Button(create_window, text="Submit", command=submit_create)
    submit_button.pack(pady=10, padx=10, anchor='w')
# Update bakeshop data
def update_action():
    if selected_item:
        store_id = treeview.item(selected_item, 'values')[0]
        store_code = treeview.item(selected_item, 'values')[1]
        store_name = treeview.item(selected_item, 'values')[2]

        update_window = tk.Toplevel(root)
        update_window.title("Update Store")

        update_window.update_idletasks()
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        window_width = 250
        window_height = 160
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        update_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        update_window.lift()
        update_window.grab_set()

        # Store code
        store_code_label = tk.Label(update_window, text="Store Code:")
        store_code_label.pack(pady=5, padx=10, anchor='w')
        store_code_entry = tk.Entry(update_window)
        store_code_entry.insert(0, store_code)
        store_code_entry.pack(pady=0, padx=10, anchor='w')

        # Store name
        store_name_label = tk.Label(update_window, text="Store Name:")
        store_name_label.pack(pady=5, padx=10, anchor='w')
        store_name_entry = tk.Entry(update_window)
        store_name_entry.insert(0, store_name)
        store_name_entry.pack(pady=0, padx=10, anchor='w')

        def submit_update():
            updated_code = store_code_entry.get()
            updated_name = store_name_entry.get()

            if updated_code and updated_name:
                conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
                cursor = conn.cursor()
                
                # status = inputTrapping(updated_code, updated_name)
                # if status != False:
                cursor.execute("UPDATE stores SET store_code = ?, store_name = ? WHERE id = ?", (updated_code, updated_name, store_id))
                conn.commit()
                conn.close()

                delImageExist(store_name)
                generateQr(url, updated_name)

                show_message("Update Bakeshop", "Bakeshop has been updated.")

                treeview.item(selected_item, values=(store_id, updated_code, updated_name))

                update_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter a Store Name")

        submit_button = tk.Button(update_window, text="Submit", command=submit_update)
        submit_button.pack(pady=10, padx=10, anchor='w')
    else:
        messagebox.showwarning("Selection Error", "Please select a row to update")
# Delete bakeshop data
def delete_action():
    global selected_item
    if selected_item:
        store_id = treeview.item(selected_item, 'values')[0]
        store_name = treeview.item(selected_item,'values')[2]
        confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete store ID {store_id}?")
        if confirm:
            conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
            cursor = conn.cursor()

            delImageExist(store_name)

            cursor.execute("DELETE FROM stores WHERE id = ?", (store_id,))
            conn.commit()
            conn.close()
            
            treeview.delete(selected_item)
            selected_item = None
            
            show_message("Delete Bakeshop", "Bakeshop has been deleted.")
    else:
        messagebox.showwarning("Selection Error", "Please select a row to delete")
# Fetch bakeshop data
def fetch_data():
    # Fetch data from the database and populate the table
    try:
        conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
        cursor = conn.cursor()

        # Fetch all records from the stores table
        cursor.execute("SELECT * FROM stores")
        rows = cursor.fetchall()

        # Insert the data into the treeview
        for row in rows:
            treeview.insert('', 'end', values=row)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
# Searchable table
def create_table():
    global treeview
    treeview_frame = tk.Frame(frame) 
    treeview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  
    
    treeview = ttk.Treeview(treeview_frame, columns=("ID", "Store Code", "Store Name"), show="headings")
    
    treeview.heading("ID", text="ID")
    treeview.heading("Store Code", text="Store Code")
    treeview.heading("Store Name", text="Store Name")
    
    treeview.pack(fill="both", expand=True)
    
    treeview.bind("<Double-1>", on_row_click)
    treeview.bind("<ButtonRelease-1>", edit)

    scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)  # Scrollbar inside the new frame
    treeview.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    fetch_data()

    # Ensure that the database and table exist
    conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
    cursor = conn.cursor()

    # Create the stores table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_code TEXT NOT NULL,
        store_name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
# Db setup
def setup_db():
    conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
    cursor = conn.cursor()

    # Create the stores table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_code TEXT NOT NULL,
        store_name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

root = tk.Tk()
root.title("Bakeshop QR Code Generator")

root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 700
window_height = 500
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Search Frame
search_frame = ttk.Frame(frame)
search_frame.pack(fill=tk.X, padx=5, pady=5)

search_var = tk.StringVar()

ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
search_button = ttk.Button(search_frame, text="Search")
search_button.pack(side=tk.LEFT, padx=5)

# Search Functionality
def search_treeview():
    query = search_var.get().lower()
    treeview.delete(*treeview.get_children())

    conn = sqlite3.connect(f'{db_dir}/BAKESHOPSDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    rows = cursor.fetchall()

    for row in rows:
        if any(query in str(value).lower() for value in row):
            treeview.insert('', 'end', values=row)

    conn.close()

search_button.config(command=search_treeview)

# Buttons at the bottom
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

button1 = tk.Button(button_frame, text="Create", command=create_action)
button1.pack(side=tk.LEFT, padx=10, pady=10)

button2 = tk.Button(button_frame, text="Update", command=update_action)
button2.pack(side=tk.LEFT, padx=10, pady=10)

button3 = tk.Button(button_frame, text="Delete", command=delete_action)
button3.pack(side=tk.LEFT, padx=10, pady=10)

button4 = tk.Button(button_frame, text="Upload", command=upload_action)
button4.pack(side=tk.LEFT, padx=10, pady=10)

setup_db()

create_table()

root.mainloop()