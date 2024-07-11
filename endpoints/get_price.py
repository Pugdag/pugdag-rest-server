# encoding: utf-8

from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from helper import get_pug_price, get_pug_market_data
from server import app


class PriceResponse(BaseModel):
    price: float = 0.025235


@app.get("/info/price", response_model=PriceResponse | str, tags=["Pugdag network info"])
async def get_price(stringOnly: bool = False):
    """
    Returns the current price for Pugdag in USD.
    """
    if stringOnly:
        return PlainTextResponse(content=str(await get_pug_price()))

    return {"price": await get_pug_price()}


@app.get("/info/market-data",
         tags=["Pugdag network info"],
         include_in_schema=False)
async def get_market_data():
    """
    Returns market data for pugdag.
    """
    return await get_pug_market_data()
