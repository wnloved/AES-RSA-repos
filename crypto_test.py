from AES_class import AES
from RSA_class import RSA


key = 'helloworldabcdef'
aes = AES(key,AES.createSblock(42),AES.invSblock(AES.createSblock(42)))
text = input('Что нужно зашифровать\n')
shipher = aes.encrypt(text, 'EBC')
rsa2 =RSA()
rsa_pub = rsa2.publicKey
rsa = RSA(publicKey=rsa_pub)
key_encrypted = rsa.encode(key)

print(shipher)

aes2 = AES(rsa2.decode(key_encrypted), AES.createSblock(42), AES.invSblock(AES.createSblock(42)))
decrypt = aes2.decrypt(shipher, 'EBC')
print(decrypt)
try:
    rsa.decode(key_encrypted)
    print("❌ Ошибка: отправитель смог расшифровать!")
except:
    print("✅ Правильно: отправитель не может расшифровать")

decrypted_key = rsa2.decode(key_encrypted)
print(f"✅ Получатель расшифровал ключ: {decrypted_key}")