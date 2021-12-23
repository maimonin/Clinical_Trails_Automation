def create_satisfy_positive_or_negative_one_choice(testCond_bool_positive):
    return create_satisfy_one_choice("positive" if  testCond_bool_positive else "negative")
def create_satisfy_range(min,max):
    return {"type":"range","value": {"min": min ,"max":max}  }
def create_satisfy_one_choice(value):
    return {"type":"one_choice","value":value}
def create_test_one_choice(name,value):
    return {"test" : name, "satisfy" : create_satisfy_one_choice(value)}
def create_test_range(name,min,max):
    return {"test" : name, "satisfy" : create_satisfy_range(min,max)}
