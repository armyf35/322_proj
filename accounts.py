

from asyncio.windows_events import NULL

from flask_login import UserMixin


class AllUser(UserMixin):
     def __init__(self, id, email, password, firstname, lastname):
         self.id = id
         self.email = email
         self.password = password
         self.phoneNumber = 0000000000
         self.firstname = firstname
         self.lastname = lastname
         self.userType = 0
         self.authenticated = False
    
     def _init_(self, id):
        self.id = id

     def is_active(self):
         return self.is_active()
     def is_anonymous(self):
         return False
     def is_authenticated(self):
         return self.authenticated
     def is_active(self):
          return True
     def get_id(self):
          return self.id
     def getUserType(self):
          return self.userType

     def changeID(self, id):
          self.id = id
     def changeEmail(self, id):
          self.id = id
     def changePassword(self, id):
         self.id = id
     def changePhoneNumber(self, id):
          self.id = id
     def changeUserType(self, userType):
          self.userType = userType

     def getName(self):
               return self.firstname + ' ' + self.lastname
     def getID(self):
          return self.id
     def getEmail(self):
          return self.email
     def getPassword(self):
          return self.password
     def getPhoneNumber(self):
          return self.phoneNumber
     def getFirstName(self):
          return self.firstname
     def getLastName(self):
          return self.lastname

class OrdinaryUser(AllUser):
     def __init__(self):
          AllUser.__init__(self)
          self.userType = 1


     
    
         
