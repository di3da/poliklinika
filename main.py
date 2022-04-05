from pydoc import doc
import models
import sqlite3
from hashlib import blake2b

models.CONNECTION = sqlite3.connect('library.db')

def employ():
    print("Введите ФИО работника без сокращений:")
    fio = input()
    print("Введите название должности работника:")
    rank = input()
    print("Введите логин работника:")
    login = input()
    print("Введите пароль работника:")
    password = input().encode()
    h = blake2b(password, digest_size=20).hexdigest()
    print(h)
    print("Выдать пользователю права доктора?(y/n)")
    ch1 = input()
    if ch1 == 'y':
        doc = 1
    elif ch1 == 'n':
        doc = 0
    else:
        doc = 0
    print("Выдать пользователю права регистратора?(y/n)")
    ch2 = input()
    if ch2 == 'y':
        reg = 1
    elif ch2 == 'n':
        reg = 0
    else:
        reg = 0    
    print("Выдать пользователю права администратора(y/n)?")
    ch3 = input()
    if ch3 == 'y':
        adm = 1
    elif ch3 == 'n':
        adm = 0
    else:
        adm = 0
    a = models.User(login, h, doc, reg, adm, fio, rank)
    a.save()
    main(current_user)

def discharge():
    print('Введите полные ФИО увольняемого работника')
    fio = str(input())
    models.User.delete(fio)
    print(fio, 'уволен(а)')

def card():
    pass

def prescription():
    pass

def register():
    print("Введите ФИО пациента без сокращений:")
    fio = input()
    print("Введите дату рождения пациента в формате dd.mm.yyyy:")
    dob = input()
    print("Введите телефонный номер пациента без +7 и 8:")
    cellphone = input()
    print("Введите адрес проживания пациента:")
    adress = input()
    a = models.Patient(fio, dob, cellphone, adress)
    a.save()
    main(current_user)

def visitdoctor():
    print(models.Patient.selectall())
    print("Введите ФИО пациента без сокращений:")
    patient_fio = input()
    print(models.User.selectall())
    print("Введите ФИО доктора без сокращений:")
    doctor_fio = input()
    print("Введите дату приёма:")
    visitdata = input()
    print("Введите время приёма:")
    time = input()
    a = models.Visit(patient_fio, doctor_fio, visitdata, time)
    a.save()
    main(current_user)

def main(current_user):
    print('Добро пожаловать,',current_user[0].rank, current_user[0].fio)
    if int(current_user[0].is_doctor) == 1:
        print('У вас есть права доктора')
    if int(current_user[0].is_register) == 1:
        print('У вас есть права регистратора')
    if int(current_user[0].is_admin) == 1:
        print('У вас есть права администратора')
    print("Введите команду:\nАдминистрация: нанять, уволить\nДоктор: медкарта, рецепт\nРегистратор: прикрепить, прием\nВсе: выйти")
    message = input()
    if message == "нанять" and int(current_user[0].is_admin) == 1:
        employ()
    if message == "уволить" and int(current_user[0].is_admin) == 1:
        discharge()
    elif message == "медкарта" and int(current_user[0].is_doctor) == 1:
        card()
    elif message == "рецепт" and int(current_user[0].is_doctor) == 1:
        prescription()
    elif message == "прикрепить" and int(current_user[0].is_register) == 1:
        register()
    elif message == "прием" and int(current_user[0].is_register) == 1:
        visitdoctor()
    elif message == "выйти":
        exit()
    else:
        print('У вас нет необходимых прав для выполнения этой команды!')
        main(current_user)

def authenticate():
    print("Введите логин:")
    login = input()
    print("Введите пароль:")
    pw = input().encode()
    a = models.User.select(login)
    h = blake2b(pw, digest_size=20).hexdigest()
    print(h)
    if a == []:
        print('Такой пользователь не зарегистрирован')
        authenticate()
    if h == a[0].password:        
        print('Добро пожаловать в систему')
    else:
        print('Неправильный пароль')
        authenticate()
    return a
    


if __name__ == '__main__':
    current_user = authenticate()
    main(current_user)


    