import Card from "./Card";

function Hand({ hand, index, isActive }) {
    return (
        <div className= {`hand ${isActive ? "active-hand" : ""}`}>
            <p className="hand-label">
                Hand {index + 1}{isActive ? " -- playing " : ""}
            </p>
            <div className="cards">
                {hand.cards.map((card, index) => {
                    return (
                        <Card
                            key={index}
                            card={card}
                        />
                    );
                })}
            </div>

            <p>Value: {hand.value}({hand.state})</p>
        </div>
    );
}

export default Hand;