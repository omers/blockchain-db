from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.bc_fastapi import app, blockchain_db_manager


client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy'}

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to BlockchainDB' in response.content

def test_reset():
    with patch.object(blockchain_db_manager, 'reset') as mock_reset:
        response = client.get('/reset')
        assert response.status_code == 200
        assert b'Successfully generated a genesis block' in response.content
        mock_reset.assert_called_once()

def test_mine_blocks():
    with patch.object(blockchain_db_manager, 'add_transaction') as mock_add_transaction,\
         patch.object(blockchain_db_manager, 'mine_for_next_block') as mock_mine_for_next_block:

        response = client.get('/mine/1')
        assert response.status_code == 200
        assert b'Successfully mined 1 blocks' in response.content
        mock_add_transaction.assert_called()
        mock_mine_for_next_block.assert_called()

def test_view_blockchain():
    with patch.object(blockchain_db_manager, 'get_all_blocks', return_value=[{'data': 'block1'}, {'data': 'block2'}]) as mock_get_all_blocks:
        response = client.get('/view/chain')
        assert response.status_code == 200
        assert b'Full chain' in response.content
        assert b'block1' in response.content
        assert b'block2' in response.content
        mock_get_all_blocks.assert_called_once()

# def test_view_last_n_block():
#     with patch.object(blockchain_db_manager, 'get_last_n_blocks', return_value=[{'data': 'block2'}, {'data': 'block1'}]) as mock_get_last_n_blocks:
#         response = client.get('/view/last_blocks/2')
#         assert response.status_code == 200
#         assert b'Last 2 Blocks' in response.content
#         assert b'block2' in response.content
#         assert b'block1' in response.content
#         mock_get_last_n_blocks.assert_called_once_with(2)

# def test_view_last_block():
#     with patch.object(blockchain_db_manager, 'get_last_block', return_value={'data': 'last_block'}) as mock_get_last_block:
#         response = client.get('/view/last_block')
#         assert response.status_code == 200
#         assert b'Last Block' in response.content
#         assert b'last_block' in response.content
#         mock_get_last_block.assert_called_once()

# def test_view_genesis_block():
#     with patch.object(blockchain_db_manager, 'get_genesis_block', return_value={'data': 'genesis_block'}) as mock_get_genesis_block:
#         response = client.get('/view/genesis_block')
#         assert response.status_code == 200
#         assert b'Genesis Block' in response.content
#         assert b'genesis_block' in response.content
#         mock_get_genesis_block.assert_called_once()

# def test_view_block():
#     with patch.object(blockchain_db_manager, 'get_block', return_value={'data': 'block_1'}) as mock_get_block:
#         response = client.get('/view/block/1')
#         assert response.status_code == 200
#         assert b'Block 1' in response.content
#         assert b'block_1' in response.content
#         mock_get_block.assert_called_once_with(1)
