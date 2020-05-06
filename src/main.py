from connector import *
import os
from datetime import datetime

clear = lambda: os.system('cls')

tables = {
    "1": "Auctions",
    "2": "Items",
    "3": "Players"
}


def main_loop():
    while True:
        clear()
        print("#####    MENU    #####")
        print("1. Tabele")
        print("2. Raport")
        print("3. Zamknij")
        while True:
            action = get_action(max_options=3)
            if not action: continue
            if action == "1":
                tables_loop()
                break
            elif action == "2":
                create_raport()
                break
            elif action == "3":
                return


def tables_loop():
    global tables
    while True:
        clear()
        print("#####    Wybierz tabele    #####")
        print("1. Aukcje")
        print("2. Przedmioty")
        print("3. Sprzedawcy")
        print("4. Wróć")

        while True:
            action = get_action(max_options=4)
            if action == "4":
                return
            elif action:
                table(tables[action])
                break


def create_raport():
    ### Queries ###
    query_1 = """select item_name, min_lvl, price, end_time, player_name
from Auctions
         join Players on Auctions.seller_id = Players.player_id
         join Items I on Auctions.item_id = I.item_id
    where end_time>GETDATE()"""
    query_1_info= {
        "item_name": {
            "data_type": "text"
        },
        "min_lvl": {
            "data_type": "int"
        },
        "price": {
            "data_type": "money"
        },
        "end_time": {
            "data_type": "datetime"
        },
        "player_name": {
            "data_type": "text"
        },
    }

    query_2 = """select item_name, AVG(price) as ave_price, COUNT(*) as amount from Auctions
join Items on Auctions.item_id = Items.item_id
group by item_name"""
    query_2_info= {
        "item_name": {
            "data_type": "text"
        },
        "ave_price": {
            "data_type": "money"
        },
        "amount": {
            "data_type": "int"
        }
    }

    query_3 = """select SUM(player_money) as all_money, COUNT(*) as player_nr, avg(player_money) as avg_player_money  from Players"""
    query_3_info= {
        "all_money": {
            "data_type": "money"
        },
        "player_nr": {
            "data_type": "int"
        },
        "avg_player_money": {
            "data_type": "money"
        }
    }


    with open("report.txt", "a+") as report:
        # TODO mogło być zrobione trochę sprytniej, ale chyba jest ok
        clear()

        header = f"      Raport z dnia {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}          "
        print("#"*(len(header)+1))
        print(header)
        print("#"*(len(header)+1))
        print("\n\n\n", file=report)
        print("#" * (len(header) + 1), file=report)
        print(header, file=report)
        print("#" * (len(header) + 1), file=report)

        print("\n\n\n#####            AKTUALNE AUKCJE            #####\n", file=report)
        print("\n\n\n#####            AKTUALNE AUKCJE            #####\n")
        data = query_data(query_1)
        pretty_data_print(data, query_1_info, to_file=report)

        print("\n\n\n#####         PRZEDMIOTY         #####", file=report)
        print("###    Wszystkie wystawione kiedykolwiek przedmioty z ", file=report)
        print("###    średnią ceną i częstością wystąpień \n", file=report)
        print("\n\n\n#####         PRZEDMIOTY         #####")
        print("###    Wszystkie wystawione kiedykolwiek przedmioty z ")
        print("###    średnią ceną i częstością wystąpień \n")

        # Wszystkie przedmioty na aukcji z nazwami wystawiających
        data = query_data(query_2)
        pretty_data_print(data, query_2_info, to_file=report)

        print("\n\n\n#####             SUMA PIENIĘDZY GRACZY            #####\n", file=report)
        print("\n\n\n#####             SUMA PIENIĘDZY GRACZY            #####\n")
        data = query_data(query_3)
        pretty_data_print(data, query_3_info, to_file=report)

    input("Wróć")


def table(table_name):
    while True:
        clear()
        print("#####    Wybierz akcje    #####")
        print("1. Wyświetl tabele")
        print("2. Edytuj tabele")
        print("3. Wróć")
        while True:
            action = get_action(max_options=3)

            if action == "3":
                return
            elif action == "1":
                show_table(table_name)
                input("Wróć")
                break

            elif action == "2":
                edit_table_loop(table_name)
                break


def edit_table_loop(table_name):
    while True:
        clear()
        print("#####    Wybierz akcje    #####")
        print("1. Dodaj wiersz")
        print("2. Edytuj dane")
        print("3. Usuń wiersze")
        print("4. Wróć")
        while True:
            action = get_action(max_options=4)
            if not action:
                continue

            col_info = get_data_info(table_name)

            if action == "4":
                return
            elif action == "1":
                values = get_values_loop(table_name, col_info)
                add_row(table_name, list(col_info.keys()), values)
                input("Wróć")
                break

            elif action == "2":
                edit_data_loop(table_name, col_info)
                break

            elif action == "3":
                delete_data_loop(table_name, col_info)
                break


def get_values_loop(table_name, column_info):
    values = []
    for col in column_info.keys():
        clear()
        print(f"###  Dodawanie wiersza do tabeli {table_name}  ###")
        print(f"    Nazwa kolumny:   {col}")
        print(f"    Typ danej:       {column_info[col]['data_type']}")
        print(f"    Może być pusta?: {column_info[col]['nullable']}\n")
        value = input("Wprowadź wartość: ")
        value = convert_value(value, column_info[col]['data_type'])
        values.append(value)
    return values


