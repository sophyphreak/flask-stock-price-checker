from db import db


class StockModel(db.Model):
    __tablename__ = "stock"
    _id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80))
    likes = db.Column(db.Integer)

    def __init__(self, symbol):
        self.symbol = symbol
        self.likes = 0

    def addLike(self):
        self.likes += 1

    def json(self):
        return {
            "_id": self._id,
            "symbol": self.symbol,
            "likes": self.likes
        }

    @classmethod
    def find_by_symbol(cls, symbol):
        return cls.query.filter_by(symbol=symbol).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
