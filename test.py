print('{0:016b}'.format(2**16-1).encode())
print(type('{0:016b}'.format(2**16-1).encode()))
print(2**16-1)

text = "Test 1,2,3. \ "

print(text)
print(len(text))
print(text.encode())
print(len(text.encode()))