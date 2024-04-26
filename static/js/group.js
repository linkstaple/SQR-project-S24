async function split(group, amount, lander, payers) {
    return fetch('/api/split', {
        method: 'POST',
        body: JSON.stringify({
            group,
            amount,
            lander,
            payers
        })
    })
}
