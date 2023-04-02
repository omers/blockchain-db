import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to BlockchainDB' in response.data

def test_reset(client):
    response = client.get('/reset')
    assert response.status_code == 200
    assert b'Successfully generated a genesis block' in response.data

def test_mine_blocks(client):
    response = client.get('/mine/1')
    assert response.status_code == 200
    assert b'Successfully mined 1 blocks' in response.data

def test_view_blockchain(client):
    response = client.get('/view/chain')
    assert response.status_code == 200
    assert b'Full chain' in response.data

def test_view_last_n_block(client):
    response = client.get('/view/last_blocks/1')
    assert response.status_code == 200
    assert b'Last 1 Blocks' in response.data

def test_view_last_block(client):
    response = client.get('/view/last_block')
    assert response.status_code == 200
    assert b'Last Block' in response.data

def test_view_genesis_block(client):
    response = client.get('/view/genesis_block')
    assert response.status_code == 200
    assert b'Genesis Block' in response.data

def test_view_block(client):
    response = client.get('/view/block/1')
    assert response.status_code == 200
    assert b'Block 1' in response.data

def test_view_top_blocks(client):
    response = client.get('/view/top/1/difficulty')
    assert response.status_code == 200
    assert b'Top 1 difficulty' in response.data
