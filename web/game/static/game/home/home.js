 function getCsrfToken(){
    return document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')[1];
 }

 
 const csrfToken = getCsrfToken();
 const status = document.getElementById('status');


  async function loadLobbies() {
    try {
      const res = await fetch('/game/lobbies/');
      const data = await res.json();
      renderLobbies(data.lobbies);
    } catch (err) {
      status.textContent = 'Could not load lobbies.';
    }
  }

  function renderLobbies(lobbies) {
    const list = document.getElementById('lobby-list');
    const empty = document.getElementById('empty-msg');

    if (!lobbies || lobbies.length === 0) {
      list.innerHTML = '<div class="lobby-empty">No open lobbies</div>';
      return;
    }

    empty && empty.remove();
    list.innerHTML = lobbies.map(lobby => `
      <div class="lobby-item">
        <div class="lobby-info">
          <div class="lobby-id">Game #${lobby.id}</div>
          <div class="lobby-players">${lobby.players_joined} / ${lobby.max_players} players</div>
        </div>
        <button class="btn-join" onclick="joinLobby(${lobby.id})">Join</button>
      </div>
    `).join('');
  }

  async function createLobby(maxPlayers) {
    status.textContent = 'Creating lobby…';
    try {
      const res = await fetch('/game/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ max_players: maxPlayers })
      });
      const data = await res.json();
      status.textContent = '';
      // store token and redirect to waiting room
      localStorage.setItem('token', data.player_token);
      localStorage.setItem('lobby_id', data.new_lobby_id);
      window.location.href = `/game/lobby/${data.new_lobby_id}/`;
    } catch (err) {
      status.textContent = 'Failed to create lobby.';
    }
  }

  async function joinLobby(lobbyId) {
    status.textContent = 'Joining…';
    try {
      const res = await fetch('/game/join/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
         },
        body: JSON.stringify({ lobby_id: lobbyId })
      });
      const data = await res.json();
      status.textContent = '';
      localStorage.setItem('token', data.player_token);
      localStorage.setItem('lobby_id', lobbyId);
      window.location.href = `/game/lobby/${lobbyId}/`;
    } catch (err) {
      status.textContent = 'Failed to join lobby.';
    }
  }

  // poll for lobby updates every 3 seconds
  loadLobbies();
  setInterval(loadLobbies, 3000);