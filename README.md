# ZIP-SPAM 🔓

**Written 100% in Python** 🐍

A simple Python tool designed to brute-force and recover passwords for protected ZIP and PDF files using a wordlist.

## 🚀 Usage / طريقة الاستخدام

Run the script using the following command structure:
```bash
python un-zip.py <ZIP | PDF> <files.zip> <files.txt>
📋 Parameters Explanation / شرح الأوامر
<ZIP | PDF>: Specify the target file type you want to unlock (write either ZIP for compressed archives or PDF for document files).
<files.zip>: Enter the name or path of the locked target file (e.g., secret.zip or document.pdf).
<files.txt>: Enter the name or path of the wordlist file containing the passwords to test (e.g., passwords.txt).
💡 Example / مثال تطبيقي

 ZIP ==> python un-zip.py ZIP secret.zip passwords.txt
 PDF ==> python un-zip.py PDF secret.pdf passwords.txt
