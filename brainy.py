import codecs , random, hashlib, ecdsa, sys

mylist = []

with open('words.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())

mynumbers = []

with open('numbers.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mynumbers.append(line.strip())
        
with open("puzzle.txt","r") as m:
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
        key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        address_int = int(address_hex, 16)
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string


prompt= '''
    ****************** BRAIN Menu  ******************
    *                                               *
    *    Option 1. Words  From File        =  1     *
    *    Option 2. Numbers From File       =  2     *
    *    Option 3.Random Number range      =  3     *   
    *                                               *
    ****************** BRAIN Menu  ******************'''
    
count=0

start=int(input(prompt))

while True:
    count+=1
    if start == 1:
        passphrase = ' '.join(random.sample(mylist, random.randint(1,12)))
        #passphrase = ''.join(random.sample(mylist, random.randint(1,12))) # no space

    if start == 2:
        passphrase = ' '.join(random.sample(mynumbers, random.randint(1,12)))
        #passphrase = ''.join(random.sample(mynumbers, random.randint(1,12))) # no space

    if start == 3:
        choice = random.randrange(2**1,2**256) #edit random range here
        passphrase= str(choice)
    wallet = BrainWallet()
    private_key, address = wallet.generate_address_from_passphrase(passphrase)
    print('Passphrase       : ',passphrase)
    print('Private Key      : ',private_key)
    print('Bitcoin Address  : ',address)
    print('Scan Number : ', count)
    if address in add:
        print ('\nCongraz you have found Bitcoin Passphrase ')
        print('Bitcoin Address  : ',address)
        print('Passphrase       : ',passphrase)
        print('Private Key      : ',private_key)
        f=open(u"winner.txt","a")
        f.write('\nBitcoin Address Compressed : ' + address)
        f.write('\nPassphrase       : '+ passphrase)
        f.write('\nPrivate Key      : '+ private_key)
        f.close()