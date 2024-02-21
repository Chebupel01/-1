def function(string):
    sp = []
    for i in string:
        brackets = {')': '(', ']': '[', '}': '{'}
        if i in brackets.values():
            sp.append(i)
        elif i in brackets.keys() and not sp or brackets[i] != sp.pop():
            return False
    return True


result = function(input())
print(result)
