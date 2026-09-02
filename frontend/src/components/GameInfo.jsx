function GameInfo( {gameState} ) {
    if (!gameState) {
        return null;
    }

    return (
        <div className = "game-info">
            <p>
                Balance: ${gameState.player.current_bal}
            </p>

            <p>
                Bet: ${gameState.player.current_bet}
            </p>

            <p>
                Current State: {gameState.game_state}
            </p>

        </div>
    );
}

export default GameInfo;