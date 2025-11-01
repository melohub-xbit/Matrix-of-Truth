from flask import Blueprint, jsonify, request, abort
import json, random, os
from db.database_service import DatabaseService

bp = Blueprint('spot_game', __name__, url_prefix='/api/spot-game')
db = DatabaseService()

@bp.route('/pair', methods=['GET'])
def get_pair():
    pairs = db.get_game_pairs()
    if not pairs:
        return jsonify({'error': 'no pairs available'}), 404
    
    pair = random.choice(pairs)
    safe_items = []
    for item in pair['items']:
        safe = {k: v for k, v in item.items() if k not in ('is_fake', 'explanation')}
        safe_items.append(safe)
    return jsonify({'id': pair['id'], 'items': safe_items})

@bp.route('/answer/<pair_id>', methods=['GET'])
def get_answer(pair_id):
    pair = db.get_game_pair(pair_id)
    if not pair:
        return jsonify({'error': 'pair not found'}), 404
        
    answer_index = next((i for i, it in enumerate(pair['items']) if it.get('is_fake')), None)
    explanations = [it.get('explanation', '') for it in pair['items']]
    return jsonify({'id': pair['id'], 'answer_index': answer_index, 'explanations': explanations})

@bp.route('/vote', methods=['POST'])
def vote():
    body = request.get_json(silent=True) or {}
    pair_id = body.get('pair_id')
    choice = body.get('choice')
    user_id = body.get('user_id', 'anonymous')
    
    if pair_id is None or choice is None:
        abort(400)
        
    db.save_game_vote(pair_id, choice, user_id)
    return jsonify({'ok': True})