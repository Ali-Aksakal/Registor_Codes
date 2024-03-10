import string
from random import *
import sqlite3
import datetime

def register_db():
    conn = sqlite3.connect("register_table.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_nickname TEXT, password TEXT, user_name TEXT, user_surname TEXT, mail_address TEXT, zaman DATE)")

    conn.commit()
    conn.close()


def register():
    conn = sqlite3.connect("register_table.db")
    cur = conn.cursor()

    characters = string.ascii_letters + string.punctuation + string.digits
    oto_password = "".join(choice(characters) for i in range(randint(7, 14)))

    while True:
        user_nickname = input("Kullanıcı Adı Giriniz: ")
        if user_nickname == "":
            print("Kullanıcı Adı boş geçilemez!!!")
            continue  # Kullanıcı adını tekrar iste

        # Kullanıcı adı daha önce kulllanılmışmı kontrol et
        cur.execute("SELECT * FROM users WHERE user_nickname=?", (user_nickname,))
        existing_user = cur.fetchone()

        if existing_user:
            print("Bu kullanıcı adı zaten kullanılmış! Lütfen başka bir kullanıcı adı seçin.")
        else:
            break  # kullanılmamışsa döngüden çık

    password = input("Şifre Giriniz(7-14 karakter): ")
    if password == "":
        print(f"Şifreniz {oto_password} olarak belirlenmiştir.")
        password = oto_password
    elif not (7 <= len(password) <= 14):
        print("Şifreniz 7-14 karakter olmalıdır")
        return

    user_name = input("Adınızı Giriniz: ")
    if user_name == "":
        print("Ad boş geçilemez!!!")
        return

    user_surname = input("Soyadınızı Giriniz: ")
    if user_surname == "":
        print("Soyad boş geçilemez!!!")
        return

    mail_address = input("Mail Adresinizi Giriniz: ")
    if mail_address == "":
        print("Mail Adresi boş geçilemez!!!")
        return

    if '@' not in mail_address or '.' not in mail_address:
        print("Hatalı Mail Adresi!!!")
        return

    # Mail adresi daha önce kulllanılmışmı kontrol et
    cur.execute("SELECT * FROM users WHERE mail_address=?", (mail_address,))
    existing_email = cur.fetchone()

    if existing_email:
        print("Bu mail adresi zaten kayıtlı!")
        return

    zaman = datetime.datetime.now()

    cur.execute("INSERT INTO users('user_nickname', 'password', 'user_name', 'user_surname', 'mail_address','zaman') VALUES (?, ?, ?, ?, ?, ?)", (user_nickname, password, user_name, user_surname, mail_address, zaman))

    conn.commit()
    print("Kullanıcı Kayıt Edildi")
    conn.close()

register_db()
register()