def edit_data_loop(table_name, col_info):
    filters = select_filters_loop(table_name, col_info)
    changes = get_changes_loop(table_name, col_info)
    query = f"UPDATE {table_name} \n SET {changes} \n WHERE {filters}"
    did_update, message = query_run(query)
    if did_update:
        print("Udało się prawidłowo zedytować tabele")
    else:
        print(message)
    return


def delete_data_loop(table_name, col_info):
    while True:
        clear()
        print("#####    Wybierz akcje    #####")
        print("1. Usuń wiersze spełniające warunek")
        print("2. Wróć")
        while True:
            action = get_action(max_options=2)
            if action: break

        if action == "2":
            return
        elif action == "1":
            query_filter = select_filters_loop(table_name, col_info)
            query = f"DELETE from {table_name} where {query_filter}"
            query_run(query)
            break


def select_filters_loop(table_name, col_info):
    statement = ""
    first_added = False
    while True:
        if not first_added:
            column, value = select_column_value(col_info)
            statement = f"{column} = {value}"
            first_added = True
        clear()
        print("#####    Dodaj kolejny warunek    #####")
        print("1. I")
        print("2. Lub")
        print("3. Zakończ")
        while True:
            action = get_action(max_options=3)
            if action: break

        if action == "3":
            return statement
        elif action == "1":
            statement += " and "
            column, value = select_column_value(col_info)
        elif action == "2":
            statement += " or "
            column, value = select_column_value(col_info)
        statement += f" {column} = {value} "


def get_changes_loop(table_name, col_info):
    statement = ""
    first_added = False
    while True:
        if not first_added:
            column, value = select_column_value(col_info)
            statement = f"{column} = {value}"
            first_added = True
        clear()
        print("#####    Zmień kolejną wartość    #####")
        print("1. Tak")
        print("2. Nie, zakończ")
        while True:
            action = get_action(max_options=2)
            if action: break

        if action == "2":
            return statement
        elif action == "1":
            column, value = select_column_value(col_info)
        statement += f", {column} = {value} "


def select_column_value(column_info):
    col_names = list(column_info.keys())
    n = len(col_names) + 1
    clear()
    print(f"###  Wybierz kolumne  ###")

    for i, column_name in enumerate(col_names):
        print(f"{i + 1}. {column_name}")

    while True:
        action = get_action(max_options=n + 1)
        if not action:
            continue
        action = int(action)
        break

    column = list(column_info.keys())[int(action) - 1]

    clear()
    print(f"###  Wprowadź wartość  ###")
    print(f"    Nazwa kolumny:   {col_names[action - 1]}")
    print(f"    Typ danej:       {column_info[col_names[action - 1]]['data_type']}")
    print(f"    Może być pusta?: {column_info[col_names[action - 1]]['nullable']}\n")
    filter_value = input()
    filter_value = convert_value(filter_value, column_info[col_names[action - 1]]['data_type'])

    if filter_value is int or filter_value is float:
        value = f"{filter_value}"
    elif filter_value is str:
        value = f"'{filter_value}'"
    else:
        value = f"{filter_value}"

    return column, value


def show_table(table_name):
    clear()
    print(f"### Tabela: {table_name}   ###")
    data = query_table(table_name)
    data_info = get_data_info(table_name)
    pretty_data_print(data, data_info)


def pretty_data_print(data, data_info,to_file = False):
    lengths = get_lengths(data_info)
    lengths_list = list(lengths.values())

    print_header(list(data_info.keys()), lengths,to_file)

    for row in data:
        row_srt = f""
        for i, value in enumerate(row):
            row_srt += "{0: ^{1}}|".format(str(value).strip(), lengths_list[i])
        if to_file:
            print(row_srt,file=to_file)
        print(row_srt)


def get_lengths(data_info):
    lenghts = {}
    for column in data_info.keys():
        if data_info[column]['data_type'] in ["bigint", "int"]:
            lenghts[column] = 12
        elif data_info[column]['data_type'] == "money":
            lenghts[column] = 20
        elif data_info[column]['data_type'] == "text":
            lenghts[column] = 25
        elif data_info[column]['data_type'] == "datetime":
            lenghts[column] = 30
    return lenghts


def print_header(col_names, lengths,to_file):
    header = ""
    for column in col_names:
        header += "{0: ^{1}}|".format(column, lengths[column])
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    if to_file:
        print("-" * len(header),file = to_file)
        print(header,file = to_file)
        print("-" * len(header),file = to_file)


def get_action(max_options):
    action = input("Wybierz akcje: ")
    if not correct_action(action, max_options):
        print("Niepoprawna akcja, spróbuj jeszcze raz")
        return False
    return action


def convert_value(value, val_type):
    if val_type in ["bigint", "int"]:
        return int(value)
    elif val_type == "money":
        return float(value)
    elif val_type == "text":
        return value
    elif val_type == 'datetime':
        datetime_object = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        return datetime_object
    else:
        print("Nienznay format danej")


def correct_action(action, max, min=1):
    try:
        action = int(action)
    except ValueError:
        return False

    if action >= min and action <= max:
        return True
    return False


if __name__ == "__main__":
    main_loop()
