import json
import os
import time

from google import genai
from google.genai import types
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key = API_KEY)

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

    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents = prompt,
                config = types.GenerateContentConfig(
                    max_output_tokens=100,
                    thinking_config = types.ThinkingConfig(
                        thinking_level = "minimal"
                    ),
                    response_mime_type = "application/json",
                ),
            )
            break
        except errors.ServerError as e:
            if attempt == max_retries -1:
                raise
            wait_time = 2 ** attempt
            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/{max_retries}). "
                f"Retrying in {wait_time}s..."
            )
            
            time.sleep(wait_time)
    
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