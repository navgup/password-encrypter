

import random
import string
import json

# Global Variables
cipher_str = string.printable

security_questions = ['In what city were you born?', 'What is the name of your favorite pet?',
                      "What is your mother's maiden name?", 'What high school did you attend?',
                      'What was the name of your elementary school?', 'What was the make of your first car?',
                      'What was your favorite food as a child?', 'Where did you meet your spouse?']

passwords = {}


# Functions
def char_to_int(ch, cipher_str):
    '''
    Converts a given character to an integer.
    '''
    int = cipher_str.find(ch)
    return int


def int_to_char(int, cipher_str):
    '''
    Converts a given integer to a character.
    '''
    ch = cipher_str[int]
    return ch


def tabula_recta(text, key, cipher_str, encipher=True):
    '''
    Does the mathematical encryption of a single character. A traditional 'tabula recta' is a 26 x 26 grid of the
    alphabet, with each row being shifted one letter to the left. This function uses string.printable instead, making
    it a 96 x 96 grid that can encrypt all characters on the keyboard. encipher parameter used to switch between
    encryption and decryption.
    '''
    if encipher:
        numerical_plaintext = char_to_int(text, cipher_str)
        numerical_key = char_to_int(key, cipher_str)
        numerical_ciphertext = (numerical_plaintext + numerical_key) % len(cipher_str)
        ciphertext = int_to_char(numerical_ciphertext, cipher_str)
        return ciphertext

    else:
        numerical_ciphertext = char_to_int(text, cipher_str)
        numerical_key = char_to_int(key, cipher_str)
        numerical_plaintext = (numerical_ciphertext - numerical_key) % len(cipher_str)
        plaintext = int_to_char(numerical_plaintext, cipher_str)
        return plaintext


def key_length(answer_inp, password_inp):
    '''
    Makes the answer to the security question (the key) equal to the length of the given password so that the password
    can be encrypted.
    '''
    new_answer = ''
    while len(new_answer) < len(password_inp):
        for ch in answer_inp:
            new_answer += ch
    new_answer = new_answer[0:len(password_inp)]
    return new_answer


def encrypt(password_inp, new_answer):
    '''
    Runs the tabula_recta function in encryption mode for each character in the password string to encrypt the password.
    '''
    encrypted_password = ''
    for i in range(len(password_inp)):
        encrypted_password += tabula_recta(password_inp[i], new_answer[i], cipher_str, encipher=True)
    return encrypted_password


def decrypt(encrypted_password, key):
    '''
    Runs the tabula_recta function in decryption mode for each character in the password string to decrypt the password.
    '''
    decrypted_password = ''
    for i in range(len(encrypted_password)):
        decrypted_password += tabula_recta(encrypted_password[i], key[i], cipher_str, encipher=False)
    return decrypted_password


print("Welcome to the Password Manager!\n")


def password_manager():
    with open('password_list.json', 'r') as read_file:
        passwords = json.load(read_file)
    inp = input("Type 1 to access your passwords\nType 2 to edit your password list\nType 3 to quit the program\n")
    if inp == '1':
        with open('password_list.json', 'r') as read_file:
            json.load(read_file)
        if len(passwords) == 0:
            print('''\nYou currently have no passwords stored. Here are your options again:\n''')
            password_manager()
        print('Here are the websites you have a password stored for:\n')
        for key in passwords:
            print(key)
        website = input('\nWhat website would you like the password for?\n')
        if website not in passwords:
            print('That website was not found in the list. Please try again.\n')
            password_manager()
        accessed_pass = passwords[website]
        print(f"Please answer the following security question: {passwords[website][1]}")
        answer = input()
        key = key_length(answer, accessed_pass[0])
        decrypted_password = decrypt(accessed_pass[0], key)
        print(f"Your password for {website} is '{decrypted_password}'!\n")
        password_manager()
    if inp == '2':
        inp = input('Type 1 to add a new password to the list or edit a current one\n'
                    'Type 2 to delete a website from the list\nType 3 to return to the menu\n')
        if inp == '1':
            website_inp = input('What website or application is this password is for?\n')
            passwords[website_inp] = []
            password_inp = input('What is your password?\n')
            x = random.randint(0, len(security_questions) - 1)
            answer_inp = input(f"Type in an answer for the following security question: {security_questions[x]}\n")
            if len(answer_inp) > len(password_inp):
                print('Your password must be longer than your answer to the security question. Please try again.')
                password_manager()
            new_answer = key_length(answer_inp, password_inp)
            encrypted_password = encrypt(password_inp, new_answer)
            passwords[website_inp] = [encrypted_password, security_questions[x]]
            with open('password_list.json', 'w') as write_file:
                json.dump(passwords, write_file)
            print('Password stored!\n')
            password_manager()
        if inp == '2':
            with open('password_list.json', 'r') as read_file:
                json.load(read_file)
            if len(passwords) == 0:
                print('You do not have any passwords to delete.\n')
                password_manager()
            print('Here are the websites you have a password stored for:\n')
            for key in passwords:
                print(key)
            inp = input('\nWhat website do you want to delete?\n')
            if inp in passwords:
                with open('password_list.json', 'w') as write_file:
                    json.dump(passwords, write_file)
                    del passwords[inp]
                print(f'\nPassword for {inp} deleted!')
                with open('password_list.json', 'w') as write_file:
                    json.dump(passwords, write_file)
            else:
                print('This website could not be found. Please try again.\n')
            password_manager()
        if inp == '3':
            password_manager()
        else:
            print('Invalid input, please try again.')
            password_manager()
    if inp == '3':
        print("Thank you for using the password manager!")
        exit()
    else:
        print('Invalid input, please try again.')
        password_manager()


password_manager()
