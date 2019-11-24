key = 100

phrase = [['test', True, []], ['another', True, []]]

phrase[-1][0] = phrase[-1][0] + chr(key)
print(phrase[-1][0])