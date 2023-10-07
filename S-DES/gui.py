import tkinter as tk
from tkinter import messagebox
from binary import EncryptBinary, DecryptBinary
from ascii import EncryptASCII, DecryptASCII

def encrypt_message():
    plaintext = input_text.get("1.0", tk.END).strip()  # 获取输入文本框的内容
    key = key_entry.get()
    is_ascii = ascii_var.get()

    try:
        if is_ascii:
            ciphertext = EncryptASCII(plaintext, key)
        else:
            ciphertext = EncryptBinary(plaintext, key)
        output_text.delete("1.0", tk.END)  # 清空输出文本框
        output_text.insert(tk.END, ciphertext)
    except:
        messagebox.showerror("Error", "Encryption error. Invalid plaintext or key.")

def decrypt_message():
    ciphertext = input_text.get("1.0", tk.END).strip()  # 获取输入文本框的内容
    key = key_entry.get()
    is_ascii = ascii_var.get()

    try:
        if is_ascii:
            plaintext = DecryptASCII(ciphertext, key)
        else:
            plaintext = DecryptBinary(ciphertext, key)
        output_text.delete("1.0", tk.END)  # 清空输出文本框
        output_text.insert(tk.END, plaintext)
    except:
        messagebox.showerror("Error", "Decryption error. Invalid ciphertext or key.")


# 创建主窗口
window = tk.Tk()
window.title("Encryption and Decryption")

# 创建标签
input_label = tk.Label(window, text="Input:")
key_label = tk.Label(window, text="Key:")
output_label = tk.Label(window, text="Output:")

# 创建输入文本框
input_text = tk.Text(window, width=30, height=5)
key_entry = tk.Entry(window, width=15)
output_text = tk.Text(window, width=30, height=5)

# 创建按钮
encrypt_button = tk.Button(window, text="Encrypt", command=encrypt_message)
decrypt_button = tk.Button(window, text="Decrypt", command=decrypt_message)

# 创建单选按钮和变量，用于选择加解密数据类型
ascii_var = tk.BooleanVar()
ascii_checkbox = tk.Checkbutton(window, text="ASCII Encryption/Decryption", variable=ascii_var)

# 网格布局
input_label.grid(row=0, column=0, pady=5)
input_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

key_label.grid(row=1, column=0, pady=5)
key_entry.grid(row=1, column=1, padx=10, pady=5)

output_label.grid(row=2, column=0, pady=5)
output_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

ascii_checkbox.grid(row=3, column=0, padx=10, pady=5)
encrypt_button.grid(row=4, column=1, padx=10, pady=5)
decrypt_button.grid(row=4, column=2, padx=10, pady=5)

# 运行主窗口循环
window.mainloop()
