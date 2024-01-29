import sqlite3 
import unidecode
from pathlib import Path

# Create directory
ROOT_DIR = Path(__file__).parent
DB_NAME = 'db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'estoque'

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Clear table for work
sql = (
    f'DELETE FROM {TABLE_NAME}'
)
cursor.execute(sql)

sql = (
    f'DELETE FROM sqlite_sequence WHERE name = "{TABLE_NAME}"'
)
cursor.execute(sql)
connection.commit()

# Create table
sql = (
    f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
    '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'product TEXT,'
        'quantity INTEGER' 
    ')'
)
cursor.execute(sql)
connection.commit()

# Insert values
sql = (
    f'INSERT INTO {TABLE_NAME} '
    '(product, quantity) '
    'VALUES ' 
    '(:product, :quantity)'
)

cursor.executemany(sql, (
    {'product': 'agua','quantity': '10'},
    {'product': 'suco','quantity': '10'},
    {'product': 'refrigerante','quantity': '10'},
    {'product': 'picole','quantity': '10'},
    {'product': 'sorvete','quantity': '10'},
    {'product': 'agua-gas','quantity': '10'},
))
connection.commit()

print("--Registro de saída de estoque--")
if __name__ == "__main__":

    def getData():
        cursor.execute(f'SELECT * FROM {TABLE_NAME}')
        response = cursor.fetchall()
        return response
    
    def verifyQuantity(quantity):
        cursor.execute(f'SELECT quantity FROM {TABLE_NAME} WHERE product = "{quantity}"')
        response = cursor.fetchall()
        return response

    
    data = getData()
    _product = []

    for i in range(len(data)):
        _product.append(data[i][1])

    while True:
        product = input("Produto: ")
        output_quantity = int(input("Quantidade: "))

        format_product = unidecode.unidecode(product.lower())

        if format_product not in _product:
            print(f"{product} não existe no estoque, tente registrar a saída novamente! \n")
            continue

        quantity = verifyQuantity(product)

        if quantity[0][0] == 0:
            print(f"Produto em falta no estoque!")
            continue

        if output_quantity > quantity[0][0]:
            print("Quantidade indisponível em estoque! \n")
        else:
            sql_update = (
                f'UPDATE {TABLE_NAME} '
                f'SET quantity = (quantity - {output_quantity} )'
                f'WHERE product = "{format_product}"'
            )

            cursor.execute(sql_update)
            connection.commit()

        resp = input("Deseja registar mais itens de saída [S/N]?")

        print()
        
        if resp.upper() == "N":
            break



    data = getData()

    for row in data:
        _, product, quantity = row
        print(
            f'Produto: {product}, \n'
            f'Quantidade: {quantity} \n'
        )
        

    cursor.close()
    connection.close()