import sqlite3
import os

def create_database():
    if os.path.exists("students.db"):
        os.remove("students.db")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE Students (
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        age INTEGER,
        email VARCHAR UNIQUE,
        city VARCHAR)
    
    ''')

    cursor.execute('''
    CREATE TABLE Courses(
        id INTEGER PRIMARY KEY,
        course_name VARCHAR NOT NULL,
        instructor_name TEXT,
        credits INTEGER)
    ''')


def insert_sample_data(cursor):
    students = [
        (1, 'Alice Johnson', 20, 'alice@gmail.com', 'New York'),
        (2, 'Bob Smith', 19, 'bob@gmail.com', 'Chicago'),
        (3, 'Carol White', 21, 'carol@gmail.com', 'Boston'),
        (4, 'David Brown', 20, 'david@gmail.com', 'New York'),
        (5, 'Emma Davis', 22, 'emma@gmail.com', 'Seattle'),

    ]
    cursor.executemany("INSERT INTO Students VALUES (?, ?, ?, ?, ?)", students)

    courses = [
        (1, 'Python Programming', 'Dr. Anderson',3),
        (2, 'Web Development', 'Prof. Wilson', 4),
        (3, 'Data Science', 'Dr. Taylor', 3),
        (4, 'Mobile Apps', 'Prof. Garcia', 2)

    ]
    cursor.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?)", courses)

    print("Sample data inserted successfully")



def basic_sql_operations(cursor):
    #1) SELECT ALL:
    print("---------------------SELECT ALL -----------------------")
    cursor.execute("SELECT * FROM Students")
    # dataları almak için bir fonksiyon daha yazmamız lazım fetch olarak:
    records = cursor.fetchall()
    for row in records:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}, City: {row[4]}")

    #2) SELECT COLUMNS:
    print("---------------------SELECT COLUMNS -----------------------")
    cursor.execute("SELECT name, age FROM Students ")
    records = cursor.fetchall()
    print(records) #tuple halinde sadece isim yaş gelir

    # 3) WHERE CLAUSE:
    print("---------------------WHERE AGE = 20 -----------------------")
    cursor.execute("SELECT * FROM Students WHERE age = 20")
    records = cursor.fetchall()
    for row in records:
        print(row)

    # 4) WHERE with STRING:
    print("---------------------WHERE city = New York -----------------------")
    cursor.execute("SELECT * FROM Students WHERE city = 'New York'")
    records = cursor.fetchall()
    for row in records:
        print(row)

    # 5) ORDER BY:
    print("---------------------Order by age -----------------------")
    cursor.execute("SELECT * FROM Students ORDER BY age")
    records = cursor.fetchall()
    print(records)

    # 6) LIMIT:
    print("---------------------LIMIT BY 3 -----------------------")
    cursor.execute("SELECT * FROM Students LIMIT 3")
    records = cursor.fetchall()
    for row in records:
        print(row)



def sql_update_delete_insert_operations(conn,cursor):
    #1) INSERT
    cursor.execute("INSERT INTO Students VALUES (6, 'Frank Miller', 23, 'frank@gmail.com', 'Miami')")
    conn.commit() #bunu da yazdık çünkü insert ettğimiz yeni kaydı delete, set gibi işlemlerle değiştirmeye çalışacağım
    #Eğer commit etmeden insert ettiğim şeyi değiştirmeye çalışırsam db'e işlenmemiş olur

    #2) UPDATE
    cursor.execute("UPDATE Students SET age = 24 WHERE id = 6")
    conn.commit() #hemen update işlemini yapsın diye

    #3) DELETE
    cursor.execute("DELETE FROM Students WHERE id = 6")
    conn.commit()



def aggregate_functions(cursor):
    #1) COUNT: Belirli bir koşula uyan satır sayısını sayar. Örneğin, bir müşterinin siparişlerinin sayısını bulmak için kullanılabilir.
    print("------------------COUNT FUNCTION-----------------------")
    cursor.execute("SELECT COUNT(*) FROM Students ") #studentsdaki her şeyi al sayısını söyle demek
    result = cursor.fetchone() #çıktıda fetchone tek bir tane tuple verir liste vermez
    print(result[0])

   #2) AVG():Veritabanındaki sayısal değerlerin ortalama değerini hesaplar.
    print("------------------AVERAGE FUNCTION-----------------------")
    cursor.execute("SELECT AVG(age) FROM Students")
    result = cursor.fetchone() #bir tane değer geleceği için fetchone daha iyidir
    print(result[0])

    #3) MAX - MIN: eritabanındaki sayısal veya metinsel değerler arasında en büyük/en küçük değeri bulur.
    print("------------------MAX-MIN FUNCTION-----------------------")
    cursor.execute("SELECT MAX(age), MIN(age) FROM Students")
    result = cursor.fetchone()
    print(result) #result[0] alırsak bize sadece max olan 22 verir ama bu şekilde alırsak (22,19) verir
    #bu alttaki gibi tanımlayıp tek tek ekrana da yazdırabilirdik:
    # max_age, min_age = result
    # print(max_age)
    # print(min_age)

    #4) GROUP BY: erileri belirli bir kritere göre gruplar ve her grup için bir veya daha fazla Aggregate fonksiyonu uygular
    print("-----------------GROUP BY FUNCTION-----------------------")
    #Hangi şehirden kaç öğrenci var öğrenmek istiyorum
    cursor.execute("SELECT city, COUNT(*) FROM Students GROUP BY city ")
    result = cursor.fetchall()
    print(result)



# ----------------- SORULAR------------------------------
def answers(cursor):
    print("-----------QUESTION 1-------------")
    # 1) Bütün kursların bilgilerini getirin
    cursor.execute("SELECT * FROM Courses")
    record = cursor.fetchall()
    for row in record:
        print(row)


    print("----------- QUESTION 2--------------")
    #2) Sadece eğitmenlerin ismini ve ders ismi bilgilerini getirin
    cursor.execute("SELECT instructor_name, course_name FROM Courses")
    record = cursor.fetchall()
    for row in record:
        print(f"Instructor Name: {row[0]}, Course Name: {row[1]}")

    print("----------- QUESTION 3--------------")
    #3) Sadece 21 yaşındaki öğrencileri getirin
    cursor.execute("SELECT * FROM Students WHERE age = 21")
    record = cursor.fetchall()
    for row in record:
        print(row)

    print("----------- QUESTION 4--------------")
    #4) Sadece Chicago'da yaşayan öğrencileri getirin
    cursor.execute("SELECT * FROM Students WHERE city = 'Chicago'")
    record = cursor.fetchall()
    print(record)

    print("----------- QUESTION 5--------------")
    # 5) Sadece 'Dr. Anderson' tarafından verilen dersleri getirin
    cursor.execute("SELECT instructor_name,course_name FROM Courses WHERE instructor_name = 'Dr. Anderson'")
    record = cursor.fetchall()
    print(record)

    print("----------- QUESTION 6--------------")
    #  6) Sadece ismi 'A' ile başlayan öğrencileri getirin
    cursor.execute("SELECT * FROM Students WHERE name LIKE 'A%'")
    record = cursor.fetchall()
    for row in record:
        print(row)

    print("----------- QUESTION 7--------------")
    #  Sadece 3 ve üzeri kredi olan dersleri getirin
    cursor.execute("SELECT course_name,credits FROM Courses WHERE credits >= 3")
    record = cursor.fetchall()
    print(f"Course Name: {record}")

    print("----------- QUESTION 8--------------")
    # 1) Öğrencileri alphabetic şekilde dizerek getirin
    cursor.execute("SELECT * FROM Students ORDER BY name")
    record = cursor.fetchall()
    for row in record:
        print(row)

    print("----------- QUESTION 9--------------")
    # 2) 20 yaşından büyük öğrencileri, ismine göre sıralayarak getirin
    cursor.execute("SELECT name,age FROM Students WHERE age > 20 ORDER BY name")
    record = cursor.fetchall()
    for row in record:
        print(row)

    print("----------- QUESTION 10--------------")
    #3) Sadece 'New York' veya 'Chicago' da yaşayan öğrencileri getirin
    cursor.execute("SELECT name,city FROM Students WHERE city IN('New York', 'Chicago')")
    record = cursor.fetchall()
    for row in record:
        print(row)

    print("----------- QUESTION 11--------------")
    # 4) Sadece 'New York' ta yaşamayan öğrencileri getirin
    cursor.execute("SELECT name,city FROM Students WHERE city != 'New York' ")
    record = cursor.fetchall()
    for row in record:
        print(row)



def main():
    conn, cursor = create_database()
    try:
        create_tables(cursor)
        insert_sample_data(cursor)
        basic_sql_operations(cursor)
        sql_update_delete_insert_operations(conn,cursor)
        aggregate_functions(cursor)
        answers(cursor)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


#eğer bu python dosyası kendi başına çalıştırılıyorsa, yani başka bir yerden paket gibi değil de kendi başına çalıştıırlıyorsa
#direkt altındaki fonksiyonu çalıştırarak başlar.
if __name__ == "__main__":
    main()