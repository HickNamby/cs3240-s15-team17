import os, random, struct
from Crypto.Cipher import AES
import uuid
def encrypt_file(key, targetFile, outputFile=None, chunksize=1024):
    if not outputFile:
        outputFile = input("Name your encrypted file:\n")+".enc"
    # iv=16 * '\x00'
    preIV=uuid.uuid1()
    preIV=preIV.urn
    preIV=preIV[9:25]
    # iv="asdfasdfasdfasdf"
    iv = preIV.encode(encoding='utf-8')

    encryptor = AES.new(key, AES.MODE_CBC, iv)
    SizeOfTarget = os.path.getsize(targetFile)

    with open(targetFile, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(struct.pack('<Q', SizeOfTarget))
            # sv=iv.decode(encoding='utf-8')
            # print(iv)
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    while not (len(chunk)%16==0):
                        chunk+= ' '.encode(encoding='utf-8')
                    # chunk += ' ' * (16 - len(chunk) % 16)#if its not a multiple of 16 we add spaces till it is

                outfile.write(encryptor.encrypt(chunk))#encrypt the damn line


def decrypt_file(key, targetFile, outputFile=None, chunksize=1024):
    if not outputFile:
        outputFile = os.path.splitext(targetFile)[0]

    with open(targetFile, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)