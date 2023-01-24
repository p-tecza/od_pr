import re

#validation & sanitization

def replace_html(this_input):
    re.sub("/</g", "&lt", this_input)
    re.sub("/>/g", "&gt;", this_input)
    #new_input = this_input.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return this_input

    
def validate_input(this_input=[]):
    for x in this_input:
        if len(x)>100 or len(x)==0:
            return False
    return True

def name_validate(name_input):
    for s in name_input:
        if not s.isalnum():
            return False
    if len(name_input) < 3:
        return False
    return True

def password_validate(pass_input):
    if len(pass_input)<8:
        return False
    if not any(a.islower() for a in pass_input):
        return False
    if not any(b.isdigit() for b in pass_input):
        return False
    if not any(c.isupper() for c in pass_input):
        return False
    return True

def select_validation(select_val):
    if select_val=="friends" or select_val=="public":
        return True
    return False

def checkbox_validation(check_input):
    if check_input!="on" and check_input!=None:
        return False
    return True

def question_validation(quest_input):
    if not quest_input:
        return False
    return True

def answer_validation(answer_input):
    if not answer_input:
        return False
    return True

def code_validation(code):
    for c in code:
        if not c.islower() and not c.isdigit() and c!='-':
            return False
    if len(code)!=36:
        return False
    return True