function LandingPage() {
    return (
        <div>
            <h1>Enter the fields</h1>
            <label htmlFor="number-of-testcases">Enter number of testcases</label>
            <input type="number" id="number-of-testcases" name="number-of-testcases" required /> <br />
            <label htmlFor="testcases-details">Testcases Details</label>
            <textarea id="testcases-details" name="testcases-details" required /> <br />
            <button type="submit">Generate Test Cases</button>
        </div>
    )
}

export default LandingPage;