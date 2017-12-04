from PyCRC.CRC16 import CRC16

n = ['\x10', '\x21', '\x11', '\xd9', '\x99']    #nhap gia tri hexa duoi sang string 

# phep tinh + trong mang se gan cac phan tu thanh 1 string,con insert hay pop thi no se dua vao tung phan tu trong mang( co nghia co nhieu string
i = n[0] + n[1] + n[2] + n[3] + n[4] 
a = (CRC16().calculate(i))

b = i[3] 
c = ord(b) # chuyen b tu string sang gia tri number 5*****
d = hex(c)
e = int(d, 16 )
print(hex(ord(b)))
print((c))                      #chuyen sang gia tri hexa 
print(e)
print(hex(a))                      #chuyen sang gia tri hexa 
print(a)

if a == 0:
    print ("ok")
else:
    print ("don't ok") 
