import codecs , random , hashlib , ecdsa , sys , time
from time import sleep
from rich import print
from rich.panel import Panel
from rich.console import Console
from lxml import html
import requests
import threading
import secp256k1 as ice
console = Console()
console.clear()

mylist = []

with open('words.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())

mynumbers = []

with open('numbers.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mynumbers.append(line.strip())


class BrainWallet :

    @staticmethod
    def generate_address_from_passphrase(passphrase) :
        private_key = str(hashlib.sha256(
            passphrase.encode('utf-8')).hexdigest())
        address = BrainWallet.generate_address_from_private_key(private_key)
        return private_key , address

    @staticmethod
    def generate_address_from_private_key(private_key) :
        public_key = BrainWallet.__private_to_public(private_key)
        address = BrainWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key) :
        private_key_bytes = codecs.decode(private_key , 'hex')
        key = ecdsa.SigningKey.from_string(
            private_key_bytes , curve = ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes , 'hex')
        bitcoin_byte = b'04'
        public_key = bitcoin_byte+key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key) :
        public_key_bytes = codecs.decode(public_key , 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest , 'hex')
        network_byte = b'00'
        network_bitcoin_public_key = network_byte+ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key , 'hex')
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest , 'hex')
        checksum = sha256_2_hex[:8]
        address_hex = (network_bitcoin_public_key+checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex) :
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        leading_zeros = len(address_hex)-len(address_hex.lstrip('0'))
        address_int = int(address_hex , 16)
        while address_int > 0 :
            digit = address_int%58
            digit_char = alphabet[digit]
            b58_string = digit_char+b58_string
            address_int //= 58
        ones = leading_zeros//2
        for one in range(ones) :
            b58_string = '1'+b58_string
        return b58_string

INPUTNEEDED = '''[yellow]

  ,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
  |esc| [red]1[/red] | [red]2[/red] | [red]3[/red] | [red]4[/red] | 5 | 6 | 7 | 8 | 9 | 0 | + | ' | <-    |
  |---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
  | ->| | Q | W | E | R | T | Y | U | I | O | P | ] | ^ |     |
  |-----',--',--',--',--',--',--',--',--',--',--',--',--'|    |
  | Caps | A | S | D | F | G | H | J | K | L | \ | [ | * |    |
  |----,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'---'----|
  |    | < | Z | X | C | V | B | N | M | , | . | - |          |
  |----'-,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
  | ctrl |🪟| alt |                          |altgr |  | ctrl |
  '------'  '-----'--------------------------'------'  '------'    

[/yellow]'''

INPUTNEEDEDBRAIN = '''[yellow]

  ,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
  |esc| [red]1[/red] | [red]2[/red] | [red]3[/red] | [red]4[/red] | [red]5[/red] | [red]6[/red] | [red]7[/red] | [red]8[/red] | [red]9[/red] | [red]0[/red] | [red]+[/red] | [red]'[/red] | [red]<-[/red]    |
  |---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
  | [red]->|[/red] | [red]Q[/red] | [red]W[/red] | [red]E[/red] | [red]R[/red] | [red]T[/red] | [red]Y[/red] | [red]U[/red] | [red]I[/red] | [red]O[/red] | [red]P[/red] | [red]][/red] | [red]^[/red] |     |
  |-----',--',--',--',--',--',--',--',--',--',--',--',--'|    |
  | [red]Caps[/red] | [red]A[/red] | [red]S[/red] | [red]D[/red] | [red]F[/red] | [red]G[/red] | [red]H[/red] | [red]J[/red] | [red]K[/red] | [red]L[/red] | \ | [red][[/red] | [red]*[/red] |    |
  |----,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'---'----|
  |    | [red]<[/red] | [red]Z[/red] | [red]X[/red] | [red]C[/red] | [red]V[/red] | [red]B[/red] | [red]N[/red] | [red]M[/red] | [red],[/red] | [red].[/red] | [red]-[/red] |          |
  |----'-,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
  | [red]ctrl[/red] |🪟| [red]alt[/red] |                          |[red]altgr[/red] |  | [red]ctrl[/red] |
  '------'  '-----'--------------------------'------'  '------'    

[/yellow]'''
prompt= ('''[yellow]
    ************** BRAIN Menu Version 3 Online******[/yellow]
    *                                               *
    *    Option 1. Words  From File        =  1     *
    *    Option 2. Numbers From File       =  2     *
    *    Option 3.Random Number range      =  3     * 
    *    Option 4.OWN BRAIN WORDS          =  4     *    
    *                                               *
    [yellow]************** BRAIN Menu Online 3 *************[/yellow]
 ''')
