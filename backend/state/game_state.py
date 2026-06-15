from dataclasses import dataclass, field

@dataclass
class GameState:
    roads: dict[int, int]        # edge_id -> player_id
    buildings: dict[int, int]    # vertex_id -> player_id

    cities: dict[int, int]       # vertex_id -> player_id

    robber_hex: int

    current_player: int

    dice: tuple[int, int] = (0, 0)