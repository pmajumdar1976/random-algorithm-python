'''
Problem Description:
===================

Commander lambda assigns tasks his minions. Each minion has a id number.
Those id numbers are of length k and digits are in base b.

This is how commander lambda assigns the tasks. He picks up a task and
randomly chooses a minion id n. After miniom n is done with the task,
the commander chooses the next minion for doing this task in the following
way.

He forms a number x by arranging the digits on n in descending order and
forms another number y by arranging the digits on n in ascending order.
The he calculates the next minion id as z = x - y. If the number of digits
in z is less than k then number is padded with 0 in the most significant
positions.

We need to avoid the situation where the task may get re-assigned to a
minion who has already done it. We need to find out after how many
iterations the task will keep coming back to a minion for any random
starting minion id.
'''

def ToInt(digits, b):
    result = 0
    mul    = 1

    for digit in reversed(digits):
        result += int(digit) * mul
        mul    *= b

    return result

def Digitize(num, b, k):
    digits = []
    while (num > 0):
        #print ("num = {}, k = {}".format(num, k))
        digits.append(str(num % b))
        num = int(num / b)
        k -= 1
    while (k > 0):
        #print ("k = {}".format(k))
        digits.append('0')
        k -= 1
    digits.reverse()
    return digits

def ToID (digits):
    return ''.join(digits)

def solution(n, b):
    #Your code here
    z       = ToInt(n, b)
    zDigits = list(n)
    k       = len(zDigits)

    ids     = [z]
    length  = 0
    while (1):
        #print ('zDigits: {}'.format(zDigits))

        xDigits = list(zDigits)
        xDigits.sort(reverse=True)
        #print ('xDigits: {}'.format(xDigits))
        yDigits = list(zDigits)
        yDigits.sort()
        #print ('yDigits: {}'.format(yDigits))

        x = ToInt (xDigits, b)
        #print ('x: {}'.format(x))
        y = ToInt (yDigits, b)
        #print ('y: {}'.format(y))
        z = x - y
        #print ('z: {}'.format(z))

        zDigits = Digitize (z, b, k)
        if z in ids:
            #print ("ID {} got repeated".format(ToID(zDigits)))
            break
        else:
            #print ("Next ID: {}".format(ToID(zDigits)))
            ids.append (z)

    return len(ids) - ids.index(z)

if __name__ == "__main__":
    print ("Cycle Length for ('210022', 3): {}".format(solution ('210022', 3)))
    print ("Cycle Length for ('1211', 10): {}".format(solution ('1211', 10)))
