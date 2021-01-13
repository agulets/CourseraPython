class Value:
    def __set__(self, obj, value):
        self.amount = value - value * obj.commission

    def __get__(self, obj, obj_type):
        return self.amount
