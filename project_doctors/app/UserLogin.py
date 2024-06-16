class UserLogin: # класс для реалищации логина в системе
    def fromDB(self, user_id, db): # функция для получения данных из бд
        self.__user = db.getUser(user_id)  # само получение
        return self # возвращаем полученное
    
    def create(self, user): # функция cоздания
        self.__user = user # обозначение юзера в системе более защищенным
        return self # возвращаем юзера

    def is_authenticated(self): # функция проверка авторизации
        return True # подвержение правдой
    
    def is_active(self): # функция автиный ли юзер сейчас
        return True # подвержение правдой
    
    def is_anonymous(self): # функция проверки юзер не авторизирован ли он
        return False # возращение лжи
     
    def get_id(self): # функция получения айди
        return str(self.__user[0]) # возрат айди

    def get_role(self): # функция получения роли
        if len(self.__user) > 5: # проверка длины юзера
            return self.__user[5] # в лучшем случае отдаем соответствующую информацию по данному индексу
        return None # или возращаем ничего
