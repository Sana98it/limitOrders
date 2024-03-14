from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class Order:
    def __init__(self, buy_sell_flag, product_id, amount, limit_price):
        self.buy_sell_flag = buy_sell_flag
        self.product_id = product_id
        self.amount = amount
        self.limit_price = limit_price


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy_sell_flag: str, product_id: str, amount: int, limit_price: float):
        order = Order(buy_sell_flag, product_id, amount, limit_price)
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        for order in self.orders[:]:
            if order.product_id == product_id and ((order.buy_sell_flag == "buy" and price <= order.limit_price) or
                                                    (order.buy_sell_flag == "sell" and price >= order.limit_price)):
                try:
                    if order.buy_sell_flag == "buy":
                        self.execution_client.buy(product_id, order.amount)
                    else:
                        self.execution_client.sell(product_id, order.amount)
                    self.orders.remove(order)
                except ExecutionException as e:
                    print(f"Execution failed for {order.buy_sell_flag} order: {e}")
