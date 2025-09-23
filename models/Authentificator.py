import bcrypt

class Authentificator:
    def __init__(self, userPwd, pwdToCheck):
        self.userPwd = userPwd
        self.pwdToCheck = pwdToCheck


    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        return hashed.decode('utf-8')

    #fonction pour vérifier le mot de passe
    def authenticate(self) -> bool:
        return bcrypt.checkpw(self.pwdToCheck.encode('utf-8'), self.userPwd.encode('utf-8'))

