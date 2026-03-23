import httpx
import os
from app.models import SummonerProfile, RankedInfo, MatchSummary
from typing import List

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

BASE_URL = "https://euw1.api.riotgames.com"
REGIONAL_URL = "https://europe.api.riotgames.com"

async def get_account_by_riot_id(game_name: str, tag_line: str) -> dict:
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def get_summoner_by_puuid(puuid: str) -> SummonerProfile:
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return SummonerProfile(
            puuid=data["puuid"],
            level=data["summonerLevel"],
            profile_icon_id=data["profileIconId"]
        )

async def get_ranked_info(puuid: str) -> List[RankedInfo]:
    url = f"{BASE_URL}/lol/league/v4/entries/by-puuid/{puuid}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return [
            RankedInfo(
                queue_type=entry["queueType"],
                tier=entry["tier"],
                rank=entry["rank"],
                league_points=entry["leaguePoints"],
                wins=entry["wins"],
                losses=entry["losses"]
            )
            for entry in data
        ]

async def get_recent_matches(puuid: str, count: int = 15) -> List[MatchSummary]:
    url = f"{REGIONAL_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        match_ids = response.json()

        matches = []
        for match_id in match_ids:
            match_url = f"{REGIONAL_URL}/lol/match/v5/matches/{match_id}"
            match_response = await client.get(match_url, headers=HEADERS)
            match_response.raise_for_status()
            match_data = match_response.json()

            # Find this player's data in the match
            participant = next(
                p for p in match_data["info"]["participants"]
                if p["puuid"] == puuid
            )
            matches.append(MatchSummary(
                match_id=match_id,
                champion=participant["championName"],
                kills=participant["kills"],
                deaths=participant["deaths"],
                assists=participant["assists"],
                win=participant["win"],
                game_duration_minutes=round(match_data["info"]["gameDuration"] / 60),
                game_mode=match_data["info"]["gameMode"]
            ))
        return matches