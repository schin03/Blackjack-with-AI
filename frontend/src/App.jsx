import { useState } from 'react'

import {
    create_game,
    deal,
    insurance,
    hit,
    split,
    double,
    stand
} from "./api";

import Card from "./components/Card";
import Hand from "./components/Hand";
import GameControls from "./components/GameControls";
import GameInfo from "./components/GameInfo";
import InsurancePopup from './components/InsurancePopup';

import './App.css'

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);

  const [balance, setBalance] = useState(1000);
  const [bet, setBet] = useState(100);

  const [error, setError] = useState(null);

  // --------------------------
  // Start new session
  // --------------------------
  async function handleStartSession() {
    try {
        setError(null);

        const game = await create_game(balance);

        setGameId(game.game_id);

    } catch (error) {
        setError(error.message);
    }
  }

  // --------------------------
  // Deal new hand
  // --------------------------
  async function handleDeal() {
    try {
        setError(null);

        const state = await deal(gameId, bet);

        setGameState(state);

    } catch (err) {
        setError(err.message);
    }
  }

  async function handleInsuranceChoice(choice) {
    try {
        setError(null);

        const state = await insurance(gameId, choice);

        setGameState(state);
    } catch (err) {
        setError(err.message);
    }
  }

  // --------------------------
  // Hit
  // --------------------------
  async function handleHit() {
    try {
        setError(null);
        
        const state = await hit(gameId);

        setGameState(state)
    } catch (error) {
        setError(error.message);
    }
  }

  // --------------------------
  // Double
  // --------------------------
  async function handleDouble() {
    try {
        setError(null);
        
        const state = await double(gameId);

        setGameState(state);
    } catch (error) {
        setError(error.message);
    }
  }

  // --------------------------
  // Split
  // --------------------------
  async function handleSplit() {
    try {
        setError(null);

        const state = await split(gameId);

        setGameState(state);

    } catch (e) {
        setError(e.message);
    }
  }


  // --------------------------
  // Stand
  // --------------------------
  async function handleStand() {
    try {
        setError(null);

        const state = await stand(gameId);

        setGameState(state)

    } catch (error) {
        setError(error.message);
    }
  }

  // --------------------------
  // Return to start session 
  // --------------------------
  function handleHome() {
    setGameId(null);
    setGameState(null);
    setError(null);
  }

  const activeHandIndex = gameState?.player.current_hand ?? 0;
  const activeHand = gameState?.player.hands[activeHandIndex];

  return (
    <div className = "app">
        <h1>BLACKJACK</h1>

        {error &&  (
            <p className = "error">
                {error}
            </p>
        )}

        {/* -------------------------- */}
        {/* START SESSION SCREEN */}
        {/* -------------------------- */}

        {!gameId && (
            <div className = "start-menu">
                <h2>Start Session</h2>

                <label>
                    Starting Balance:
                    <input
                        type = "number"
                        value = {balance}
                        onChange = {(event) => 
                            setBalance(Number(event.target.value))
                        }
                    />
                    <button onClick = {handleStartSession}>
                        Start Session
                    </button>
                </label>
            </div>
        )}

        {/* -------------------------- */}
        {/* GAME SCREEN */}
        {/* -------------------------- */}

        {gameId && (
            <div className = "table">
                {/* Home Button */}
                <button onClick = {handleHome}>
                    Home
                </button>

                {/* -------------------------- */}
                {/* If no hand is active */}
                {/* -------------------------- */}

                {!gameState && (
                    <div className = "deal-menu">
                        <h2>Place your bet</h2>
                        <label>
                            Bet:
                            <input
                                type = "number"
                                value = {bet}
                                onChange = {(event) => setBet(Number(event.target.value))}
                            />
                        </label>

                        <button onClick = {handleDeal}>
                            Deal
                        </button>
                    </div>
                )}




                {/* -------------------------- */}
                {/* ACTIVE / COMPLETED GAME */}
                {/* -------------------------- */}
                {gameState && (
                    <>
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
                                <div className = "player-hands">
                                {gameState.player.hands.map(
                                    (hand, index) => (
                                        <Hand
                                            key = {index}
                                            hand = {hand}
                                            index = {index}
                                            isActive = {gameState.game_state === "active" && index === activeHandIndex}
                                        />
                                    )
                                )}
                                </div>
                        </section>
                        
                        {/* Hit / Stand */}
                        <GameControls
                            onHit = {handleHit}
                            onStand = {handleStand}
                            onDouble = {handleDouble}
                            onSplit = {handleSplit}
                            disabled = {gameState.game_state !== "active"}
                            activeHand = {activeHand}
                        />
                        
                        {/* Deal another hand */}
                        {gameState.game_state !== "active" && (
                            <div className = "next_hand">
                                <label>
                                    Bet:
                                    <input
                                        type = "number"
                                        value = {bet}
                                        onChange = {(event) => 
                                            setBet(Number(event.target.value))
                                        }
                                    />
                                </label>
                                
                                <button onClick = {handleDeal}>
                                    Deal
                                </button>      
                            </div>
                        )}
                    </>
                )}
                {gameState?.game_state === "insurance" && (
                    <InsurancePopup
                        onChoice = {handleInsuranceChoice}
                    />
                )}

            </div>
        )}
    </div>
  )
}
export default App
