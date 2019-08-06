import os, sys
import pyaes
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from pymsgbox import *
from Crypto import Random
from Crypto.Cipher import AES

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-6], 'wb') as f:
        f.write(dec)

def decrypt_file_pyaes(file_name, key):
    aes = pyaes.AESModeOfOperationCTR(key)

    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    dec = aes.decrypt(plaintext)
    with open(file_name[:-6], 'wb') as fo:
        fo.write(dec)

def rename_file(file_name):
    os.rename(file_name, file_name[:-6])

def dec_key():
    key = password(text='Please enter your decryption key', title='Enter Key', mask ='*')
    if key == None or key == '':
        messagebox.showwarning('Error', 'No key given. Canceled...')
        return False
    return key

def dec_path():
    path = askdirectory(title = 'Select directory with files to decrypt')
    if path == None or path == '':
        messagebox.showwarning('Error', 'No path selected, exiting...')
        return False
    path =  path + '/'
    return path

def decrypt_files():
      ask = confirm(text='What type of encryption are we dealing with?', buttons=['PyCrypto', 'PyAES', 'Ghost', "I don't know"])
      if ask == "I don't know":
          messagebox.showinfo('Encryption type detection', 'Comming Soon!\n\nIf you really dont know, test it on one file first.')
          return

      if ask == 'Ghost':
          pass
      else:
          key = dec_key()
          key = key.encode('utf-8')
          if key == False:
              return

      p = dec_path()
      if p == False:
          return

      a = messagebox.askokcancel('WARNING', 'This tool will decrypt your files with the given key.\n\nHowever, if your key or method is not correct, your (encrypted) files will return corrupted.\n\n You might want to make a backup!')
      if a == True:
          pass
      else:
          return

      try:
          counter = 0
          for path, subdirs, files in os.walk(p):
              for name in files:
                  if name.endswith(".DEMON"):
                      if ask == 'PyCrypto':
                          decrypt_file(os.path.join(path, name), key)
                          print("[Decrypted] %s" % name)
                          counter+=1
                          os.remove(os.path.join(path, name))
                      elif ask == 'PyAES':
                          print("[Decrypting] %s" % name)
                          decrypt_file_pyaes(os.path.join(path, name), key)
                          counter+=1
                          os.remove(os.path.join(path, name))
                      elif ask == 'Ghost':
                          rename_file(os.path.join(path, name))
                          print("[RENAMED] %s" % name)
                          counter+=1
                  elif name == 'README.txt':
                      os.remove(os.path.join(path, name))
                      print('[DELETED] %s/%s' % (path, name))
                  else:
                      print("[Skipped] %s" % name)
          print("\n[DONE] Decrypted %i files" % counter)

      except KeyboardInterrupt:
          print("\nInterrupted!\n")
          sys.exit(0)
      except Exception as e:
          print("\n[ ERROR ] %s" % e)
          sys.exit(1)

Tk = Tk()
Tk.withdraw()

decrypt_files()
