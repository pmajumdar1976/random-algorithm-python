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
