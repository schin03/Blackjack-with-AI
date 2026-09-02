function Card( {card} ) {
    return (
        <div className = "card">
            {card.hidden ? "?" : `${card.num}${card.icon}`}
        </div>
    );
}

export default Card;