import re


def find_occurences(array, string):
    ocurrences = []

    for item in array:
        indices = []
        start = 0
        count = 0

        while True:
            index = string.find(item, start)
            if index == -1:
                break 
            else:
                string = string[:index] + string[index + len(item):]
                indices.append(index)
                start = index + 1
                count += 1
            
        ocurrences.append(count)

    return ocurrences, string


def clean_text(string):
    return re.sub(r'\s+', ' ', string)


def verify_valid(string):
    is_valid = True
    for char in string:
         if not((char in numbers) or (char in identifiers) or (char in signs) or (char in operators)):
            is_valid = False

    return is_valid


def count_variables(string):
    variables = clean_text(string).split(' ')

    counts = {} 

    for item in variables:
        if item in counts:
            counts[item] += 1
        else:
            counts.update({item: 1})

    return counts


key_words = ['entero', 'decimal', 'booleano', 'cadena', 'sino', 'si', 'mientras', 
             'hacer', 'verdadero', 'falso']
operators = ['+', '-', '*', '/', '%', '==', '<=', '>=', '<', '>',  '=']
signs = ['(', ')', '{', '}', '"', ';']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
identifiers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

text = 'Number1 entero + entero Number2 - si + == <= = + number2 sino (number1 - 8) + 8 - Number1'.lower()

if (verify_valid(text)):
    key_words_ocurrences, new_text = find_occurences(key_words, text)
    operators_ocurrences, new_text = find_occurences(operators, new_text)
    signs_ocurrences, new_text = find_occurences(signs, new_text)
    variables_ocurrences = count_variables(clean_text(new_text))

    print('----------Key words----------')
    for i, key_word in enumerate(key_words):
        if key_words_ocurrences[i] > 0:
            print(f'{key_word} finded {key_words_ocurrences[i]} times')
    
    print('----------Operators----------')
    for i, operator in enumerate(operators):
        if operators_ocurrences[i] > 0:
            print(f'{operator} finded {operators_ocurrences[i]} times')
    print('----------Signs----------')
    for i, sign in enumerate(signs):
        if signs_ocurrences[i] > 0:
            print(f'{sign} finded {signs_ocurrences[i]} times')

    print('----------Variables----------')
    for variable in variables_ocurrences:
        print(f'{variable} finded {variables_ocurrences[variable]} times')

else:
    print('Text is not valid')
