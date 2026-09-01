import { useState } from 'react'

import {
    create_game,
    deal,
    hit,
    stand
} from "./api";

import Card from "./components/Card";
import Hand from "./components/Hand";
import GameControls from "./components/GameControls";
import GameInfo from "./components/GameInfo";

import './App.css'

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);

  const [balance, setBalance] = useState(1000);
  const [bet, setBet] = useState(100);

  const [error, setError] = useState(null);

  async function handleStartGame() {
    try {
        setError(null);

        const game = await create_game(balance);

        setGameId(game.game_id);

        const state = await deal(
            game.game_id,
            bet
        );
        setGameState(state)
    } catch (error) {
        setError(error.message);
    }
  }

  async function handleHit() {
    try {
        setError(null);
        
        const state = await hit(gameId);

        setGameState(state)
    } catch (error) {
        setError(error.message);
    }
  }

  async function handleStand() {
    try {
        setError(null);

        const state = await stand(gameId);

        setGameState(state)

    } catch (error) {
        setError(error.message);
    }
  }

  return (
    <div className = "app">
        <h1>BLACKJACK</h1>
        {!gameState && (
            <div className = "start-menu">
                <label>
                    Starting Balance: 
                    <input
                        type = "number"
                        value = {balance}
                        onChange = {(event) => setBalance(Number(event.target.value))}
                    />
                </label>
                <label>
                    Bet:
                    <input
                        type = "number"
                        value = {bet}
                        onChange = {(event) => setBet(Number(event.target.value))}
                    />
                </label>

                <button onClick = {handleStartGame}>
                    Start Game
                </button>
            </div>
        )}

        {error && (
            <p className = "error">
                {error}
            </p>
        )}

        {gameState && (
            <div className = "table">
                <GameInfo
                    gameState = {gameState}
                />

                <section className = "dealer">
                    <h2>Dealer</h2>
                    <div className = "cards">
                        {gameState.dealer.cards.map(
                            (card, index) => (
                                <Card
                                    key = {index}
                                    card = {card}
                                />
                            )
                        )}
                    </div>
                    <p>
                        Value: {gameState.dealer.value}
                    </p>
                </section>
                
                <section className = "player">
                        <h2>Player</h2>
                        {gameState.player.hands.map(
                            (hand, index) => (
                                <Hand
                                    key = {index}
                                    hand = {hand}
                                />
                            )
                        )}
                </section>
                
                <GameControls
                    onHit = {handleHit}
                    onStand = {handleStand}
                    disabled = {false}
                />

            </div>
        )}
    </div>
  )
}
export default App
