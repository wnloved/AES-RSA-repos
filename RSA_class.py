import random
class RSA:
    @staticmethod
    def generateSimple():
        q = random.randint(2, 1024)
        if RSA.getSimple(q) == False:
            return RSA.generateSimple()
        return q
    @staticmethod
    def getSimple(integer):
        for i in range(2, integer):
            if integer%i == 0:
                return False
        return True
    def __init__(self, publicKey = None):
        self._keys = self.__getKeys()
        if publicKey !=None:
            self.publicKey = publicKey
        else:
            self.publicKey = self._keys[0]
        self._privateKey = self._keys[1]
    @staticmethod
    def __getInverse(integer, mod):
        for i in range(mod):
            if (integer*i)%mod == 1:
                return i
    def __getEulerFunc(self,q,d):
        return (q-1)*(d-1)

    def __getKeys(self):
        p = RSA.generateSimple()
        q = RSA.generateSimple()
        n = q * p
        e = 65537
        d = self.__getInverse(e, self.__getEulerFunc(q,p))
        public_key = [n,e]
        private_key = [n,d]
        return [public_key,private_key]

    def encode(self, text):
        text = list(text.encode('utf-8'))
        shipher = b''
        for i in range(len(text)):
            text[i] = pow(text[i],self.publicKey[1],self.publicKey[0])
        for i in text:
            shipher+=i.to_bytes(3,'big')
        shipher = shipher.hex()
        return shipher
    def decode(self, byte):
        byte = bytes.fromhex(byte)
        text = []
        for i in range(0, len(byte), 3):
            text.append(int.from_bytes(byte[i:i+3], 'big'))
        for i in range(len(text)):
            text[i] = pow(text[i], self._privateKey[1], self._privateKey[0])
        text = bytes(text)
        text = text.decode('utf-8')
        return text
