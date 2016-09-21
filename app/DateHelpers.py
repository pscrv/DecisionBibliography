import datetime


def EndOfThisMonth(dt:datetime):
    next_month = dt.replace(day=28) + datetime.timedelta(days=4)   # enough to get to the next month, no matter where we start
    return next_month - datetime.timedelta(days=next_month.day)

def FirstOfNextMonth(dt:datetime):
    next_month = dt.replace(day=28) + datetime.timedelta(days=4)   # enough to get to the next month, no matter where we start        
    return next_month.replace(day=1)

def FirstOfThisMonth(dt:datetime):       
    return dt.replace(day=1)

def MonthIterator(fromdt:datetime, todt:datetime):
    current = FirstOfThisMonth(fromdt)
    while current < todt:
        yield current
        current = FirstOfNextMonth(current)

def FirstOfThisYear(dt:datetime):
    return dt.replace(day=1, month=1)

def FirstOfNextYear(dt:datetime):
    return dt.replace(day=1, month=1, year=dt.year +1)

def EndOfThisYear(dt:datetime):
    return FirstOfNextYear(dt) - datetime.timedelta(days=1)

def YearIterator(fromdt:datetime, todt:datetime):
    current = FirstOfThisYear(fromdt)
    while current < todt:
        yield current
        current = FirstOfNextYear(current)

def MonthIteratorOneYear(dt:datetime):
    return MonthIterator(FirstOfThisYear(dt), EndOfThisYear(dt))