const lobbyId = parseInt(window.location.pathname.split('/')[3]);
const token = localStorage.getItem('token');
const status = document.getElementById('status');
const csrfToken = document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')[1];


async function startGame() {
    const res = await fetch('/game/start/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ lobby_id: lobbyId })
    });
    if (res.ok) {
        window.location.href = '/game/board/';
    }
}

async function leaveLobby() {
    try {
        const res = await fetch('/game/leave/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ player_token: token })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.removeItem('token');
            localStorage.removeItem('lobby_id');
            window.location.href = '/game/';
        } else {
            status.textContent = data.error;
        }
    } catch (err) {
        status.textContent = 'Failed to leave lobby.';
    }
}