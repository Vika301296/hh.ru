def count_average_salary(from_salary=None, to_salary=None):
    if not (from_salary and to_salary):
        return None
    elif from_salary:
        average_salary = int(from_salary * 1.2)
    elif to_salary:
        average_salary = int(to_salary * 0.8)
    else:
        average_salary = int((from_salary + to_salary) / 2)
    return average_salary
