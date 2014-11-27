from django.core.exceptions import ImproperlyConfigured
from products.models import Product, Color, Size

class CartItem(object):
    def __init__(self, item, quantity=1, color=None, size=None):
        self.item = item
        self.quantity = quantity
        self.color = color
        self.size = size

    def __repr__(self):
        if self.size:
            name = "CartItem(%r, %r, size - %r)" % (self.item,
                                                   self.quantity,
                                                   self.size)
        elif self.color:
            name = "CartItem(%r, %r, color - %r)" % (self.item,
                                                    self.quantity,
                                                    self.color)
        if self.color and self.size:
            name = "CartItem(%r, %r, color - %r, size- %r)" % (self.item,
                                                              self.quantity,
                                                              self.color,
                                                              self.size)
        if not self.color and not self.size:
            name = "CartItem(%r, %r)" % (self.item, self.quantity)

        return name


class Cart(list):
    model = None
    def __init__(self, request, name="cart"):
        super(Cart, self).__init__()
        self.request = request
        self.name = name
        if self.model is None:
            from django.conf import settings
            try:
                self.model = Product
            except AttributeError:
                raise ImproperlyConfigured("%s isn't a valid Cart model." % settings.CART_MODEL)
        for item, quantity, color, size in request.session.get(self.name, []):
            try:
                self.append(item, quantity, color, size)
            except self.model.DoesNotExist:
                pass

    def save(self):
        self.request.cart = self
        self.request.session[self.name] = tuple(
            (i.item.pk, i.quantity, i.color, i.size)
            for i in self
        )

    def _get(self, item):
        '''Ensure item is an instance of self.model'''
        if not isinstance(item, self.model):
            return self.model._default_manager.get(pk=item)
        return item

    def append(self, item, quantity=1, color=None, size=None):
        item = self._get(item)
        try:
            self[self.index(item)].quantity += quantity
        except ValueError:
            super(Cart, self).append(CartItem(item, quantity, color, size))

    def change_color(self, item, color):
        item = self._get(item)
        self[self.index(item)].color = int(color)

    def change_size(self, item, size):
        item = self._get(item)
        self[self.index(item)].size = int(size)

    def index(self, value, **kwargs):
        '''Prevent duplication of (item, quantity) pairs.'''
        if isinstance(value, self.model):
            for i in self:
                if i.item == value:
                    return self.index(i)
        return super(Cart, self).index(value, **kwargs)

    def decrease(self, item, quantity=1):
        item = self._get(item)
        try:
            self[self.index(item)].quantity -= quantity
        except ValueError:
            super(Cart, self).append(CartItem(item, quantity))

    def remove(self, item):
        super(Cart, self).remove(self[self.index(self._get(item))])

    def empty(self):
        '''Remove all items from cart'''
        while len(self):
            self.pop()

    def __repr__( self ):
        return ','.join([repr(x) for x in self])

    @property
    def items(self):
        return [line.item for line in self]

    @property
    def color(self):
        return [Color.objects.get(pk=line.color) for line in self]

    @property
    def size(self):
        return [Size.objects.get(pk=line.size) for line in self]

    @property
    def items_total(self):
        return len(self)

    @property
    def total_quantity(self):
        return reduce(lambda res, x: res+x, [i.quantity for i in self])

    @property
    def total_price(self):
        if not self:
            return 0
        else:
            return reduce(lambda x, y: x+y, [i.item.total_price() * i.quantity for i in self])
