import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os

d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}


def encrypt_image(image_path, secret_message, password):
    img = cv2.imread(image_path)

    if img is None:
        messagebox.showerror("Error", "Failed to load image.")
        return

    n, m, z = 0, 0, 0

    for i in range(len(secret_message)):
        img[n, m, z] = d[secret_message[i]]
        n += 1
        m += 1
        z = (z + 1) % 3

    encrypted_image_path = os.path.join(
        os.path.dirname(image_path), "encryptedImage.jpg"
    )
    cv2.imwrite(encrypted_image_path, img)

    os.startfile(encrypted_image_path)


def decrypt_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        messagebox.showerror("Error", "Failed to load image.")
        return ""

    message = ""
    n, m, z = 0, 0, 0

    for i in range(255):
        try:
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3
        except IndexError:
            break

    return message


def process_encryption():
    img_path = filedialog.askopenfilename(title="Select Image")
    secret_message = secret_message_entry.get()
    password = password_entry.get()

    if img_path and secret_message and password:
        encrypt_image(img_path, secret_message, password)
        messagebox.showinfo("Success", "Message encrypted successfully!")
        reset_fields()
    else:
        messagebox.showerror("Error", "Please fill all fields!")


def process_decryption():
    img_path = filedialog.askopenfilename(title="Select Stego Image")
    password = password_entry_decrypt.get()

    if img_path and password:
        decoded_message = decrypt_image(img_path)
        if decoded_message:
            decrypted_message_text.delete(1.0, tk.END)
            decrypted_message_text.insert(tk.END, decoded_message)
            messagebox.showinfo("Success", "Decryption successful!")
        else:
            messagebox.showerror("Error", "Decryption failed or no message found.")
        reset_fields()
    else:
        messagebox.showerror("Error", "Please fill all fields!")


def reset_fields():
    secret_message_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    password_entry_decrypt.delete(0, tk.END)
    decrypted_message_text.delete(1.0, tk.END)


app = tk.Tk()
app.title("Steganography Tool")


frame = tk.Frame(app)
frame.pack(pady=20)

option_var = tk.StringVar(value="Encrypt")


tk.Radiobutton(frame, text="Encrypt", variable=option_var, value="Encrypt").pack(
    anchor=tk.W
)

secret_message_entry = tk.Entry(frame)
secret_message_entry.pack(pady=5)
secret_message_entry.insert(0, "Enter secret message")

password_entry = tk.Entry(frame)
password_entry.pack(pady=5)
password_entry.insert(0, "Enter password")

process_button_encrypt = tk.Button(frame, text="Encrypt", command=process_encryption)
process_button_encrypt.pack(pady=10)


tk.Radiobutton(frame, text="Decrypt", variable=option_var, value="Decrypt").pack(
    anchor=tk.W
)

password_entry_decrypt = tk.Entry(frame)
password_entry_decrypt.pack(pady=5)
password_entry_decrypt.insert(0, "Enter password")

process_button_decrypt = tk.Button(frame, text="Decrypt", command=process_decryption)
process_button_decrypt.pack(pady=10)


decrypted_message_text = tk.Text(frame, height=4, width=40)
decrypted_message_text.pack(pady=10)

app.mainloop()
