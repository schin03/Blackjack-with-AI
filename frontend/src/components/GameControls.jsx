function GameControls({
    onHit,
    onStand,
    onDouble,
    onSplit,
    disabled,
    activeHand
}) {
    return (
        <div className = "controls">
            <button
                onClick = {onSplit}
                disabled = {disabled || !activeHand?.can_split}
            >
                Split
            </button>
            
            <button
                onClick = {onHit}
                disabled = {disabled}
            >
                Hit
            </button>

            <button
                onClick = {onStand}
                disabled = {disabled}
            >
                Stand
            </button>
            <button
                onClick = {onDouble}
                disabled = {disabled || !activeHand?.can_double}
            >
                Double
            </button>
        </div>
    );
}

export default GameControls;