# encoding: utf-8

from fastapi import Path, HTTPException
from pydantic import BaseModel

from server import app, pugdagd_client


class BalanceResponse(BaseModel):
    address: str = "pugdag:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00"
    balance: int = 38240000000


@app.get("/addresses/{pugdagAddress}/balance", response_model=BalanceResponse, tags=["Pugdag addresses"])
async def get_balance_from_pugdag_address(
        pugdagAddress: str = Path(
            description="Pugdag address as string e.g. pugdag:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00",
            regex="^pugdag\:[a-z0-9]{61,63}$")):
    """
    Get balance for a given pugdag address
    """
    resp = await pugdagd_client.request("getBalanceByAddressRequest",
                                       params={
                                           "address": pugdagAddress
                                       })

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if "getUtxosByAddressesResponse" in resp and "error" in resp["getUtxosByAddressesResponse"]:
            raise HTTPException(status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"])
        else:
            raise

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {
        "address": pugdagAddress,
        "balance": balance
    }
