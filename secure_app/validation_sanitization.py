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


    return True


def select_validation(select_val):

    print(select_val)

    if select_val=="friends" or select_val=="public":
        return True
    return False

def checkbox_validation(check_input):

    print(check_input)

    if check_input!="on" and check_input!=None:
        return False
    return True