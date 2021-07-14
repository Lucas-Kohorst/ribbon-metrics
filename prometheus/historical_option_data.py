import random
import json
import requests
import datetime, time
from python_graphql_client import GraphqlClient
import asyncio
import mysql.connector

class OptionData:
    def totalVolume():
        dataBase = mysql.connector.connect(
            host ="localhost",  
            user ="ribbon",
            passwd ="password"
        )

        client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/kenchangh/ribbon-finance")

        # Create the query string and variables required for the request.
        query = """
            {
                vaultOptionTrades {
                    timestamp
                    buyer
                    txhash
                    sellAmount
                    premium
                    optionToken
                    vault {
                        name
                    }
                }
            }
        """

        sql = "INSERT INTO ribbon.options (timestamp, buyer, txhash, optionToken, premium, name, sellAmount) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        data = asyncio.run(client.execute_async(query=query))
        for option in data["data"]["vaultOptionTrades"]:
            timestamp = datetime.datetime.fromtimestamp(int(option["timestamp"])).strftime('%Y-%m-%d')    
            buyer = option["buyer"]
            txhash = option["txhash"]
            optionToken = option["optionToken"]
            name = option["vault"]["name"]
            option["timestamp"]
            premium = float(option["premium"]) / 10e18
            sellAmount = float(option["sellAmount"])

            val = (timestamp, buyer, txhash, optionToken, premium, name, sellAmount)
            dataBase.cursor().execute(sql, val)
            dataBase.commit()

            print(dataBase.cursor().rowcount, "details inserted")

        # disconnecting from server
        dataBase.close()


if __name__ == '__main__':
    OptionData.totalVolume()