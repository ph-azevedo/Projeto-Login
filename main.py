import sqlite3
from sqlite3 import Error
con = sqlite3.connect('database.db')
cur = con.cursor()


def menu():
    print('Olá! Escolha o que quer fazer:')
    print('1. Login\n2. Cadastro\n3. Recuperar senha\n4. Sair')
    option = int(input('Qual a opção desejada? '))
    if option == 1:
        login()
    elif option == 2:
        cadastra_usuario()
    elif option == 3:
        recupera_senha()
    elif option == 4:
        exit()

# Função utilizada para criar a tabela no db. Não é utilizada no código
# def cria_tabela():
#     try:
#         cur.execute("""CREATE TABLE tb_users(
#                         N_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                         T_NOME VARCHAR,
#                         T_MAIL VARCHAR,
#                         T_USUARIO VARCHAR(15),
#                         T_PASSWORD VARCHAR(8)
#                     )""")
#         print('Tabela Criada')
#     except Error as ex:
#         print(ex)


def cadastra_usuario():
    nome = input('Nome completo: ')
    email = input('E-Mail: ')
    nascimento = input('Data de nascimento (XX/XX/XXXX): ')
    user = input('Nome de usuário: ')
    password = input('Senha (até 8 caracteres): ')
    confirma_password = input('Confirme sua senha: ')
    while password != confirma_password:
        print('Senhas diferentes. Tente novamente.')
        password = input('Senha (até 8 caracteres): ')
        confirma_password = input('Confirme sua senha: ')
    try:
        cur.execute(f"""INSERT INTO tb_users (T_NOME, T_MAIL, T_USUARIO, T_PASSWORD, T_NASCIMENTO)
                         VALUES('{nome}', '{email}', '{user}', '{password}', '{nascimento}')
                     """)
        con.commit()
        print('Usuário cadastrado.')
        menu()
    except Error as ex:
        print('Erro ao cadastar o usuário. Informe o erro abaixo ao seu administrador.')
        print(ex)
        menu()


def login():
    user = input('Nome de usuário: ')
    password = input('Senha: ')
    cur.execute(f"SELECT N_ID, T_PASSWORD FROM tb_users WHERE T_USUARIO = '{user}'")
    resultado = cur.fetchall()
    senha = (resultado[0])[1]
    global id
    id = (resultado[0])[0]
    if password == senha:
        print('Logado!')
        menu_logado()
    elif password != senha:
        print('Senha incorreta. Tente novamente.')
        login()


def altera_senha():
    old_pass = input('Digite a senha antiga: ')
    cur.execute(f"SELECT T_PASSWORD FROM tb_users WHERE N_ID = '{id}'")
    resultado = ((cur.fetchall())[0])[0]
    if old_pass == resultado:
        new_pass = input('Digite a nova senha: ')
        new_pass_c = input('Confirme a nova senha: ')
        while new_pass != new_pass_c:
            print('Senhas diferentes. Tente novamente.')
            new_pass = input('Digite a nova senha: ')
            new_pass_c = input('Confirme a nova senha: ')
        if new_pass == new_pass_c:
            cur.execute(f"UPDATE tb_users SET T_PASSWORD='{new_pass}' WHERE N_ID = {id}")
            con.commit()
            print('Senha alterada!')
            menu_logado()


def menu_logado():
    print('Olá! Escolha o que quer fazer:')
    print('1. Alterar senha\n2. Ver meus dados\n3. Logoff')
    option = int(input('Qual a opção desejada? '))
    if option == 1:
        altera_senha()
    elif option == 2:
        ver_dados()
    elif option == 3:
        menu()



def ver_dados():
    cur.execute(f"SELECT T_NOME, T_MAIL, T_USUARIO, T_NASCIMENTO FROM tb_users WHERE N_ID = '{id}'")
    resultado = (cur.fetchall()[0])
    print()
    print()
    print(f'Nome: {resultado[0]}')
    print(f'E-Mail: {resultado[1]}')
    print(f'Usuário: {resultado[2]}')
    print(f'Data de Nascimento: {resultado[3]}')
    print()
    print()
    menu_logado()

def recupera_senha():
    user = input('Digite seu nome de usuário: ')
    email = input('Digite seu email: ')
    nascimento = input('Digite sua data de nascimento: ')
    cur.execute(f"SELECT T_PASSWORD FROM tb_users WHERE (T_USUARIO = '{user}' AND T_MAIL = '{email}' AND T_NASCIMENTO = '{nascimento}')")
    resultado = cur.fetchall()
    senha = (resultado[0])[0]
    print(f'Sua senha é: {senha}')
    print()
    menu()

menu()