document.getElementById('runSimulation').addEventListener('click', async () => {
    const response = await fetch('/run-simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ max_iters: 20 }),
    });
    const data = await response.json();
    document.getElementById('output').innerText = data.dialogue;
});