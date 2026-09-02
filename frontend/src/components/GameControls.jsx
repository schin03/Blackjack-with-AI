function GameControls({
    onHit,
    onStand,
    onDouble,
    disabled,
    handState
}) {
    return (
        <div className = "controls">
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
                disabled = {disabled || handState !== "active"}
            >
                Double
            </button>

        </div>
    );
}

export default GameControls;