import asyncio

from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 2877537
api_hash = '59f641860ce2abb7112e1e117efbc479'


# Press the green button in the gutter to run the script.
async def process_message(client_api, client_id, message):
    try:
        username = await client_api.get_entity(client_id)
        # print(username)
        result = await client_api.send_message(username, message)
        # print(result)
        return True, result
    except ValueError:
        return False, 'No user'


async def send_message_to_clients(client_api, client_id_list, message):
    await asyncio.gather(*[process_message(client_api, client_id, message) for client_id in client_id_list])


def run_send_message_to_clients(clients_ids, message, api_id, api_hash):
    with TelegramClient('anon', api_id, api_hash) as client_api:
        client_api.loop.run_until_complete(send_message_to_clients(client_api, clients_ids, message))


def run_send_message_to_client(client_id, message, api_id, api_hash):
    with TelegramClient('anon', api_id, api_hash) as client_api:
        client_api.loop.run_until_complete(process_message(client_api, client_id, message))


if __name__ == '__main__':
    run_send_message_to_clients(['me', 'me'], 'TEST', api_id, api_hash)
    # with TelegramClient('anon', api_id, api_hash) as client:
        # client.loop.run_until_complete(process_message(client, '+380937768660', 'Тест Привет!')) # DEFERENT USER
        # client.loop.run_until_complete(process_message(client, '+380000999999', 'Тест Привет!')) # ERROR
    #    client.loop.run_until_complete(process_message(client, 'me', 'Тест Привет!'))  # ME
