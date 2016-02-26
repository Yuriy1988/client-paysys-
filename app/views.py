from app import app
from flask import render_template, request
from app.forms import UserPaymentForm


class Shop:
    """
    Fake Shop model.
    """
    def __init__(self, id, name, logo):
        self.id = id
        self.name = name
        self. logo = logo

# DataBase:
shop1 = Shop("1", "Shop1", "pass_to_image1")
shop2 = Shop("2", "Shop2", "pass_to_image2")
shop3 = Shop("3", "Shop3", "pass_to_image3")
shops = [shop1, shop2, shop3]


@app.route('/')
def home():
    """
    Homepage with a shops list.
    """
    # TODO: Getting the list of all Shop objects.
    return render_template('home.html', shops=shops)


@app.route('/form/<shop_id>', methods=["GET", "POST"])
def user_payment_form(shop_id):
    """
    Form shows after the shop picking.
    """
    # TODO: faking the getting a Shop object by ID:
    for i in shops:
        if shop_id == i.id:
            shop = i

    form = UserPaymentForm()

    # Showing the form to user:
    if request.method == 'GET':
        return render_template('user_payment_form.html', form=form, shop=shop)

    # If form submited by user:
    elif request.method == 'POST':
        message = "We took your transaction to processing. Thx for your choice. We love you!"
        return render_template('thank_you.html', message=message, shop=shop)
