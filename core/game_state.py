import json
import os
from datetime import datetime

class GameState:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.level = "mudah"
        self.game_mode = "kuis"  
        self.player_name = "Player"
        
    def reset(self):
        self.score = 0
        self.streak = 0
        
    def add_score(self, points):
        self.score += points
        self.streak += 1
        
    def break_streak(self):
        self.streak = 0
        
    def save_score(self):
        """Save score ke file JSON"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        data = {
            "player": self.player_name,
            "score": self.score,
            "level": self.level,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            if os.path.exists("data/scores.json"):
                with open("data/scores.json", "r") as f:
                    scores = json.load(f)
            else:
                scores = []
                
            scores.append(data)
            scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
            
            with open("data/scores.json", "w") as f:
                json.dump(scores, f, indent=2)
                
        except Exception as e:
            print(f"Error saving score: {e}")
    
    @staticmethod
    def load_scores():
        """Load high scores"""
        try:
            if os.path.exists("data/scores.json"):
                with open("data/scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return []