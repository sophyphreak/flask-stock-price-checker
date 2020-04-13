from flask_restful import Resource, reqparse
import requests

from models.stock import StockModel


class Stock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("stock", action="append")
    parser.add_argument('like')

    def get(self):
        symbols = Stock.parser.parse_args()["stock"]
        like = Stock.parser.parse_args()['like']

        if len(symbols) > 1:
            return getTwoSymbols(symbols, like)
        return getOneSymbol(symbols[0], like)

def getTwoSymbols(symbols, like):
    symbolOne, symbolTwo, *other = symbols
    symbolOne = symbolOne.upper()
    symbolTwo = symbolTwo.upper()
    stockOne = StockModel.find_by_symbol(symbolOne)
    if not stockOne:
        stockOne = StockModel(symbol=symbolOne)
    stockTwo = StockModel.find_by_symbol(symbolTwo)
    if not stockTwo:
        stockTwo = StockModel(symbol=symbolTwo)
    if like and (like == 'true' or like == 'True' or like == True):
        stockOne.addLike()
        stockTwo.addLike()
    stockOne.save_to_db()
    stockTwo.save_to_db()
    priceOne = requests.get(f'https://repeated-alpaca.glitch.me/v1/stock/{symbolOne}/quote').json()['latestPrice']
    priceTwo = requests.get(f'https://repeated-alpaca.glitch.me/v1/stock/{symbolTwo}/quote').json()['latestPrice']
    return {"stockData": [{
        "stock": symbolOne,
        "price": priceOne,
        "rel_likes": stockOne.likes - stockTwo.likes
    }, {
        "stock": symbolTwo,
        "price": priceTwo,
        "rel_likes": stockTwo.likes - stockOne.likes
    }]}

def getOneSymbol(symbol, like):
    symbol = symbol.upper()
    stock = StockModel.find_by_symbol(symbol)
    if not stock:
        stock = StockModel(symbol=symbol)
    if like and (like == 'true' or like == 'True' or like == True):
        stock.addLike()
    stock.save_to_db()
    price = requests.get(f'https://repeated-alpaca.glitch.me/v1/stock/{symbol}/quote').json()['latestPrice']
    return {"stockData": {
        "stock": symbol,
        "price": price,
        "likes": stock.likes
    }}
