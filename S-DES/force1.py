from tkinter import messagebox

from gui import input_text, ascii_var, output_text


def brute_force_attack(ciphertext, decrypt_function):
    for possible_key in range(256):  # 假设密钥是一个字节（0-255之间的值）
        decrypted_message = decrypt_function(ciphertext, possible_key)

        # 在这里，您可以添加进一步的逻辑来判断解密是否成功
        # 例如，检查解密后的消息是否包含常见的单词或短语
        # 或者使用其他方法来验证解密是否正确

        # 如果解密成功（根据您的判断条件），则返回解密后的消息和密钥
        if is_decryption_successful(decrypted_message):
            return decrypted_message, possible_key

    # 如果未找到正确的密钥，可以返回一个错误消息或者抛出异常
    raise Exception("Brute force attack failed. Correct key not found.")

# 示例的解密函数
def decrypt_function(ciphertext, key):
    # 这是一个示例解密函数，根据密钥将密文解密为明文
    decrypted_message = ""
    for char in ciphertext:
        decrypted_char = chr(ord(char) ^ key)
        decrypted_message += decrypted_char
    return decrypted_message

# 示例的判断解密是否成功的函数
def is_decryption_successful(decrypted_message):
    # 这是一个示例判断解密是否成功的函数
    # 您可以根据实际情况来定义判断条件
    # 这里只是一个简单示例
    return "成功的标志" in decrypted_message

# 在您的应用程序中调用brute_force_attack函数并处理结果
def brute_force_attack(tk=None, decrypt_function_ascii=None, decrypt_function_binary=None):
    ciphertext = input_text.get("1.0", tk.END).strip()
    is_ascii = ascii_var.get()

    try:
        if is_ascii:
            decrypted_message, key = brute_force_attack(ciphertext, decrypt_function_ascii)
        else:
            decrypted_message, key = brute_force_attack(ciphertext, decrypt_function_binary)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Decrypted Message: {decrypted_message}\nKey: {key}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
