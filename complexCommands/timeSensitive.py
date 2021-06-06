#removed until use found
'''from datetime import datetime, time
# https://stackoverflow.com/questions/18884017/how-to-check-in-python-if-im-in-certain-range-of-times-of-the-day

timestamp = datetime.datetime.now().time() # Throw away the date information
print (datetime.datetime.now().time() > timestamp) # >>> True (unless you ran this one second before midnight!)

# Or check if a time is between two other times
start = datetime.time(8, 30)
end = datetime.time(15)
print (start <= timestamp <= end) # >>> depends on what time it is

now = datetime.datetime.now()
if 0 <= now.weekday() <= 4:
    print ("It's a weekday!")
print (start <= now.time() <= end) # with start & end defined as above

if 0 <= now.weekday() <= 4:
    print("it's a weekday")
    if time(8, 30) <= now.time() <= time(15):
        print("and it's in range")
'''