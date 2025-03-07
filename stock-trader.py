import threading
import random
import time


class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quanity = quantity
        self.price = price
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None


    def enqueue(self, order):
        if (not self.head):
            self.head = self.tail = order
        else:
            self.tail.next = order
            self.tail = order

    def dequeue(self):
        if (not self.head):
            return None
        order = self.head
        self.head = self.head.next
        if (not self.head):
            self.tail = None
        return order

    def empty(self):
        return (self.head is None)


class orderBook:
    def __init__(self):
        self.buy_head = None
        self.sell_head = None
        self.buy_queue = queue()
        self.sell_queue = queue()

    def addOrder(self, order_type, ticker, quantity, price):
        order = Order(order_type, ticker, quantity, price)
        if (order_type == "Buy"):
            self.buy_queue.

    def insertOrder(self, order):
        if (order.order_type = "Buy"):
            if ((not self.buy_head) or (self.buy_head.price < order.price)):
                order.next = self.buy_head
                self.buy_head = order
            
            else:
                curr = self.buy_head
                while (curr.next and (curr.next.price >= order.price)):
                    curr = curr.next
                order.next = curr.next
                curr.next = order
        else:
            if ((not self.sell_head) or (self.sell_head.price > order.price)):
                order.next = self.sell_head
                self.sell_head = order
            else:
                curr = self.sell_head
                while (curr.next and (curr.next.price <= order.price)):
                    curr = curr.next
                order.next = curr.next
                curr.next = order
    def matchOrder(self):
        return 0
            






def randomOrders(order_book):
    tickers = ["STK{}".format(i) for i in range(1024)]
#   print(len(tickers))
    while(True):
       order_type = random.choice(["Buy", "Sell"])
       ticker = random.choice(tickers)
       quantity = random.randint(1, 100)
       price = random.uniform(10, 500)
       order_book.addOrder(order_type, ticker, quantity, round(price, 2))
       time.sleep(random.uniform(0.1, 0.5))

if (__name__ == "__main__"):
#   print(0)
    order_book = orderBook()
    trading_thread = threading.Thread(target=randomOrders, args=(order_book,), daemon=True)
    trading_thread.start()
#   randomOrders(order_book)
