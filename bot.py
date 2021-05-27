import argparse
import logging
import os
from datetime import datetime, timedelta
from random import randint
import requests
from telegram.ext import (BaseFilter, CommandHandler, Filters,
                          InlineQueryHandler, MessageHandler, Updater)

from db import (create_connection, create_table, create_number, get_all_numbers, get_number, delete_number, delete_all_numbers)


def args_read():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-path', required=True)

    args = parser.parse_args()
    return args



def add_number(update, context):
    try:
        args = args_read()
        conn = create_connection(args.db_path)

        if len(context.args) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Debe tener el formato:\n\n/add número alias')
            return

        numero = int(context.args[0])
        alias = context.args[1]

        space = get_number(conn, numero)
        if len(space) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Imposible añadir el número {numero}')
            return
        if space[0][1] != '':
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'El número {numero} ya se encuentra tomado por {space[0][1]}')
            return

        delete_number(conn, numero)
        create_number(conn, numero, alias)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ahora el número {numero} le pertenece a {alias}')
        return

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Debe tener el formato:\n\n/add número alias')
        print(e)
        return

    #SEND TO CHANNEL
    # context.bot.forward_message(chat_id='', from_chat_id=update.message.chat_id, message_id=update.message.message_id)


def new_sorteo(update, context):
    try:
        args = args_read()
        conn = create_connection(args.db_path)

        if len(context.args) != 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Debe tener el formato:\n\n/new cantidad_maxima_de_participantes')
            return

        delete_all_numbers(conn)

        numero = int(context.args[0])

        for i in range(1, numero + 1):
            create_number(conn, i, '')

        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Sorteo de {numero} personas creado con éxito')
        return

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Debe tener el formato:\n\n/new cantidad_maxima_de_participantes')
        print(e)
        return


def get_list(update, context):
    args = args_read()
    conn = create_connection(args.db_path)

    lista = get_all_numbers(conn)
    message_lista = ''
    for i in lista:
        message_lista += f'{i[0]}: {i[1]}\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{message_lista}')
    return

def random_number(update, context):
    args = args_read()
    conn = create_connection(args.db_path)

    lista = get_all_numbers(conn)
    r = randint(1, len(lista))

    winner = get_number(conn, r)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ha ganado el número {r}: {winner[0][1]}')
    return



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola!!!")
        

def main():
    logger = logging.getLogger(__name__)

    args = args_read()
    print('database:', args.db_path)

    conn = create_connection(args.db_path)

    sql_create_numeros_table = """ CREATE TABLE IF NOT EXISTS numeros (
                                        id integer PRIMARY KEY,
                                        alias text NOT NULL
                                    ); """

    if conn is not None:
        create_table(conn, sql_create_numeros_table)
    else:
        print("Error! cannot create the database connection.")

    updater = Updater(token='1790107525:AAEPXpSPn1kDBlX-n0Zi3rx6ta0GnoZmKG4', use_context=True)
    dispatcher = updater.dispatcher

    admin_group_id = -1001322740976

    start_handler = CommandHandler('start', start, Filters.chat(admin_group_id))
    dispatcher.add_handler(start_handler)

    new_sorteo_handler = CommandHandler('new', new_sorteo, Filters.chat(admin_group_id))
    dispatcher.add_handler(new_sorteo_handler)

    add_number_handler = CommandHandler('add', add_number, Filters.chat(admin_group_id))
    dispatcher.add_handler(add_number_handler)

    get_list_handler = CommandHandler('list', get_list, Filters.chat(admin_group_id))
    dispatcher.add_handler(get_list_handler)

    random_handler = CommandHandler('random', random_number, Filters.chat(admin_group_id))
    dispatcher.add_handler(random_handler)

    updater.start_polling()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    main()
