from numpy import hypot 


class BaseTest:
    # Price
    upfront_expense     = 0.5
    price_per_unit      = 1

    # Work
    steps               = 0.25
    portability         = 0.25
    dev_time            = 0.25
    result_time         = 0.25

    @classmethod
    def price(cls):
        return cls.upfront_expense + cls.price_per_unit

    @classmethod
    def work(cls):
        return cls.steps + cls.portability + cls.dev_time + cls.result_time

    @classmethod
    def cost(cls):
        return hypot(cls.price(), cls.work())



class LFT(BaseTest):
    price_per_unit      = 0.3

    steps               = 0.1
    portability         = 0.1
    dev_time            = 0.7
    result_time         = 0.1


class PCR(BaseTest):
    upfront_expense     = 0.8
    price_per_unit      = 0.5

    portability         = .6
    dev_time            = 0.2
    result_time         = 0.3
    steps               = 0.4


class Antibody(BaseTest):
    upfront_expense     = 0.9
    price_per_unit      = 0.9

    steps               = 0.7
    portability         = 1
    result_time         = 0.4


