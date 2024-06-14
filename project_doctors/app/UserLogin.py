class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)  # Изменено с get_user на getUser
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user[0])

    def get_role(self):
        if len(self.__user) > 5:
            return self.__user[5]
        return None
