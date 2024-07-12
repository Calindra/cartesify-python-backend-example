import asyncio
import logging
from cartesify_backend import CartesifyBackend, CartesifyOptions
from quart import Quart, request, jsonify
import httpx


app = Quart(__name__)

logging.basicConfig(level=logging.DEBUG)

# Definindo um logger para a aplicação Flask
logger = logging.getLogger(__name__)

port = 8383

games = []

@app.route('/your-endpoint', methods=['GET'])
async def your_endpoint():
    logger.info("Requisição recebida no endpoint your-endpoint")
    print("Requisição recebida no endpoint your-endpoint")
    sender_address = request.headers.get('x-msg_sender')
    response_data = {'some': 'response', 'senderAddress': sender_address, 'games': len(games)}
    logger.info(f'response is {response_data}')
    return jsonify(response_data)

@app.route('/new-game', methods=['POST'])
async def new_game():
    logger.info("Requisição recebida no endpoint new_game")
    print("Requisição recebida no endpoint new-game")
    sender_address = request.headers.get('x-msg_sender')
    commit = await request.get_json()
    games.append({'player1': sender_address, 'commit1': commit})
    return jsonify({'created': len(games)})

async def main():
    try:
        logger.info(f'Initiating app')

        options = CartesifyOptions(url='http://127.0.0.1:5004', broadcast_advance_requests=False)
        cartesify_app = CartesifyBackend().create_app(options)

        await asyncio.gather(app.run_task(port=port, host='0.0.0.0'), cartesify_app.start())

    except Exception as e:
        print(e)
        logger.error(e)

if __name__ == '__main__':
    asyncio.run(main())
















