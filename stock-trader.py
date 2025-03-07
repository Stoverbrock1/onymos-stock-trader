import threading
import random
import time


class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
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
        self.buy_queue = Queue()
        self.sell_queue = Queue()

    def addOrder(self, order_type, ticker, quantity, price):
        order = Order(order_type, ticker, quantity, price)
        if (order_type == "Buy"):
            self.buy_queue.enqueue(order)
        else:
            self.sell_queue.enqueue(order)
        self.insertOrder(order)

    def insertOrder(self, order):
        if (order.order_type == "Buy"):
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
        while ((not self.buy_queue.empty()) and (not self.sell_queue.empty())):        
            buy_order = self.buy_head
            sell_order = self.sell_head

            if ((not buy_order) or (not sell_order)):
                return

            if (buy_order.price >= sell_order.price):
                match_qty = min(buy_order.quantity, sell_order.quantity)
                print(f"Match: {match_qty} shares of {buy_order.ticker} at ${sell_order.price}")
                buy_order.quantity -= match_qty
                sell_order.quantity -= match_qty

                if (buy_order.quantity == 0):
                    self.buy_head = buy_order.next
                if (sell_order.quantity == 0):
                    self.sell_head = sell_order.next

            else:
                break



def randomOrders(order_book):
    tickers = ["STK{}".format(i) for i in range(1024)]
    while(True):
       order_type = random.choice(["Buy", "Sell"])
       ticker = random.choice(tickers)
       quantity = random.randint(1, 100)
       price = random.uniform(10, 500)
       order_book.addOrder(order_type, ticker, quantity, round(price, 2))
       time.sleep(random.uniform(0.1, 0.5))



if (__name__ == "__main__"):
    order_book = orderBook()
    trading_thread = threading.Thread(target=randomOrders, args=(order_book,), daemon=True)
    trading_thread.start()
    while (True):
        order_book.matchOrder()
        time.sleep(1)
