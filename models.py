from datetime import date
from lib2to3.pgen2.pgen import generate_grammar

 
CONNECTION = None

class User():
    SQL_SELECT = '''
        SELECT * from userdata WHERE {} = '{}';
    '''
    SQL_SELECTALL = '''
        SELECT * from userdata;
    '''
    SQL_SELECTFIO = '''
        SELECT * from userdata WHERE fio = '{}';
    '''

    SQL_DELETE = '''
        DELETE * from userdata WHERE fio = '{}';
    '''

    SQL_CREATE = '''
        CREATE TABLE userdata (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_doctor TEXT NOT NULL,
            is_register TEXT NOT NULL,
            is_admin TEXT NOT NULL,
            fio TEXT NOT NULL,
            rank TEXT NOT NULL
        );
    '''
    SQL_INSERT = ''' 
        INSERT INTO userdata (
            login,
            password,
            is_doctor,
            is_register,
            is_admin,
            fio,
            rank
        )
        VALUES(
            "{}",
            "{}",
            "{}",
            "{}",
            "{}",
            "{}",
            "{}"
        ) 
    '''
    
    def __init__(self, 
        login, 
        password, 
        doc, reg, adm, 
        fio, 
        rank):
        cursor = CONNECTION.cursor()
        self.login = login
        self.password = password
        self.is_doctor = doc
        self.is_register = reg
        self.is_admin = adm
        self.fio = fio
        self.rank = rank

    def __repr__(self):
        rep = '\n______________ ' + '\nДоктор ' + str(self.fio) + '\nСпециализация - ' + str(self.rank)
        return rep


    

    def save(self):
        cursor = CONNECTION.cursor()
        # Создать или обновить в базе
        cursor.execute(self.SQL_INSERT.format(
            self.login,
            self.password,
            self.is_doctor,
            self.is_register,
            self.is_admin,
            self.fio,
            self.rank
        ))
        CONNECTION.commit()

    @staticmethod
    def delete(login):
        cursor = CONNECTION.cursor()
        cursor.execute(User.SQL_DELETE.format(login))
        CONNECTION.commit()

    @staticmethod
    def selectall(): 
        cursor = CONNECTION.cursor()
        cursor.execute(User.SQL_SELECTALL)
        result = []   
        for row in cursor.fetchall():
            login = row[0]
            password = row[1]
            doc = row[2]
            reg = row[3]
            adm = row[4]
            fio = row[5]
            rank = row[6]
            user = User(login, password, doc, reg, adm, fio, rank)
            result.append(user)   
        return result 

    @staticmethod
    def select(type, condition):
        cursor = CONNECTION.cursor()
        cursor.execute(User.SQL_SELECT.format(type, condition))
        result = []   
        for row in cursor.fetchall():
            login = row[0]
            password = row[1]
            doc = row[2]
            reg = row[3]
            adm = row[4]
            fio = row[5]
            rank = row[6]
            user = User(login, password, doc, reg, adm, fio, rank)
            result.append(user)   
        return result

