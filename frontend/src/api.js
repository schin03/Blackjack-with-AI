const API_URL = "http://127.0.0.1:8000";
// const API_URL = import.meta.env.VITE_API_URL;

// create_game api call
export async function create_game(bal) {
  const res = await fetch(`${API_URL}/games?balance=${bal}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to create a game session");
  }

  return res.json();
}

// deal hand api call
export async function deal(game_id, bet) {
  const res = await fetch(`${API_URL}/games/${game_id}/deal`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      bet: bet,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to deal a hand in game session: " + game_id);
  }

  return res.json();
}

// insurance choice api call
export async function insurance(game_id, choice) {
    const res = await fetch(`${API_URL}/games/${game_id}/insurance`, {
       method: "POST",
       headers: {
        "Content-Type" : "application/json",
       },
       body: JSON.stringify({
        choice: choice,
       }),
    })

    if (!res.ok) {
        throw new Error("Failed to make insurance choice in game session: " + game_id)
    }

    return res.json();
}

// player hit hand api call
export async function hit(game_id) {
  const res = await fetch(`${API_URL}/games/${game_id}/hit`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to perform hit action in game session: " + game_id);
  }

  return res.json();
}

// player double hand api call
export async function double(game_id) {
  const res = await fetch(`${API_URL}/games/${game_id}/double`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to perform double action in game session: " + game_id);
  }

  return res.json();
}

// player stand hand api call
export async function stand(game_id) {
  const res = await fetch(`${API_URL}/games/${game_id}/stand`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to perform stand action in game session: " + game_id);
  }

  return res.json();
}
