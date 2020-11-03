# compare a single character
def compare_char(reg_exp, str_) -> bool:
    return reg_exp == str_ or bool(reg_exp == '.' and str_) or not reg_exp


# compare two strings of equal length
def compare_string(reg_exp, string) -> bool:
    if not reg_exp or (reg_exp == '$' and not string):  # check for end-pattern '$'
        return True
    if not string:
        return False

    if len(reg_exp) > 1 and reg_exp[0] == '\\':
        return compare_char(reg_exp[1], string[0])

    # '?' zero or one wildcard
    if len(reg_exp) > 1 and reg_exp[1] == '?':
        return compare_string(reg_exp[2:], string) or compare_string(reg_exp[2:], string[1:])

    # '*' zero or more wildcard
    if len(reg_exp) > 1 and reg_exp[1] == '*':
        return compare_string(reg_exp[2:], string) or compare_string(reg_exp, string[1:])

    # '+' one ore more wildcard
    if len(reg_exp) > 1 and reg_exp[1] == '+':
        return compare_string(reg_exp.replace('+', '*', 1), string[1:])

    # regular character comparison
    if compare_char(reg_exp[0], string[0]):
        return compare_string(reg_exp[1:], string[1:])
    return False


# compare regex with longer strings
def regex(reg_exp, str_) -> bool:
    if not reg_exp:
        return True
    if not str_:
        return False
    if reg_exp[0] == '^':  # check for begin-pattern '^'
        return compare_string(reg_exp[1:], str_)
    if compare_string(reg_exp, str_):
        return True
    return regex(reg_exp, str_[1:])


print(regex(*input().split('|')))