class Patient():
    SQL_SELECTALL = '''
        SELECT * from patientdata;
    '''
    SQL_SELECT = '''
        SELECT * from patientdata WHERE fio = '{}';
    '''

    SQL_DELETE = '''
        DELETE * from patientdata WHERE fio = '{}';
    '''

    SQL_CREATE = '''
        CREATE TABLE patientdata (
            fio TEXT PRIMARY KEY,
            dob TEXT NOT NULL,
            cellphone TEXT NOT NULL,
            adress TEXT NOT NULL
        );
    '''
    SQL_INSERT = ''' 
        INSERT INTO patientdata (
            fio,
            dob,
            cellphone,
            adress
        )
        VALUES(
            "{}",
            "{}",
            "{}",
            "{}"
        ) 
    '''


    
    def __init__(self, 
        fio, 
        dob, 
        cellphone, 
        adress):
        cursor = CONNECTION.cursor()
        self.adress = adress
        self.cellphone = cellphone
        self.dob = dob
        self.fio = fio
        

    def __repr__(self):
        rep = '______________' + '\nПациент ' + str(self.fio) + '\nДата рождения - ' + str(self.dob) + '\nНомер телефона - ' + str(self.cellphone) + '\nАдрес - ' + str(self.adress)
        return rep

    def save(self):
        cursor = CONNECTION.cursor()
        cursor.execute(self.SQL_INSERT.format(
            self.fio,
            self.dob,
            self.cellphone,
            self.adress,
        ))
        CONNECTION.commit()

    @staticmethod
    def select(fio):
        cursor = CONNECTION.cursor()
        cursor.execute(Patient.SQL_SELECT.format(fio))
        result = []   
        for row in cursor.fetchall():
            fio = row[0]
            dob = row[1]
            cellphone = row[2]
            adress = row[3]
            patient = Patient(fio, dob, cellphone, adress)
            result.append(patient)   
        return result

    @staticmethod
    def selectall():
        cursor = CONNECTION.cursor()
        cursor.execute(Patient.SQL_SELECTALL)
        result = []   
        for row in cursor.fetchall():
            fio = row[0]
            dob = row[1]
            cellphone = row[2]
            adress = row[3]
            patient = Patient(fio, dob, cellphone, adress)
            result.append(patient)   
        return result
    
class Visit():
    SQL_SELECT = '''
        SELECT * from visit WHERE {} = '{}';
    '''

    SQL_INSERT = ''' 
        INSERT INTO visit (
            patient_fio,
            doctor_login,
            visitdata,
            time,
            note
        )
        VALUES(
            "{}",
            "{}",
            "{}",
            "{}",
            "{}"
        ) 
    '''
    SQL_INSERTNOTE = ''' 
        INSERT INTO visit WHERE id = {} (
            note
        )
        VALUES(
            "{}"
        ) 
    '''

    SQL_CREATE = '''
        CREATE TABLE visit (
            patient_fio TEXT NOT NULL,
            doctor_login TEXT NOT NULL,
            visitdata DATE NOT NULL,
            time TEXT NOT NULL,
            note TEXT,
            id INTEGER PRIMARY KEY
        );
    '''
    def __repr__(self):
        rep = '\n______________ ' + '\nНомер приема ' + str(self.id) + '\nПациент ' + str(self.patient_fio) + '\nДоктор ' + str(User.select('login', self.doctor_login)[0].fio) + '\nДата ' + str(self.visitdate) + '\nВремя ' + str(self.time) + '\nКомментарий ' + str(self.note)
        return rep
    
    def __init__(self, 
        patient_fio, 
        doctor_login, 
        visitdate, 
        time,
        note,
        id
        ):
        cursor = CONNECTION.cursor()
        self.id = None
        self.patient_fio = patient_fio
        self.doctor_login = doctor_login
        self.visitdate = visitdate
        self.time = time
        self.note = note

    def save(self):
        cursor = CONNECTION.cursor()
        cursor.execute(self.SQL_INSERT.format(
            self.patient_fio,
            self.doctor_login,
            self.visitdate,
            self.time,
            self.note
        ))
        CONNECTION.commit()
        print('Номер талона:', self.id)

    def savenote(self, idx, note):
        cursor = CONNECTION.cursor()
        cursor.execute(self.SQL_INSERTNOTE.format(
            idx,
            note
        ))
        CONNECTION.commit()

    @staticmethod
    def select(type, condition):
        cursor = CONNECTION.cursor()
        cursor.execute(Visit.SQL_SELECT.format(type, condition))
        result = []   
        for row in cursor.fetchall():
            patient_fio = row[0]
            doctor_login = row[1]
            visitdata = row[2]
            time = row[3]
            note = row[4]
            idx = row[5]
            user = Visit(patient_fio, doctor_login, visitdata, time, note, idx)
            user.id = idx
            result.append(user)   
        return result

