#!/usr/bin/env python3

"""
	blockchain_db_server.py - BlockchainDB Server
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""
from pydantic import BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials


from fastapi.templating import Jinja2Templates


from uuid import uuid4
from random import randint
import random

from src.blockchain_core import BlockchainDB

class Vote(BaseModel):
    id: int
    pm: list = ['bibi', 'benet', 'gantz']

app = FastAPI(docs_url='/docs', redoc_url='/redoc')
app.add_middleware(PrometheusMiddleware,
                   app_name='blockchain-voting',
                   skip_paths=['/health'])
security = HTTPBasic()
app.add_route("/metrics", handle_metrics)
blockchain_db_manager = BlockchainDB()
templates = Jinja2Templates(directory="src/templates")

@app.get('/health')
async def health():
    """
    Health Check URL.
    The Healthchek quiries the Database to get the last block
    """
    try:
        response = {
            'chain': [blockchain_db_manager.get_last_block()],
            'length': 1,
            'header': 'Last Block'
        }
    except:
        raise HTTPException(
            status_code=503,
            detail="Service Unavaliable",
            headers={"X-Error": "There goes my error"},
        )
    return {"status": "healthy"}

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """
    Welcome to Blockchain message
    :return: HTML
    """
    response = {
        'header': 'Welcome to BlockchainDB'
    }    
    return templates.TemplateResponse("landing.html", {"request": request, "data": response})

@app.get('/reset', response_class=HTMLResponse)
async def reset(request: Request):
    """
    Drop the database and start all over again by creating the genesis block.
    Run once when start, or whenever you feel like dropping!
    :return: HTML
    """
    blockchain_db_manager.reset()
    response = {
        'header': 'Successfully generated a genesis block'
    }
    return templates.TemplateResponse("landing.html", {"request": request, "data": response})

@app.get('/mine/{number}', response_class=HTMLResponse)
async def mine_blocks(request: Request, number: int):
    """
    Mine for a some number of blocks with random generated transactions.
    :return: HTML
    Here we can get the payload and mine it
    {"id": <ID>, "vote_id": <number>}
    """
    transactions_range = randint(1, 10)
    pm = ['bibi','benet','gantz']
    for i in range(number):
        for transaction in range(transactions_range):
            blockchain_db_manager.add_transaction(sender=(str(uuid4()).replace('-', '')[:-10]),
                                          recipient=pm[random.randint(0,2)],
                                          amount=1)
        blockchain_db_manager.mine_for_next_block()

    response = {
        'header': 'Successfully mined {0} blocks'.format(number)
    }

    return templates.TemplateResponse("landing.html", {"request": request, "data": response})

@app.get('/view/chain', response_class=HTMLResponse)
async def view_blockchain(request: Request):
    """
    View the full BlockChain.
    :return: HTML
    """
    response = {
        'chain': blockchain_db_manager.get_all_blocks(),
        'length': blockchain_db_manager.get_length(),
        'header': 'Full chain'
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})

@app.get('/view/last_blocks/{number}', response_class=HTMLResponse)
async def view_last_n_block(request: Request, number: int):
    """
    View the last number of mined blocks.
    :param number: Number of blocks
    :return: HTML
    """
    # Reverse order to display latest ones to oldest one
    temp = []
    blocks = blockchain_db_manager.get_last_n_blocks(number)
    for i in range(number - 1, -1, -1):
        
        temp.append(blocks[i])

    response = {
        'chain': temp,
        'length': number,
        'header': 'Last {0} Blocks'.format(number)
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})

@app.get('/view/last_block', response_class=HTMLResponse)
async def view_last_block(request: Request):
    """
    View the last block.
    :return: HTML
    """
    response = {
        'chain': [blockchain_db_manager.get_last_block()],
        'length': 1,
        'header': 'Last Block'
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})

@app.get('/view/genesis_block', response_class=HTMLResponse)
async def view_genesis_block(request: Request):
    """
    View the genesis block.
    :return: HTML
    """
    response = {
        'chain': [blockchain_db_manager.get_genesis_block()],
        'length': 1,
        'header': 'Genesis Block'
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})

@app.get('/view/block/{number}', response_class=HTMLResponse)
async def view_block(request: Request, number: int):
    """
    View a specific block for a given height number.
    :param number: Block height
    :return: HTML
    """
    response = {
        'chain': [blockchain_db_manager.get_block(number)],
        'length': 1,
        'header': 'Block {0}'.format(number)
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})

@app.get('/view/top/{number}/{state}}', response_class=HTMLResponse)
async def view_top_blocks(request: Request, number: int, state: str):
    """
    View a number of top blocks for a given state.
    :param number: Number of blocks
    :param state: difficulty | elapsed_time | block_reward | hash_power | height | nonce | number_of_transaction
    :return: HTML
    """
    # Reverse order to display latest ones to oldest one
    temp = []
    blocks = blockchain_db_manager.get_top_blocks(state=state, number=number)
    for i in range(number - 1, -1, -1):
        temp.append(blocks[i])

    response = {
        'chain': temp,
        'length': number,
        'header': 'Top {0} {1}'.format(number, state)
    }
    return templates.TemplateResponse("chain.html", {"request": request, "data": response})


@app.post('/vote}')
async def vote(item: Vote):
    """
    Mine for a some number of blocks with random generated transactions.
    :return: HTML
    Here we can get the payload and mine it
    {"id": <ID>, "vote_id": <number>}
    """

    blockchain_db_manager.add_transaction(sender=item.id,
                                    recipient=item.vote,
                                    amount=1)
    blockchain_db_manager.mine_for_next_block()