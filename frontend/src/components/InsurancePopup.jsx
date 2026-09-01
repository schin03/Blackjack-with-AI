function InsurancePopup({ onChoice }) {
    return (
        <div className = "insurance-overlay">
            <div className = "insurance-popup">
                <h2>Insurance?</h2>
                <p>The dealer is showing an Ace</p>
                <p>Would you like to take insurance?</p>

                <div className = "insurance-buttons">
                    <button onClick = {() => onChoice(true)}>
                        YES
                    </button>
                    <button onClick = {() => onChoice(false)}>
                        NO
                    </button>

                </div>
            </div>
        </div>
    )
}

export default InsurancePopup