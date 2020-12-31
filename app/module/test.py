a = [1, 2, 3, 4, 5, 6, 11, 12, 13, 21, 22, 23, 191, 192, 193, 31, 32, 33, 41, 42, 43, 51, 52, 53, 54, 61, 62, 63, 65, 64, 66, 67, 71, 72, 73, 74, 75, 81, 82, 83, 91, 92, 93, 111, 112, 113, 121, 122, 123, 131, 132, 133, 141, 142, 143, 144, 151, 152, 153, 154, 161, 162, 163, 163, 181, 182]

# print(a)
# print(b)
c = True
d = False
# a.Find(item => item.name == "foo").value;

def t(a):
    b= ([-2], [1, 1])
    or_list = b[0]
    and_list = b[1]
    print(and_list)
    for i in or_list:
        if i in a:
            return True
    c = True
    for i in and_list:
        print(i)
        if not i in a:
            c = False
    return c

print(t(a))
