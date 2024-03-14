import unittest
from unittest.mock import Mock
from limit_order_agent import LimitOrderAgent


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.mock_execution_client = Mock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_order_execution(self):
        self.agent.add_order("buy", "IBM", 1000, 100)
        self.agent.on_price_tick("IBM", 99)
        self.mock_execution_client.buy.assert_called_once_with("IBM", 1000)

    def test_sell_order_execution(self):
        self.agent.add_order("sell", "AAPL", 500, 150)
        self.agent.on_price_tick("AAPL", 151)
        self.mock_execution_client.sell.assert_called_once_with("AAPL", 500)

    def test_order_not_executed_if_price_not_met(self):
        self.agent.add_order("buy", "GOOG", 200, 1200)
        self.agent.on_price_tick("GOOG", 1201)
        self.mock_execution_client.buy.assert_not_called()

        self.agent.add_order("sell", "MSFT", 300, 200)
        self.agent.on_price_tick("MSFT", 199)
        self.mock_execution_client.sell.assert_not_called()


if __name__ == '__main__':
    unittest.main()