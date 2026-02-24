# 🔐 AES-RSA Cryptographic Implementations

> 🎓 Учебный проект по реализации криптографических алгоритмов AES и RSA с нуля

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Educational](https://img.shields.io/badge/purpose-educational-orange.svg)]()

## ⚠️ Важное предупреждение

**Данная реализация предназначена ТОЛЬКО для образовательных целей!**  
Не используйте этот код в production-среде. Для реальных задач применяйте проверенные библиотеки (`cryptography`, `pycryptodome`, `OpenSSL`).

---

## 📋 Содержание

- [AES (Advanced Encryption Standard)](#-aes-advanced-encryption-standard)
  - [Быстрый старт AES](#быстрый-старт-aes)
  - [Режимы работы](#режимы-работы)
  - [Padding](#padding)
- [RSA (Rivest–Shamir–Adleman)](#-rsa-rivestshamiradleman)
  - [Быстрый старт RSA](#быстрый-старт-rsa)
  - [Статические методы](#статические-методы)
- [Примеры использования](#-примеры-использования)
- [Установка](#-установка)
- [Лицензия](#-лицензия)

---

## 🔷 AES (Advanced Encryption Standard)

Полная реализация AES-128 с нуля, включая все раунды, KeyExpansion, SubBytes, ShiftRows, MixColumns и AddRoundKey.

### ✨ Особенности:
- ✅ Поддержка режимов **ECB** и **CBC**
- ✅ **PKCS#7 padding** для произвольной длины сообщений
- ✅ Генерация случайного S-блока с обратным преобразованием
- ✅ Работа с UTF-8 текстом

### Быстрый старт AES

```python
from AES_class import AES

# Инициализация с кастомным S-блоком
key = b'helloworldabcdef'
aes = AES(
    key,
    AES.createSblock(42),        # прямой S-блок
    AES.invSblock(AES.createSblock(42))  # обратный S-блок
)

# Шифрование
ciphertext = aes.encrypt("Секретное сообщение", mode='CBC')

# Расшифровка
plaintext = aes.decrypt(ciphertext, mode='CBC')
print(plaintext)  # "Секретное сообщение"
Режимы работы
ECB (Electronic Codebook)
python
cipher_ecb = aes.encrypt("Hello World!", mode='ECB')
plain_ecb = aes.decrypt(cipher_ecb, mode='ECB')
CBC (Cipher Block Chaining)
python
cipher_cbc = aes.encrypt("Hello World!", mode='CBC')
plain_cbc = aes.decrypt(cipher_cbc, mode='CBC')
Padding
Реализован стандарт PKCS#7:

Добавляется от 1 до 16 байт

Значение каждого байта равно длине padding'а

Всегда добавляется даже при полном блоке

```
🔶 RSA (Rivest–Shamir–Adleman)
Реализация асимметричного шифрования для безопасной передачи ключей AES.

✨ Особенности:
✅ Генерация простых чисел

✅ Вычисление публичного и приватного ключей

✅ Поддержка шифрования/расшифровки

✅ Возможность использования чужих публичных ключей

### Быстрый старт RSA
```
python
from RSA_class import RSA

# Создание пары ключей
rsa_receiver = RSA()
public_key = rsa_receiver.publicKey

# Отправитель использует публичный ключ получателя
rsa_sender = RSA(publicKey=public_key)
aes_key = b'my_aes_key_12345'
encrypted_key = rsa_sender.encode(aes_key)

# Получатель расшифровывает своим приватным ключом
decrypted_key = rsa_receiver.decode(encrypted_key)
print(decrypted_key)  # b'my_aes_key_12345'
Статические методы
python
# Генерация простого числа в диапазоне (2, 1024)
prime = RSA.generateSimple()

# Проверка числа на простоту
is_prime = RSA.getSimple(17)  # True
🎯 Примеры использования
Гибридная схема (RSA + AES)
python
# Получатель создает ключи
receiver_rsa = RSA()
public_key = receiver_rsa.publicKey

# Отправитель шифрует AES-ключ
sender_rsa = RSA(publicKey=public_key)
aes_key = b'my_secret_aes_key'
encrypted_aes_key = sender_rsa.encode(aes_key)

# Шифрование данных AES
aes = AES(aes_key, AES.createSblock(42), AES.invSblock(AES.createSblock(42)))
ciphertext = aes.encrypt("Привет, получатель!", mode='CBC')

# Передача: encrypted_aes_key + ciphertext
# ...

# Получатель расшифровывает
restored_key = receiver_rsa.decode(encrypted_aes_key)
aes_receiver = AES(restored_key, AES.createSblock(42), AES.invSblock(AES.createSblock(42)))
plaintext = aes_receiver.decrypt(ciphertext, mode='CBC')
```
📦 Установка
Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/AES-RSA-repos.git
cd AES-RSA-repos
```
Убедитесь, что используете Python 3.8 или выше:

```bash
python --version
```
Запустите примеры:

```bash
python crypto_test.py
```
📄 Лицензия
Этот проект распространяется под лицензией MIT.
Используйте в образовательных целях, но не применяйте в продакшене.

👨‍💻 Автор
Разработано в образовательных целях для глубокого понимания криптографии.

⭐ Если проект был полезен, поставьте звезду на GitHub!
