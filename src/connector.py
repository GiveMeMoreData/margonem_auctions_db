import pyodbc


#### TĄ LINIJKĘ NALEŻY ZMODYFIKOWAĆ BY POŁĄCZYĆ SIĘ Z ODPOWIEDNIĄ BAZĄ  ####
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=master;UID=sa;PWD=Bartusus11')

def query_table(table_name):
    cursor = cnxn.cursor()
    cursor.execute(f"select * from {table_name}")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def query_data(query):
    cursor = cnxn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def query_run(query):
    cursor = cnxn.cursor()
    try:
        cursor.execute(query)
        cursor.commit()
        cursor.close()
        return True, ok
    except Exception as e:
        return False, e

def filter_table_by(table,key,value):
    query = f"select * from {table} where {key}={value}"


def add_row(table_name,col_names, values_list):
    cursor = cnxn.cursor()
    values_representation = '?'+', ?'*(len(values_list)-1)
    col_str=_to_col_str(col_names)
    cursor.execute(f"insert into {table_name}({col_str}) values ({values_representation})",values_list)
    cursor.commit()
    cursor.close()

def get_col_names_list(table_name):
    cursor = cnxn.cursor()
    names=[]
    for row in cursor.columns(table=table_name):
        names.append(row.column_name)
    cursor.close()
    return names


def get_data_info(table_name):
    cursor = cnxn.cursor()
    names = {}
    for row in cursor.columns(table=table_name):
        names[row.column_name]={
            "data_type" : _read_type(row.data_type),
            "nullable" : bool(row.nullable)
        }
    cursor.close()
    return names

def _read_type(sql_data_type):
    if sql_data_type == -5:
        return "bigint"
    elif sql_data_type== -1:
        return "text"
    elif sql_data_type == 3:
        return "money"
    elif sql_data_type == 93:
        return "datetime"
    elif sql_data_type == 12:
        return "text"
    elif sql_data_type == 4:
        return "int"
    else:
        return sql_data_type

def _to_col_str(col_names):
    col_str=col_names.pop(0)
    for col_name in col_names:
        col_str+=f", {col_name}"
    return col_str

