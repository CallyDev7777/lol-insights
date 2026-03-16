from fastapi import FastAPI, HTTPException
from app import riot_client, cache
from app.models import SummonerProfile, RankedInfo, MatchSummary
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LoL Insights API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/summoner/{game_name}/{tag_line}")
async def get_summoner(game_name: str, tag_line: str, refresh: bool = False):
    cache_key = f"summoner:{game_name}:{tag_line}"

    if not refresh:
        cached = await cache.get_cached(cache_key)
        if cached:
            return cached

    try:
        account = await riot_client.get_account_by_riot_id(game_name, tag_line)
        puuid = account["puuid"]
        summoner = await riot_client.get_summoner_by_puuid(puuid)
        result = summoner.model_dump()
        await cache.set_cached(cache_key, result, ttl_seconds=300)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/summoner/{game_name}/{tag_line}/ranked")
async def get_ranked(game_name: str, tag_line: str, refresh: bool = False):
    cache_key = f"ranked:{game_name}:{tag_line}"

    if not refresh:
        cached = await cache.get_cached(cache_key)
        if cached:
            return cached

    try:
        account = await riot_client.get_account_by_riot_id(game_name, tag_line)
        puuid = account["puuid"]
        # Use puuid-based ranked endpoint instead
        ranked = await riot_client.get_ranked_info(puuid=puuid)
        result = [r.model_dump() for r in ranked]
        await cache.set_cached(cache_key, result, ttl_seconds=300)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summoner/{game_name}/{tag_line}/matches")
async def get_matches(game_name: str, tag_line: str, refresh: bool = False):
    cache_key = f"matches:{game_name}:{tag_line}"

    if not refresh:
        cached = await cache.get_cached(cache_key)
        if cached:
            return cached

    # Falls through to fresh API call if refresh=True or cache miss
    try:
        account = await riot_client.get_account_by_riot_id(game_name, tag_line)
        puuid = account["puuid"]
        matches = await riot_client.get_recent_matches(puuid)
        result = [m.model_dump() for m in matches]
        await cache.set_cached(cache_key, result, ttl_seconds=300)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))