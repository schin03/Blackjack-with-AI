import json
import os

import google.generativeai as genai 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash") if API_KEY else None

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
def get_blackjack_state(game_snapshot: dict) -> dict:
    if model is None:
        raise RuntimeError("GEMINI_API_KEY is not configured on the server")

    prompt = f"""
    You are a blackjack basic-strategy assistant. Recommend one legal move
    for the given state.

    Use the dealer's visible up-card only. Only choose a move from
    allowed_moves.

    Return valid JSON only in this exact shape:
    {{"move":"hit|stand|double|split","explanation":"One or two short sentences."}}

    Game snapshot:
    {json.dumps(game_snapshot)}
    """

    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
            temperature = 0,
            max_output_tokens=200,
            response_mime_type = "application/json",
        ),
    )
    
    print("================== GEMINI RESPONSE ==================")
    print(response)
    print("=====================================================")
    
    text = response.text.strip()
    advice = json.loads(text)
    move = str(advice.get("move","")).lower()

    if move not in game_snapshot["allowed_moves"]:
        raise ValueError("AI returned illegal move for current hand")

    explanation = str(advice.get("explanation", "").strip())

    if not explanation:
        raise ValueError("AI did not include explananation")
    
    return {"move": move, "explanation": explanation}