

# from __future__ import annotations
# from typing import TYPE_CHECKING
 
# from shared.enums import Resource, DevCard
 
# if TYPE_CHECKING:
#     from engine.game import Game
 
 
# class Dispatcher:
#     """
#     Receives a raw action dict (from network or UI) and routes it to the correct Game method.
#     All input arrives as JSON-decoded dicts. All errors are caught and returned as error responses.
#     """
 
#     def __init__(self, game: Game):
#         self._game = game
 
#         self._handlers = {
#             "place_settlement": self._place_settlement,
#             "place_city":       self._place_city,
#             "place_road":       self._place_road,
#             "roll_dice":        self._roll_dice,
#             "move_robber":      self._move_robber,
#             "buy_dev_card":     self._buy_dev_card,
#             "play_knight":      self._play_knight,
#             "play_road_building":   self._play_road_building,
#             "play_year_of_plenty":  self._play_year_of_plenty,
#             "play_monopoly":    self._play_monopoly,
#             "end_turn":         self._end_turn,
#         }
 
#     def dispatch(self, message: dict) -> dict:
#         action = message.get("action")
 
#         if action not in self._handlers:
#             return _error(f"Unknown action: '{action}'")
 
#         try:
#             return self._handlers[action](message)
#         except (ValueError, KeyError, TypeError) as e:
#             return _error(str(e))
 
#     # ── Handlers ──────────────────────────────────────────────────────────────
 
#     def _place_settlement(self, msg: dict) -> dict:
#         self._game.place_settlement(
#             player_id=msg["player_id"],
#             vertex_id=msg["vertex_id"],
#         )
#         return _ok()
 
#     def _place_city(self, msg: dict) -> dict:
#         self._game.place_city(
#             player_id=msg["player_id"],
#             vertex_id=msg["vertex_id"],
#         )
#         return _ok()
 
#     def _place_road(self, msg: dict) -> dict:
#         self._game.place_road(
#             player_id=msg["player_id"],
#             edge_id=msg["edge_id"],
#         )
#         return _ok()
 
#     def _roll_dice(self, msg: dict) -> dict:
#         die1, die2 = self._game.roll_dice(player_id=msg["player_id"])
#         return _ok({"die1": die1, "die2": die2, "total": die1 + die2})
 
#     def _move_robber(self, msg: dict) -> dict:
#         self._game.move_robber(
#             player_id=msg["player_id"],
#             hex_id=msg["hex_id"],
#             victim_id=msg.get("victim_id"),  # optional
#         )
#         return _ok()
 
#     def _buy_dev_card(self, msg: dict) -> dict:
#         self._game.buy_dev_card(player_id=msg["player_id"])
#         return _ok()
 
#     def _play_knight(self, msg: dict) -> dict:
#         self._game.play_knight(
#             player_id=msg["player_id"],
#             hex_id=msg["hex_id"],
#             victim_id=msg.get("victim_id"),
#         )
#         return _ok()
 
#     def _play_road_building(self, msg: dict) -> dict:
#         self._game.play_road_building(
#             player_id=msg["player_id"],
#             edge_id_1=msg["edge_id_1"],
#             edge_id_2=msg.get("edge_id_2"),  # optional — may have only one valid edge
#         )
#         return _ok()
 
#     def _play_year_of_plenty(self, msg: dict) -> dict:
#         self._game.play_year_of_plenty(
#             player_id=msg["player_id"],
#             resource_1=Resource(msg["resource_1"]),
#             resource_2=Resource(msg["resource_2"]),
#         )
#         return _ok()
 
#     def _play_monopoly(self, msg: dict) -> dict:
#         self._game.play_monopoly(
#             player_id=msg["player_id"],
#             resource=Resource(msg["resource"]),
#         )
#         return _ok()
 
#     def _end_turn(self, msg: dict) -> dict:
#         self._game.end_turn(player_id=msg["player_id"])
#         return _ok()
 
 
# # ── Response helpers ──────────────────────────────────────────────────────────
 
# def _ok(data: dict | None = None) -> dict:
#     response = {"status": "ok"}
#     if data:
#         response.update(data)
#     return response
 
# def _error(message: str) -> dict:
#     return {"status": "error", "message": message}