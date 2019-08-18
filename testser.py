#/usr/bin/python3
import serial
import libscrc
import modbus_tk
import crcmod
import binascii
from binascii import *
from crcmod import *
import tkinter
import array
ser = serial.Serial('/dev/ttyUSB1', 9600)


def crc16Add(read):
    crc16 =crcmod.mkCrcFun(0x18005,rev=True,initCrc=0xFFFF,xorOut=0x0000)
    data = read.replace(" ","")
    readcrcout=hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2,'0')      # 位数不足补0
    crc_data = "".join(str_list)
    print(crc_data)
    read = read.strip()+' '+crc_data[4:]+' '+crc_data[2:4]
    print('CRC16校验:',crc_data[4:]+' '+crc_data[2:4])
    print('增加Modbus CRC16校验：>>>',read)
    return read


def modbus_send(addr,feature,start_addr,length):
    read_length=length*2+5
    space=' '
    AD=str(addr)
    FE=str(feature)
    ST=str(start_addr)
    LE=str(length)
    ADI=hex(int(AD))
    FEI=hex(int(FE))
    STI=hex(int(ST))
    LEI=hex(int(LE))
    ADIL=ADI.partition('0x')
    FEIL=FEI.partition('0x')
    STIL=STI.partition('0x')
    LEIL=LEI.partition('0x')
    ADS=ADIL[-1]
    FES=FEIL[-1]
    STS=STIL[-1]
    LES=LEIL[-1]
    ADSD=ADS.zfill(2)
    FESD=FES.zfill(2)
    STSD=STS.zfill(4)
    LESD=LES.zfill(4)
    STSDH=STSD[0]+STSD[1]
    LESDH=LESD[0]+LESD[1]
    STSDL=STSD[-2]+STSD[-1]
    LESDL=LESD[-2]+LESD[-1]
    crc_c=ADSD+space+FESD+space+STSDH+space+STSDL+space+LESDH+space+LESDL
    if __name__ == '__main__':
        send=crc16Add(crc_c)
    send_l=send.split()
    crc_cl=crc_c.split()
    #ser.write(chr(I).encode('utf=8'))
    for i in send_l:
        ser.write(binascii.a2b_hex(i))
    return length


def data_decode(start_addr,data_rl,leng) :
    data_nde=""
    if(start_addr==5):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==37):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==45):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==65):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==85):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==165):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr==197):
        data_nde=data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)+data_rl.pop(0)
    elif(start_addr<255):
        for j in range(leng):
            data_nde=data_nde+data_rl.pop(0)
    return data_nde

def data_part(data_resived):
    print(data_resived)
    data_r=binascii.b2a_hex(data_resived).decode('ascii')
    print(data_r)
    data_rl=[]
    rj=0
    for j in range(int(0.5*len(data_r))):
        data_rl.append(data_r[rj:rj+2])
        rj=rj+2
    return data_rl
def data_check(data_rl):
    i=0
    data_check=''
    for i in range(len(data_rl)-2):
        data_check=data_check+data_rl[i]+' '
        print(data_check)
    data_resive=data_check+data_rl[-2]+' '+data_rl[-1]
    if __name__ == '__main__':
        data_crc=crc16Add(data_check)
    print(data_crc)
    if(data_resive==(data_crc)):
        data_check_result=0
    else:
        data_check_result=1
    return data_check_result
'''a=input()
b=input()
c=input()
d=input()
ai=int(a,base=16)
bi=int(b,base=16)
ci=int(c,base=16)
di=int(d,base=16)'''
length=modbus_send(0x01, 0x03, 0x0015, 0x0002)
read_length=length*2+5


data_resived=ser.read(read_length)

data_rl=data_part(data_resived)
print(data_rl)

data_check_result=data_check(data_rl)
print(data_check_result)
addr=data_rl.pop(0)
feature=data_rl.pop(0)
lengt=data_rl.pop(0)
leng=int(lengt)

data_nde=data_decode(0x03, data_rl, leng)

print(data_nde)
crc=data_rl.pop(0)+data_rl.pop(0)



data_read=int(data_nde,base=16)/10000

print(addr)
print(feature)
print(lengt)
print(data_nde)
print(crc)
print(data_read)






