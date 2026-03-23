from pydantic import BaseModel
from typing import Optional, List

class SummonerProfile(BaseModel):
    puuid: str
    level: int
    profile_icon_id: int

class RankedInfo(BaseModel):
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int

    @property
    def win_rate(self) -> float:
        total = self.wins + self.losses
        return round((self.wins / total) * 100, 1) if total > 0 else 0.0

class MatchSummary(BaseModel):
    match_id: str
    champion: str
    kills: int
    deaths: int
    assists: int
    win: bool
    game_duration_minutes: int
    game_mode: str