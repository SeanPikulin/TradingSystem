from Backend.Domain.Payment.OutsideSystems.outside_cashing import OutsideCashing
from collections import defaultdict
from Backend.response import Response


class OutsideCashingStub(OutsideCashing):

    def __init__(self):
        self.faulty = False
        self.can_pay = defaultdict(lambda: True)
        self.balances = defaultdict(lambda: 0.0)

    def pay(self, price, payment_details):
        if self.faulty:
            return Response(False, msg="The Cashing system is currently not working")
        if not self.can_pay[payment_details]:
            return Response(False, msg="The client with those payment details cannot pay")
        self.balances[payment_details] += price
        return Response(True)

    def brake(self):
        self.faulty = True

    def fix(self):
        self.faulty = False
