from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# id  title  price  isActive  description
#  1  Some   200    True      Desc. about item1
#  2  Some2  50     True      Desc. about item2
#  3  Some3  2200   False     Desc. about item3
#  4  Some4  500    True      Desc. about item4


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Товар: {self.title}, Цена:{self.price}, Описание:{self.description}'


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('home.html', data=items)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        item = Item(
            title=title,
            price=price,
            description=description)

        db.session.add(item)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')


@app.route('/buy/<int:item_id>')
def item_buy(item_id):
    item = Item.query.get(item_id)

    api = Api(merchant_id='your_id_here',
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/album')
def album():
    return render_template('album.html')


if __name__ == '__main__':
    app.run()
