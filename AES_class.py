import random
import os
class AES:
    @staticmethod
    def createSblock(seed):
        sbox = list(range(256))
        random.seed(seed)
        random.shuffle(sbox)
        return sbox

    @staticmethod
    def invSblock(sbox):
        inv_sbox = [0] * 256
        for i in range(256):
            inv_sbox[sbox[i]] = i
        return inv_sbox

    def __init__(self, key, sbox,invsbox, iv=None):
        self._key = key
        self._sbox = sbox
        self._keys = self.__expancionKeys()
        self._invsbox = invsbox
        if iv == None:
            self._IV = os.urandom(16)
        else:
            self._IV = iv

    def __expancionKeys(self):
        startKey = []
        startKeys = []
        if len(self._key) == 16:
            for i in self._key:
                startKey.append((ord(i)))
        else:
            return
        for i in range(4):
            startKeys.append(list(startKey[i*4 : i*4+4]))
        expancionKeys = startKeys
        for i in range(4,44):
            if i%4!=0:
                roundKey = []
                for x in range(4):
                    roundKey.append(expancionKeys[i-4][x] ^ expancionKeys[i-1][x])
                expancionKeys.append(roundKey)
            else:
                roundKey = []
                readyKey = []
                for x in range(4):
                    roundKey.append(self.__SubWord(self.__RotWord(expancionKeys[i-1]),self._sbox)[x])
                roundKey[0] ^= self.__Rcon(i//4)
                for x in range(4):
                    readyKey.append((expancionKeys[i-4][x] ^ roundKey[x]))
                expancionKeys.append(readyKey)
        return expancionKeys
    def __RotWord(self, key):
        rottenKey = [key[1],key[2],key[3],key[0]]
        return rottenKey
    def __SubWord(self,key,sbox):
        subKey = [sbox[i] for i in key]
        return subKey
    def __Rcon(self,round):
        rcon = [
                0x01, 0x02, 0x04, 0x08, 0x10,
                0x20, 0x40, 0x80, 0x1B, 0x36
                ]
        if 1<=round<=len(rcon):
            return rcon[round-1]
        return 0x00
    def encrypt(self,text, mode):
        if mode == 'EBC':
            text = list(text.encode('utf-8'))
            text = self.__Padding(text)
            text = [text[i:i + 16] for i in range(0, len(text), 16)]
            shifroText = ''
            for i in text:
                    encryptedBlock = self.__encryptBlock(i)
                    shifroText = shifroText + encryptedBlock.hex()
            return shifroText
        elif mode == 'CBC':
            text = list(text.encode('utf-8'))
            text = self.__Padding(text)
            print(text)
            text = [text[i:i + 16] for i in range(0, len(text), 16)]
            shifroText = ''
            IV = b''
            for i in text:
                if text.index(i) == 0:
                    encryptedBlock = self.__encryptBlock(
                        (int.from_bytes(self._IV, 'big') ^ int.from_bytes(i, 'big')).to_bytes(16, 'big'))
                    shifroText = shifroText + encryptedBlock.hex()
                    IV = encryptedBlock
                else:
                    encryptedBlock = self.__encryptBlock(
                        (int.from_bytes(IV, 'big') ^ int.from_bytes(i, 'big')).to_bytes(16, 'big'))
                    shifroText = shifroText + encryptedBlock.hex()
                    IV = encryptedBlock
            shifroText = self._IV.hex() + shifroText
            return shifroText
    def decrypt(self, text, mode):
        if mode == 'EBC':
            text = list(bytes.fromhex(text))
            text = [text[i:i + 16] for i in range(0, len(text), 16)]
            decryptedBytes = b''
            for i in text:
                    decryptedBlock = self.__decryptBlock(i)
                    decryptedBytes = decryptedBytes + decryptedBlock
            decryptedText = decryptedBytes.decode('utf-8')
            decryptedText = self.__unPadding(decryptedText)
            return  decryptedText
        elif mode == 'CBC':
            text = list(bytes.fromhex(text))
            text = [text[i:i + 16] for i in range(0, len(text), 16)]
            decryptedBytes = b''
            IV = text[0]
            text = text[1:]
            for i in text:
                decryptedBlock = (int.from_bytes(self.__decryptBlock(i), 'big') ^ int.from_bytes(IV, 'big')).to_bytes(
                    16, 'big')
                decryptedBytes = decryptedBytes + decryptedBlock
                IV = i
            decryptedText = decryptedBytes.decode('utf-8')
            decryptedText = self.__unPadding(decryptedText)
            return decryptedText
    def __encryptBlock(self, text):
        state = []
        rounds = 0
        if len(text)==16:
            for x in range(4):
                a=[]
                for y in range(4):
                    a.append(text[x+y*4])
                state.append(a)
        state = self.__AddKeyRounds(state,0)
        rounds=rounds+1
        for i in range(9):
            state = self.__AddKeyRounds(self.__MixColumns(self.__ShiftRows(self.__SubBytes(state))),rounds)
            rounds = rounds+1
        CryptoBlock = self.__AddKeyRounds(self.__ShiftRows(self.__SubBytes(state)), rounds)
        ShifroText = []
        for x in range(4):
            for y in range(4):
                ShifroText.append(CryptoBlock[y][x])
        return bytes(ShifroText)
    def __SubBytes(self, block):
        for x in range(4):
            for y in range(4):
                block[x][y] = self._sbox[block[x][y]]
        return block
    def __ShiftRows(self,block):
        block = [[block[0][0],block[0][1],block[0][2],block[0][3]],
                 [block[1][1],block[1][2],block[1][3],block[1][0]],
                 [block[2][2],block[2][3],block[2][0],block[2][1]],
                 [block[3][3],block[3][0],block[3][1],block[3][2]]]
        return block
    def __MixColumns(self, block):
        Matrix = [[2,3,1,1],
                  [1,2,3,1],
                  [1,1,2,3],
                  [3,1,1,2]]
        mix_block = [[0] * 4 for _ in range(4)]
        for x in range(4):
            for y in range(4):
                a = []
                for z in range(4):
                    if Matrix[y][z] == 1:
                        a.append(block[z][x])
                    elif Matrix[y][z] == 2:
                        a.append(self.__mul2(block[z][x]))
                    elif Matrix[y][z] == 3:
                        a.append(self.__mul3(block[z][x]))
                mix_block[y][x] = (a[0]^a[1]^a[2]^a[3])
        return mix_block
    def __mul2(self, x):
        shifted = x << 1
        if x & 0x80:
            shifted ^= 0x1B
        return shifted & 0xFF
    def __AddKeyRounds(self, block,round):
        for x in range(4):
            for y in range(4):
                block[y][x] = block[y][x] ^ self._keys[x+(4*round)][y]
        return block
    def __mul3(self, x):
        return self.__mul2(x) ^ x

    def __decryptBlock(self,stext):
        state = []
        rounds = 10
        if len(stext)==16:
            for x in range(4):
                a=[]
                for y in range(4):
                    a.append(stext[x+y*4])
                state.append(a)
        state = self.__invSubBytes(self.__invShiftRows((self.__AddKeyRounds(state, rounds))))
        rounds = rounds-1
        for i in range(9):
            state = self.__invSubBytes(self.__invShiftRows(self.__invMixColumns(self.__AddKeyRounds(state, rounds))))
            rounds = rounds - 1
        state = self.__AddKeyRounds(state,0)
        DecryptedText = []
        for x in range(4):
            for y in range(4):
                DecryptedText.append(state[y][x])
        return bytes(DecryptedText)
    def __invSubBytes(self,block):
        for x in range(4):
            for y in range(4):
                block[x][y] = self._invsbox[block[x][y]]
        return block
    def __invShiftRows(self,block):
        block = [[block[0][0], block[0][1], block[0][2], block[0][3]],
                 [block[1][3], block[1][0], block[1][1], block[1][2]],
                 [block[2][2], block[2][3], block[2][0], block[2][1]],
                 [block[3][1], block[3][2], block[3][3], block[3][0]]]
        return block
    def __invMixColumns(self, block):
        Matrix = [['E','B','D',9],
                  [9,'E','B','D'],
                  ['D',9,'E','B'],
                  ['B','D',9,'E']]
        mix_block = [[0] * 4 for _ in range(4)]
        for x in range(4):
            for y in range(4):
                a=[]
                for z in range(4):
                    if Matrix[y][z] == 9:
                        a.append(self.__mul9(block[z][x]))
                    elif Matrix[y][z] == 'B':
                        a.append(self.__mulB(block[z][x]))
                    elif Matrix[y][z] == 'E':
                        a.append(self.__mulE(block[z][x]))
                    elif Matrix[y][z] == 'D':
                        a.append(self.__mulD(block[z][x]))
                mix_block[y][x] = a[0] ^ a[1] ^ a[2] ^ a[3]
        return mix_block

    def __mul9(self, x):
        return self.__mul2(self.__mul2(self.__mul2(x))) ^ x

    def __mulB(self, x):
        mul8 = self.__mul2(self.__mul2(self.__mul2(x)))
        mul2 = self.__mul2(x)
        return mul8 ^ mul2 ^ x

    def __mulD(self, x):
        mul8 = self.__mul2(self.__mul2(self.__mul2(x)))
        mul4 = self.__mul2(self.__mul2(x))
        return mul8 ^ mul4 ^ x

    def __mulE(self, x):
        mul8 = self.__mul2(self.__mul2(self.__mul2(x)))
        mul4 = self.__mul2(self.__mul2(x))
        mul2 = self.__mul2(x)
        return mul8 ^ mul4 ^ mul2
    def __Padding(self, text):
        pad = len(text) % 16
        for i in range(16-pad):
            text.append(16-pad)
        return text
    def __unPadding(self,text):
        chr = text[-1]
        while text[-1] == chr:
            text = text[:-1]
        return text