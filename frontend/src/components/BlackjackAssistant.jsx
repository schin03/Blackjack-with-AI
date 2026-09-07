import { useState } from "react";

function BlackjackAssistant({
    canHelp, onHelp, advice, error, isLoading
}) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <aside className = "blackjack-assistant" aria-label = "Blackjack assistant">
            {isOpen && (
                <div className = "assistant-panel" role = "dialog" aria-label = "Blackjack help">
                    <div className = "assistant-header">
                        <div>
                            <p className = "assistant-kicker">
                                BLACKJACK ASSISTANT
                            </p>
                            <h2>Need a hand?</h2>
                        </div>

                        <button
                            className = "assistant-close"
                            onClick = {() => setIsOpen(false)}
                            aria-label = "Close assistant">
                                x
                        </button>
                    </div>
                    <p className = "assistant-copy">
                        I'll suggest a legal move for your current hand and explain why you should do it.
                    </p>
                    <button
                        className = "help-hand-button"
                        onClick = {onHelp}
                        disabled = {!canHelp || isLoading}>
                            {isLoading ? "Thinking..." : "Help this hand"}
                    </button>

                    {!canHelp && (
                        <p className = "assistant-status">
                            Deal a hand before asking for advice.
                        </p>
                    )}

                    {error && <p clasName = "assistant-error">{error}</p>}

                    {advice && (
                        <div className = "assistant-answer" aria-live = "polite">
                            <p className = "assistant-move">{advice.move}</p>
                            <p>{advice.explanation}</p>
                        </div>
                    )}
                <button
                    className = "assistant-fab"
                    onClick = {() => setIsOpen((open) => !open)}
                    aria-expanded = {isOpen}>
                    ♠ Help
                </button>
                </div>
            )}
        </aside>
    );
}

export default BlackjackAssistant;