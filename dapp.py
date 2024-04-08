import asyncio
import logging
from cartesify_backend import CartesifyBackend, CartesifyOptions
from quart import Quart, request, jsonify


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
    response_data = {'some': 'response', 'senderAddress': sender_address}
    logger.info(f'response is {response_data}')
    return jsonify(response_data)

@app.route('/new-game', methods=['POST'])
async def new_game():
    logger.info("Requisição recebida no endpoint new_game")
    print("Requisição recebida no endpoint new-game")
    sender_address = request.headers.get('x-msg_sender')
    commit = request.body['commit']
    games.append({'player1': sender_address, 'commit1': commit})
    return jsonify({'created': len(games)})

async def run_quart():
    logger.info(f'Starting Quart on port {port}')
    app.run(port=port)
    logger.info(f'Quart started on port {port}')
async def run_cartesify():
    logger.info(f'Starting Cartesify')
    options = CartesifyOptions(url='', broadcast_advance_requests=False)
    cartesify_app = CartesifyBackend().create_app(options)

    asyncio.create_task(cartesify_app.start())

    logger.info("Cartesify started")

async def main():
    try:
        logger.info(f'Initiating app')

        await asyncio.gather(run_quart(), run_cartesify())

    except Exception as e:
        print(e)
        logger.error(e)

if __name__ == '__main__':
    asyncio.run(main())
