print (INPUTNEEDED)
print (prompt) 
start=int(input('Enter Your Choice 1/2/3/4 = '))


def main_scan() :
    s = 0
    w = 0
    count = 0
    while True:
        count+=4
        if start == 1:
            passphrase = ' '.join(random.sample(mylist, random.randint(1,12)))
            #passphrase = ''.join(random.sample(mylist, random.randint(1,12))) # no space

        if start == 2:
            passphrase = ' '.join(random.sample(mynumbers, random.randint(1,12)))
            #passphrase = ''.join(random.sample(mynumbers, random.randint(1,12))) # no space

        if start == 3:
            choice = random.randrange(2**1,2**256) #edit random range here
            passphrase= str(choice)
        if start == 4:
            print (INPUTNEEDEDBRAIN)
            yourbrain =str(input('Enter Your Brain Words => '))
            passphrase= yourbrain
        wallet = BrainWallet()
        private_key, address = wallet.generate_address_from_passphrase(passphrase)
        dec = int(private_key , 16)
        wifc = ice.btc_pvk_to_wif(private_key)
        wifu = ice.btc_pvk_to_wif(private_key, False)
        caddr = ice.privatekey_to_address(0, True, dec) #Compressed
        p2sh = ice.privatekey_to_address(1, True, dec) #p2sh
        bech32 = ice.privatekey_to_address(2, True, dec)  #bech32
        urlblock = "https://bitcoin.atomicwallet.io/address/"+address
        respone_block = requests.get(urlblock)
        byte_string = respone_block.content
        source_code = html.fromstring(byte_string)
        xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'
        treetxid = source_code.xpath(xpatch_txid)
        xVol = str(treetxid[0].text_content())
        bal = str(xVol)
        
        urlblockcaddr = "https://bitcoin.atomicwallet.io/address/"+caddr
        respone_blockcaddr = requests.get(urlblockcaddr)
        byte_stringcaddr = respone_blockcaddr.content
        source_codecaddr = html.fromstring(byte_stringcaddr)
        xpatch_txidcaddr = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'
        treetxidcaddr = source_codecaddr.xpath(xpatch_txidcaddr)
        xVolcaddr = str(treetxidcaddr[0].text_content())
        balcaddr = str(xVolcaddr)
        
        urlblockp2sh = "https://bitcoin.atomicwallet.io/address/"+p2sh
        respone_blockp2sh = requests.get(urlblockp2sh)
        byte_stringp2sh = respone_blockp2sh.content
        source_codep2sh = html.fromstring(byte_stringp2sh)
        xpatch_txidp2sh = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'
        treetxidp2sh = source_codep2sh.xpath(xpatch_txidp2sh)
        xVolp2sh = str(treetxidp2sh[0].text_content())
        balp2sh = str(xVolp2sh)
        
        urlblockbech32 = "https://bitcoin.atomicwallet.io/address/"+bech32
        respone_blockbech32 = requests.get(urlblockbech32)
        byte_stringbech32 = respone_blockbech32.content
        source_codebech32 = html.fromstring(byte_stringbech32)
        xpatch_txidbech32 = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'
        treetxidbech32 = source_codebech32.xpath(xpatch_txidbech32)
        xVolbech32 = str(treetxidbech32[0].text_content())
        balbech32 = str(xVolbech32)
        
        ammount = '0 BTC'
        if int(bal) > 0 or int(balcaddr) > 0 or int(balp2sh) > 0 or int(balbech32) > 0:
            urlblock1 = "https://bitcoin.atomicwallet.io/address/"+address
            respone_block1 = requests.get(urlblock1)
            byte_string1 = respone_block1.content
            source_code1 = html.fromstring(byte_string1)
            xpatch_txid1 = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
            treetxid1 = source_code1.xpath(xpatch_txid1)
            xVol1 = str(treetxid1[0].text_content())
            val = str(xVol1)
            
            urlblock1caddr = "https://bitcoin.atomicwallet.io/address/"+caddr
            respone_block1caddr = requests.get(urlblock1caddr)
            byte_string1caddr = respone_block1caddr.content
            source_code1caddr = html.fromstring(byte_string1caddr)
            xpatch_txid1caddr = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
            treetxid1caddr = source_code1caddr.xpath(xpatch_txid1caddr)
            xVol1caddr = str(treetxid1caddr[0].text_content())
            valcaddr = str(xVol1caddr)
            
            urlblock1p2sh = "https://bitcoin.atomicwallet.io/address/"+p2sh
            respone_block1p2sh = requests.get(urlblock1p2sh)
            byte_string1p2sh = respone_block1p2sh.content
            source_code1p2sh = html.fromstring(byte_string1p2sh)
            xpatch_txid1p2sh = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
            treetxid1p2sh = source_code1p2sh.xpath(xpatch_txid1p2sh)
            xVol1p2sh = str(treetxid1p2sh[0].text_content())
            valp2sh = str(xVol1p2sh)
            
            urlblock1bech32 = "https://bitcoin.atomicwallet.io/address/"+bech32
            respone_block1bech32 = requests.get(urlblock1bech32)
            byte_string1bech32 = respone_block1bech32.content
            source_code1bech32 = html.fromstring(byte_string1bech32)
            xpatch_txid1bech32 = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
            treetxid1bech32 = source_code1bech32.xpath(xpatch_txid1bech32)
            xVol1bech32 = str(treetxid1bech32[0].text_content())
            valbech32 = str(xVol1bech32)
            
            running_print = str(
                '[gold1 on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                    bal)+'[gold1]  BAL:[aquamarine1]'+str(val)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(address)+'[gold1 on grey15]                  Passphrase: '+'[orange_red1]'+str(passphrase)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
            running_print1 = str(
                '[gold1 on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                    balcaddr)+'[gold1]  BAL:[aquamarine1]'+str(valcaddr)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(caddr)+'[gold1 on grey15]                  Passphrase: '+'[orange_red1]'+str(passphrase)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
            running_print2 = str(
                '[gold1 on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                    balp2sh)+'[gold1]  BAL:[aquamarine1]'+str(valp2sh)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(p2sh)+'[gold1 on grey15]                  Passphrase: '+'[orange_red1]'+str(passphrase)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
            running_print3 = str(
                '[gold1 on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                    balbech32)+'[gold1]  BAL:[aquamarine1]'+str(valbech32)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(bech32)+'[gold1 on grey15]                  Passphrase: '+'[orange_red1]'+str(passphrase)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')

            style = "gold1 on grey11"
            f=open('brainsave.txt','a')
            f.write(f"  Passphrase  >>  \n{passphrase}\n Private Key  >>  \n{private_key} \n\n  WIF Compressed  >>  \n{wifc}\n\n  WIF Uncompressed  >>  \n{wifu}\n\n Bitcoin Address = {caddr}  Balance {valcaddr}  TX = {balcaddr}  BTC \n\n Bitcoin Address = {address}  Balance  {val}  TX = {bal}  BTC \n\n Bitcoin Address = {p2sh}  Balance  {valp2sh}  TX = {balp2sh}  BTC \n\n Bitcoin Address = {bech32} Balance  {valbech32}  TX = {balbech32}  BTC")
            f.close()
            console.print(Panel(str(running_print) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "red") , style = style , justify = "full")
            console.print(Panel(str(running_print1) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "red") , style = style , justify = "full")
            console.print(Panel(str(running_print2) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "red") , style = style , justify = "full")
            console.print(Panel(str(running_print3) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "red") , style = style , justify = "full")

            w += 1
            if str(val) != str(ammount) or str(valcaddr) != str(ammount) or str(valp2sh) != str(ammount) or str(valbech32) != str(ammount):
                s += 1
                running_print_Balance = str(
                    '[green on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                        bal)+'[gold1]  BAL:[aquamarine1]'+str(val)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(address)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
                running_print_Balance1 = str(
                    '[green on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                        balcaddr)+'[gold1]  BAL:[aquamarine1]'+str(valcaddr)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(u)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
                running_print_Balance2 = str(
                    '[green on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                        balp2sh)+'[gold1]  BAL:[aquamarine1]'+str(valp2sh)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(p2sh)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
                running_print_Balance3 = str(
                    '[green on grey15]Total Checked: '+'[orange_red1]'+str(count)+'[/][gold1 on grey15] '+' Found:'+'[white]'+str(w)+'[/]'+'[/][gold1]                  TX: '+'[/][aquamarine1]'+str(
                        balbech32)+'[gold1]  BAL:[aquamarine1]'+str(valbech32)+'\n[/][gold1 on grey15]Addr: '+'[white] '+str(bech32)+'[/]\nPRIVATEKEY: [grey54]'+str(private_key)+'[/]')
                
                console.print(Panel(str(running_print_Balance) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "green") , style = style , justify = "full")
                console.print(Panel(str(running_print_Balance1) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "green") , style = style , justify = "full")
                console.print(Panel(str(running_print_Balance2) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "green") , style = style , justify = "full")
                console.print(Panel(str(running_print_Balance3) , title = "[white]Found Wallet [/]" , subtitle = "[green_yellow blink] Good Luck Happy Hunting [/]" , style = "green") , style = style , justify = "full")

                f=open('Foundner.txt','a')
                f.write(f"  Passphrase  >>  \n{passphrase}\n Private Key  >>  \n{private_key} \n\n  WIF Compressed  >>  \n{wifc}\n\n  WIF Uncompressed  >>  \n{wifu}\n\n Bitcoin Address = {caddr}  Balance {valcaddr}  TX = {balcaddr}  BTC \n\n Bitcoin Address = {address}  Balance  {val}  TX = {bal}  BTC \n\n Bitcoin Address = {p2sh}  Balance  {valp2sh}  TX = {balp2sh}  BTC \n\n Bitcoin Address = {bech32} Balance  {valbech32}  TX = {balbech32}  BTC")
                f.close()
        else :
            console.print('[gold1 on grey7]Scan:[light_goldenred1]'+str(count)+'[gold1] Tx:[white]'+str(w)+'[green] Rich:[white]'+str(s)+'[/][yellow] Add:[green1]'+str(address)+'[red1]  TXID:[white]'+str(
                bal)+'[gold1]  Passphrase:[white]'+str(passphrase))
            console.print('[gold1 on grey7]Scan:[light_goldenred1]'+str(count)+'[gold1] Tx:[white]'+str(w)+'[green] Rich:[white]'+str(s)+'[/][yellow] Add:[green1]'+str(caddr)+'[red1]  TXID:[white]'+str(
                balcaddr)+'[gold1]  Passphrase:[white]'+str(passphrase))
            console.print('[gold1 on grey7]Scan:[light_goldenred1]'+str(count)+'[gold1] Tx:[white]'+str(w)+'[green] Rich:[white]'+str(s)+'[/][yellow] Add:[green1]'+str(p2sh)+'[red1]  TXID:[white]'+str(
                balp2sh)+'[gold1]  Passphrase:[white]'+str(passphrase))
            console.print('[gold1 on grey7]Scan:[light_goldenred1]'+str(count)+'[gold1] Tx:[white]'+str(w)+'[green] Rich:[white]'+str(s)+'[/][yellow] Add:[green1]'+str(bech32)+'[red1]  TXID:[white]'+str(
                balbech32)+'[gold1]  Passphrase:[white]'+str(passphrase))

thr = threading.Thread(target = main_scan , args = ())
thr.start()
thr.join()