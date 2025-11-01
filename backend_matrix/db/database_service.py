from firebase_admin import firestore
from typing import Dict, List
from firebase import db
import datetime

class DatabaseService:
    def __init__(self):
        self.db = db
        self.news_ref = self.db.collection('news')
        self.factcheck_ref = self.db.collection('factcheck')
    
    def store_news(self, news_list: List[Dict]):
        batch = self.db.batch()
        for news in news_list:
            doc_ref = self.news_ref.document()
            news['processed'] = False
            batch.set(doc_ref, news)
        batch.commit()
        
    def store_factcheck(self, news_id: str, factcheck: Dict):
        self.news_ref.document(news_id).update({'processed': True})

        return self.factcheck_ref.document(news_id).set(factcheck)
        
    def get_unprocessed_news(self):
        query = self.news_ref.where('processed', '==', False).limit(1)
        docs = query.get()
        return next((doc.to_dict() | {'id': doc.id} for doc in docs), None)
        
    # def get_all_news_with_factchecks(self):
    #     news_docs = self.news_ref.get()
    #     result = []
    #     for news in news_docs:
    #         news_data = news.to_dict() | {'id': news.id}
    #         factcheck = self.factcheck_ref.document(news.id).get()
    #         news_data['factcheck'] = factcheck.to_dict() if factcheck.exists else None
    #         result.append(news_data)
    #     return result

    def get_all_news_with_factchecks(self):
        factcheck_docs = self.factcheck_ref.get()
        result = [doc.to_dict() | {'id': doc.id} for doc in factcheck_docs]
        return result
    def store_user_broadcast(self, user_data: Dict):
        doc_ref = self.db.collection('user_broadcast').document()
        return doc_ref.set(user_data), doc_ref.id

    def get_all_user_broadcasts(self):
        user_docs = self.db.collection('user_broadcast').get()
        return [doc.to_dict() | {'id': doc.id} for doc in user_docs]

    def get_game_pairs(self):
        """Fetch all game pairs from database"""
        collection = self.db.game_pairs
        return list(collection.find({}))

    def get_game_pair(self, pair_id):
        """Fetch specific game pair"""
        collection = self.db.game_pairs
        return collection.find_one({'id': pair_id})

    def save_game_vote(self, pair_id, choice, user_id):
        """Save user vote"""
        collection = self.db.game_votes
        vote = {
            'pair_id': pair_id,
            'choice': choice,
            'user_id': user_id,
            'timestamp': datetime.utcnow()
        }
        collection.insert_one(vote)

    def init_db(self):
        """Initialize database with game data"""
        # Create game_pairs collection if it doesn't exist
        if 'game_pairs' not in self.db.collections():
            game_pairs = self.db.collection('game_pairs')
        else:
            game_pairs = self.db.collection('game_pairs')

        # Add initial game data
        initial_pairs = [
            {
                "id": "pair-001",
                "items": [
                    {
                        "id": "item-1",
                        "type": "article",
                        "title": "Local Weather Service Predicts Mild Summer",
                        "url": "https://example.com/weather",
                        "excerpt": "Meteorologists at the National Weather Service predict temperatures will remain mild...",
                        "is_fake": False,
                        "explanation": "This article comes from a verified weather service and includes specific, verifiable predictions."
                    },
                    {
                        "id": "item-2",
                        "type": "article",
                        "title": "Scientists Discover Weather Control Device",
                        "url": "https://weather-news.biz/control",
                        "excerpt": "A revolutionary device that can control weather patterns has been invented...",
                        "is_fake": True,
                        "explanation": "This article makes extraordinary claims without evidence and uses a suspicious domain."
                    }
                ]
            }
        ]

        # Add pairs to database
        for pair in initial_pairs:
            game_pairs.document(pair['id']).set(pair)

        print("Database initialized with game pairs")
