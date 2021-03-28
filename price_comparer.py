#!/bin/python3

import random
import requests
import sys
import cmd
import json
from color import *
from file_op import *

#Function that returns key corresponding to the minimum value
def min_from_dict(diction):
    key_list = list(diction.keys())
    value_list = list(diction.values())
    min_value = min(value_list)
    key_index = value_list.index(min_value)
    min_key = key_list[key_index]
    return min_key

def set_title():
    item_name_title = input("[Optional] Enter the name of the product you wish to compare price: ")
    return item_name_title

#API from https://exchangeratesapi.io/
api_http = 'https://api.exchangeratesapi.io/latest'
exchange_rate_data = requests.get(api_http).json()
exchange_rate_data['rates']['EUR'] = 1.0

#Prints banner
banner1 = '\n__________        .__               _________                                                  \n\\______   \\_______|__| ____  ____   \\_   ___ \\  ____   _____ ___________ _______   ___________ \n |     ___/\\_  __ \\  |/ ___\\/ __ \\  /    \\  \\/ /  _ \\ /     \\\\____ \\__  \\\\_  __ \\_/ __ \\_  __ \\\n |    |     |  | \\/  \\  \\__\\  ___/  \\     \\___(  <_> )  Y Y  \\  |_> > __ \\|  | \\/\\  ___/|  | \\/\n |____|     |__|  |__|\\___  >___  >  \\______  /\\____/|__|_|  /   __(____  /__|    \\___  >__|   \n                          \\/    \\/          \\/             \\/|__|       \\/            \\/       \n'
banner2 = ' ######                             #####                                                   \n #     # #####  #  ####  ######    #     #  ####  #    # #####    ##   #####  ###### #####  \n #     # #    # # #    # #         #       #    # ##  ## #    #  #  #  #    # #      #    # \n ######  #    # # #      #####     #       #    # # ## # #    # #    # #    # #####  #    # \n #       #####  # #      #         #       #    # #    # #####  ###### #####  #      #####  \n #       #   #  # #    # #         #     # #    # #    # #      #    # #   #  #      #   #  \n #       #    # #  ####  ######     #####   ####  #    # #      #    # #    # ###### #    # \n                                                                                            '
banner3 = '   _ \\        _)                 ___|                                                  \n  |   |   __|  |   __|   _ \\    |       _ \\   __ `__ \\   __ \\    _` |   __|  _ \\   __| \n  ___/   |     |  (      __/    |      (   |  |   |   |  |   |  (   |  |     __/  |    \n _|     _|    _| \\___| \\___|   \\____| \\___/  _|  _|  _|  .__/  \\__,_| _|   \\___| _|    \n                                                        _|                             '
banner4 = ' ____  ____  _  ____  _____   ____  ____  _      ____  ____  ____  _____ ____ \n/  __\\/  __\\/ \\/   _\\/  __/  /   _\\/  _ \\/ \\__/|/  __\\/  _ \\/  __\\/  __//  __\\\n|  \\/||  \\/|| ||  /  |  \\    |  /  | / \\|| |\\/|||  \\/|| / \\||  \\/||  \\  |  \\/|\n|  __/|    /| ||  \\_ |  /_   |  \\__| \\_/|| |  |||  __/| |-|||    /|  /_ |    /\n\\_/   \\_/\\_\\\\_/\\____/\\____\\  \\____/\\____/\\_/  \\|\\_/   \\_/ \\|\\_/\\_\\\\____\\\\_/\\_\\\n                                                                              '

#Banner list
banner = [banner1,banner2,banner3,banner4]
version = '1.0.0'



#Opens the currency dictionary
with open('currency_dict.json') as file_obj:
    currency_dict = json.load(file_obj)

