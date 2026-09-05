import google.generativeai as genai
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

"""
    Sends the game snapshot to Gemini and returns the recommended move.
    game_snapshot should contain:
    {
        "player_hand": [...],
        "dealer_card": ...,
        "can_double": bool,
        "can_split": bool
    }
"""
def get_blackjack_state(game_snapshot: dict) -> str:
    prompt = f"""
    You are given a blackjack hand where player_hand contains their current hand's value and
    dealer_card is the value of the up facing card. You are also given booleans as to if the hand
    can be doubled or split, to maximize the player's winnings. Given the following game state, 
    return ONLY the recommended move:
    - "hit"
    - "stand"
    - "double"
    - "split"

    Game snapshot:
    {game_snapshot}
    """

    response = model.generate_content(prompt)
    return response.text.strip().lower()