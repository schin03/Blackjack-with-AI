import Card from "./Card";

function Hand({ hand }) {
    return (
        <div className="hand">
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

            <p>Value: {hand.value}</p>
        </div>
    );
}

export default Hand;