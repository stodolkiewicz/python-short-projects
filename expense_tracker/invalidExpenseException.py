class InvalidExpenseException(Exception):
    def __init__(self):
        super().__init__("Amount must be greater than 0")