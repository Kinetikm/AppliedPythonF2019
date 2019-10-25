def isvalid(field, value):
    if field == 'Departure(GMT)' or field == 'Arrival(GMT)' or field == 'Travel time':
        if type(value) == int and value > 0:
            return True
    else:
        if type(value) == str:
            return True
    return False
