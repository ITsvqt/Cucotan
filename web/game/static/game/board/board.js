const status = document.getElementById('status');
const SIZE = 44;
const SQRT3 = Math.sqrt(3);
const lobbyId = localStorage.getItem('lobby_id');


function hexToPixel(q, r) {
    const x = SIZE * (SQRT3 * q + SQRT3 / 2 * r);
    const y = SIZE * (3 / 2 * r);
    return { x, y };
}

function hexCorners(cx, cy, size) {
    const pts = [];
    for (let i = 0; i < 6; i++) {
        const angle = Math.PI / 180 * (60 * i - 30);
        pts.push([cx + size * Math.cos(angle), cy + size * Math.sin(angle)]);
    }
    return pts.map(p => p.join(",")).join(" ");
}

function renderBoard(data) {
    const svg = document.getElementById("board");
    svg.innerHTML = "";

    data.hexes.forEach(hex => {
        const { x, y } = hexToPixel(hex.q, hex.r);
        const isSea = hex.terrain === "Sea";
        const isDesert = hex.terrain === "Desert";
        const isHot = hex.number === 6 || hex.number === 8;

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");

        const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        poly.setAttribute("points", hexCorners(x, y, SIZE - 1));
        poly.setAttribute("class", isSea ? "hex-sea" : `hex-land terrain-${hex.terrain}`);
        g.appendChild(poly);

        if (!isSea) {
            if (hex.number !== null) {
                const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                circle.setAttribute("cx", x);
                circle.setAttribute("cy", y);
                circle.setAttribute("r", 14);
                circle.setAttribute("class", isHot ? "hex-number-circle hot" : "hex-number-circle");
                g.appendChild(circle);

                const num = document.createElementNS("http://www.w3.org/2000/svg", "text");
                num.setAttribute("x", x);
                num.setAttribute("y", y);
                num.setAttribute("class", isHot ? "hex-number hot" : "hex-number");
                num.textContent = hex.number;
                g.appendChild(num);
            } else if (isDesert) {
                const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
                lbl.setAttribute("x", x);
                lbl.setAttribute("y", y);
                lbl.setAttribute("class", "hex-label");
                lbl.textContent = "Desert";
                g.appendChild(lbl);
            }
        }

        svg.appendChild(g);
    });
}


async function loadBoard() {
    try {
        const res = await fetch(`/game/board-data/${lobbyId}/`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        status.textContent = '';
        renderBoard(data);
    } catch (err) {
        status.textContent = `Error: ${err.message}`;
    }
}

loadBoard();