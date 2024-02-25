freq = [0] * 26
print(freq)
with open("/usr/share/dict/words", 'r') as file:
    for line in file:
        for letter in line:
            i = ord(letter) - 97
            if (i >= 0 and i < 26):
                freq[i] = freq[i] + 1

print(freq)
total = 0
for i in range(len(freq)):
    count = freq[i]
    total = total + count
    freq[i] = total
for i in range(len(freq)):
    freq[i] = freq[i] / total
    print(chr(i + 97) + ": " + str(freq[i]))
    
with open("freq", 'w') as output:
    for val in freq:
        print(val, file=output)
