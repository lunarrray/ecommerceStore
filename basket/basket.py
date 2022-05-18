from store.models import Product
from decimal import Decimal
from store.models import Category

class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    # def add(self, product, qty):
    #     product_id = str(product.id)
    #
    #     if product_id in self.basket:
    #         self.basket[product_id]['qty'] = qty
    #     else:
    #         self.basket[product_id] = {'price': str(product.price), 'qty': qty}
    #
    #     self.session.modified = True

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        categoryID = product.category.id
        wishList = self.session.get('wishList')
        if 'wishList' not in self.session:
            wishList = self.session['wishList'] = []
        wishList.append(categoryID)
        self.session['wishList'] = wishList
        self.session.modified = True



    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]

        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        qty = qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.session.modified = True

    def clear(self):
        del self.session['skey']
        self.session.modified = True

    def declareWishList(self):
        wishList = self.session.get('wishList')
        if 'wishList' not in self.session:
            wishList = self.session['wishList'] = []
        if len(wishList) != 0:
            allCategories = Category.objects.all()
            countAll = []
            for categoryFromModel in allCategories:
                sum = 0
                for wish in wishList:
                    if wish == categoryFromModel.id:
                        sum += 1
                countAll.append(sum)
            max = countAll[0]
            index = 0
            for sum in countAll:
                if sum > max:
                    max = sum
                    index = countAll.index(max)
            return allCategories[index]
        return -1
