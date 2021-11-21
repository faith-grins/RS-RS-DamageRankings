with open(r'C:\Users\alanb\Desktop\stylenames.txt', 'r') as input_file:
    names = [i.strip() for i in input_file.read().split('\n')]
names.sort(key=str.__len__)
for i in range(50):
    print(names[-(i+1)])
