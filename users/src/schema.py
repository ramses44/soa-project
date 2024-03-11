from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length, Regexp, Email

DateValidator = lambda: Regexp(r"^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$")
PhoneValidator = lambda: Regexp(r"(\+)[1-9]{1,3} [0-9]{10}")

class UserAuthData(Schema):
    username = String(required=True, validate=Length(max=32), 
                      metatdata={'description': 'username for authentification in the system'})
    
    password = String(required=True, validate=Length(min=8),
        metatdata={'description': 'User\'s password'}
     )
    

class UserProfileData(Schema):
    first_name = String(required=False, validate=Length(max=64), 
                        metatdata={'description': 'First name for user\'s profile'})
    
    second_name = String(required=False, validate=Length(max=64), 
                         metatdata={'description': 'Second name for user\'s profile'})
    
    birth_date = String(required=False, validate=DateValidator(), 
                        metatdata={'description': 'Date of birth for user\'s profile'})
    
    email = String(required=False, validate=Email(), 
                   metatdata={'description': 'E-mail for user\'s profile'})
    
    phone = String(required=False, validate=PhoneValidator(), 
                   metatdata={'description': 'Phone number for user\'s profile'})
    

class AuthResponseHeaders(Schema):
    set_session = String(data_key='Set-Cookie: ...', metadata={'description': 'Set authentification session'})
