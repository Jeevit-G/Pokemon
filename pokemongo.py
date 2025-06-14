# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate


# This is the filename of the database to be used
DB_NAME = 'pokemongo.db'


def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close()


TABLES = (" pokemongo "
            "LEFT JOIN type1 on pokemongo.type1_id = type1.type1_id "
            "LEFT JOIN type2 on pokemongo.type2_id = type2.type2_id "
            "LEFT JOIN rarity on pokemongo.rarity_id = rarity.rarity_id "
            "LEFT JOIN intro on pokemongo.intro_id = intro.intro_id ")


def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  


pokemon_list = []

menu_choice = ''
while menu_choice != 'Z':
    menu_choice = input('Welcome to the Pokemon GO Master Class Ranking Database\n\n'
                    'Type the letter for the information you want:\n'
                    'A: All Pokemon Data\n'
                    'B: Base Form Pokemon With Under 4000 Combat Power\n'
                    'C: Combat Power Above 5000\n'
                    'D: Attack Descending\n'
                    'E: Combat Power Descending\n'
                    'F: Defense Descending\n'
                    'G: Introduced In Generation 4 and Second Typing is Dragon\n'
                    'H: Rarity Is Legendary And Is Not Base Form\n'
                    'I: Strongest Water Type\n'
                    'J: Weakest Stats Pokemon\n'
                    'K: Search Pokemon\n'
                    'L: Search Generation\n'
                    'O: Add Information\n'
                    'Z: Exit\n\nType option here: ')


    menu_choice = menu_choice.upper()
    if menu_choice == 'A':
        print_query('All Data')
    elif menu_choice == 'B':
        print_query('Base Form  with under 4000 CP')
    elif menu_choice == 'C':
        print_query('CP over 5000')
    elif menu_choice == 'D':
        print_query('HTL Attack')
    elif menu_choice == 'E':
        print_query('Highest to Lowest Combat Power')
    elif menu_choice == 'F':
        print_query('Highest to Lowest Defense')
    elif menu_choice == 'G':
        print_query('Introduced in Generation iv and are Dragon type')
    elif menu_choice == 'H':
        print_query('Rarity is Legendary and is not Base form')
    elif menu_choice == 'I':
        print_query ('Strongest Water Type')
    elif menu_choice == 'J':
        print_query ('Weakest Stats Pokemon')
    elif menu_choice == 'K':
        pokemon = input('Enter Pokemon name: ')
        pokemon = pokemon.capitalize()
        print_parameter_query("dex, pokemon, form, type1, type2", "pokemon = ?",pokemon)
    elif menu_choice == 'L':
        intro = input('Enter A Generation In Roman Numericals: ')
        print_parameter_query("dex, pokemon, form, type1, type2", "intro = ?",intro)
    elif menu_choice == 'O':
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()
        dex = input("Pokemon Dex Number: ")
        pokemon_list.append(dex)
        pokemon = input("Pokemon Name: ")
        pokemon_list.append(pokemon)
        form = input("Pokemon Form: ")
        pokemon_list.append(form)
        type1_id = input("Pokemon's Primary Typing: ")
        pokemon_list.append(type1_id)
        type2_id = input("Pokemon's Secondary Typing: ")
        pokemon_list.append(type2_id)
        intro_id = input("Generation Introduced In Roman Numericals: ")
        pokemon_list.append(intro_id)
        rarity_id = input("Pokemon's Rarity: ")
        pokemon_list.append(rarity_id)
        cp_used = input("CP Used: ")
        pokemon_list.append(cp_used)
        attack_used = input("Attack Used: ")
        pokemon_list.append(attack_used)
        defense_used = input("Defense Used: ")
        pokemon_list.append(defense_used)
        a = '''INSERT INTO pokemongo(dex, pokemon, form, type1_id, type2_id, intro_id,
                rarity_id, cp_used , attack_used, defense_used)
                VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,?)'''
       
       
        cursor.execute(a, pokemon_list)
        db.commit()
        db.close()
   
