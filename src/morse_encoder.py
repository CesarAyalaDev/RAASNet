def morse():
    MORSE_CODE_DICT = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        # Exclamation mark for lowercase because python is case sensative.
        "a": "!.-",
        "b": "!-...",
        "c": "!-.-.",
        "d": "!-..",
        "e": "!.",
        "f": "!..-.",
        "g": "!--.",
        "h": "!....",
        "i": "!..",
        "j": "!.---",
        "k": "!-.-",
        "l": "!.-..",
        "m": "!--",
        "n": "!-.",
        "o": "!---",
        "p": "!.--.",
        "q": "!--.-",
        "r": "!.-.",
        "s": "!...",
        "t": "!-",
        "u": "!..-",
        "v": "!...-",
        "w": "!.--",
        "x": "!-..-",
        "y": "!-.--",
        "z": "!--..",
        # Numbers and Symbols
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        "&": ".-...",
        "@": ".--.-.",
        ":": "---...",
        ",": "--..--",
        ".": ".-.-.-",
        "'": ".----.",
        '"': ".-..-.",
        "?": "..--..",
        "/": "-..-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "(": "-.--.",
        ")": "-.--.-",
        # Exclamation mark is not in ITU-R recommendation
        "!": "-.-.--",
    }


    def encode(message: str) -> str:
        cipher = ""
        for letter in message:
            if letter != " ":
                cipher += MORSE_CODE_DICT[letter] + " "
            else:
                cipher += "/ "

        # Remove trailing space added on line 64
        return cipher[:-1]


    def decode(message: str) -> str:
        decipher = ""
        letters = message.split(" ")
        for letter in letters:
            if letter != "/":
                decipher += list(MORSE_CODE_DICT.keys())[
                    list(MORSE_CODE_DICT.values()).index(letter)
                ]
            else:
                decipher += " "

        return decipher

    payload = open('./payload.py', 'r').readlines()
    code = []
    imports = ''

    for line in payload:
        if not line.startswith('import '):
            line = line.replace('{', 'OOOO').replace('}', 'PPPP').replace('$', 'LLLL').replace('*', '0000').replace('\\', '1111').replace('%', 'AAAA').replace(';', 'BBBB').replace('[', 'CCCC').replace(']', 'DDDD').replace(' ', '5555').replace('\n', '6666').replace('_', '7777').replace('#', '8888').strip()
            if not line.startswith('from '):
                result = encode(line)
                code.append(result)
            elif line.startswith('from '):
                imports += line
        elif line.startswith('import '):
            imports += line

    new_payload = '''%s

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",

    "a": "!.-",
    "b": "!-...",
    "c": "!-.-.",
    "d": "!-..",
    "e": "!.",
    "f": "!..-.",
    "g": "!--.",
    "h": "!....",
    "i": "!..",
    "j": "!.---",
    "k": "!-.-",
    "l": "!.-..",
    "m": "!--",
    "n": "!-.",
    "o": "!---",
    "p": "!.--.",
    "q": "!--.-",
    "r": "!.-.",
    "s": "!...",
    "t": "!-",
    "u": "!..-",
    "v": "!...-",
    "w": "!.--",
    "x": "!-..-",
    "y": "!-.--",
    "z": "!--..",

    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    "&": ".-...",
    "@": ".--.-.",
    ":": "---...",
    ",": "--..--",
    ".": ".-.-.-",
    "'": ".----.",
    '"': ".-..-.",
    "?": "..--..",
    "/": "-..-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",

    "!": "-.-.--",
}

def decode(message: str) -> str:
    decipher = ""
    letters = message.split(" ")
    for letter in letters:
        if letter != "/":
            decipher += list(MORSE_CODE_DICT.keys())[
                list(MORSE_CODE_DICT.values()).index(letter)
            ]
        else:
            decipher += " "
    return decipher

ex = %s
roses = ''
for i in ex:
    if not i == '':
        result = decode(i)
        roses +=result
    else:
        roses +=' '
exec(roses.replace('OOOO', '{').replace('PPPP', '}').replace('LLLL', '$').replace('0000', '*').replace('1111', '\\\\').replace('7777', '_').replace('8888', '#').replace('AAAA', '%%').replace('BBBB', ';').replace('CCCC', '[').replace('DDDD', ']').replace('5555', ' ').replace('6666', '\\n'))
''' % (imports, code)


    with open('./morse_payload.py', 'w') as f:
        f.write(new_payload)
        f.close()