#MainShell
class MainShell(cmd.Cmd):
    prompt = 'Price Comparer: '

    load_path = ''
    price_data = {}
    item_name = set_title()
    #Adds an entry
    def do_add(self,arg):
        'Adds data.\nNote that this can also be used to modify data.'
        try:
            print("Currency code list: ")
            print("-" * 10)
            for key,entry in currency_dict.items():
                print(key + ": " + entry)
            print("-" * 10)
            currency = input('Input the currency ' + color_text(color_text("code",'UNDERLINE'),"BOLD") + ': ')
            currency = currency[:3]
            #Check if currency code is appropriate
            if currency.upper() not in exchange_rate_data['rates']:
                print("Wrong currency code!\n")
                return 0
            cost_val = input('Enter cost (without currency symbol): ')
            self.price_data[currency.upper()] = float(cost_val)
        except:
            print("An error occurred! Cancelling operation.\n")
            return 0
        print('-' * 10)

    #Removes information entered
    def do_remove(self,arg):
        'Removes data.'
        print("Currency code list: ")
        print("-" * 10)
        for key,entry in currency_dict.items():
            print(key + ": " + entry)
        print("-" * 10)
        self.do_view('')
        currency = input('Input the currency ' + color_text(color_text("code",'UNDERLINE'),"BOLD") + ' of the data you wish to remove: ')
        currency = currency.upper()
        if currency in self.price_data:
            del self.price_data[currency]
        else:
            print('No such data is given!')


    #View all the information entered
    def do_view(self,arg):
        'View information entered.'
        print("-" * 10)
        if self.item_name:
            print(color_text("Item: " + self.item_name,'YELLOW'))
        for entry in self.price_data:
            print(color_text(entry + ": " + str(self.price_data[entry]),'YELLOW'))
        print("-" * 10)

    #Convert the information entered into a given currency.
    def do_convert(self,arg):
        'View the information entered with each price converted into one currency.'
        print("-" * 10)
        currency = input("Enter the " + color_text(color_text("code",'UNDERLINE'),"BOLD") + " for the currency you wish to view data in: ")
        currency = currency.upper()
        #Check if valid currency
        if currency in currency_dict:
            #For each currency, calculate the converted price.
            #Dictionary of all converted price
            converted_price_dict = {}
            for original_currency in self.price_data:
                #Converting price using exchange rate
                converted_price = self.price_data[original_currency] / exchange_rate_data['rates'][original_currency] * exchange_rate_data['rates'][currency]
                #Adding to the dictionary of converted prices
                converted_price_dict[original_currency] = converted_price
                print(color_text(original_currency + ': ' + str(self.price_data[original_currency]),'YELLOW') + '\t\t==>\t\t' + color_text(currency + ": " + str(converted_price),'CYAN'))
            if converted_price_dict:
                best_currency = min_from_dict(converted_price_dict)
                print(color_text("Best Currency: " + best_currency,"GREEN"))
            print("-" * 10)
                
        else:
            print("Check your currency again!")
            print("-" * 10)

    #View the exchange rate data
    def do_xrate(self,arg):
        'View the raw exchange rate data.'
        print('-' * 10)
        print("Loaded data:")
        print(color_text(str(exchange_rate_data),'GREEN'))
        print('-' * 10)

    #Saves session
    def do_save(self,arg):
        'Saves the current session as a .json file.'
        print("-" * 10)
        save_bool = input("Would you like to save? [y/N]: ")
        if save_bool.lower() == 'y':
            if not self.load_path:
                save_path = input("Enter the save path (with .json): ")
            else:
                save_path = self.load_path
            try:
                jsonsave([self.item_name,self.price_data],save_path)
                print("Saved!")
                print([self.item_name,self.price_data])
            except:
                print("Error when saving!")
        print("-" * 10)

    #Loads saved session
    def do_load(self,arg):
        'Loads session from .json file.'
        print("-" * 10)
        self.load_path = input("Enter the load path (with .json): ")
        try:
            loaded_data = jsonload(self.load_path)
            self.item_name = loaded_data[0]
            self.price_data = loaded_data[1]
        except:
            print("Error when loading!")

    #Updates the exchange rate data
    def do_update(self,arg):
        'Updates the raw exchange rate data.'
        print('-' * 10)
        download_bool = input('Would you like to update the exchange rate data? [y/N] ')
        if download_bool.lower() == 'y':
            try:
                exchange_rate_data = requests.get(api_http).json()
                exchange_rate_data['rates']['EUR'] = 1.0
                print("Updated!")
                print('-' * 10)
                print("Loaded data:")
                print(color_text(str(exchange_rate_data),'GREEN'))
                print('-' * 10)
            except:
                print("An error occurred.")
                print('-' * 10)
                return 0
        else:
            return 0
    def do_exit(self,arg):
        'Quits the shell.'
        print("Good bye!")
        sys.exit()
    def do_quit(self,arg):
        'Quits the shell'
        self.do_exit('')






if __name__ == '__main__':
#Print banner
    print(banner[random.randrange(len(banner))])
    print("-" * 10)
    print("Version: " + str(version))
    print("-" * 10)
    print("Loaded Data:")
    print(color_text(str(exchange_rate_data),'GREEN'))
    print("-" * 10)
    MainShell().cmdloop()