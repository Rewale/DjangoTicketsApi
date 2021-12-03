class TicketCustomerWOEscort(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message is None:
            return 'Пассажиру менее 16 лет, необходим сопровождающий'
        else:
            return self.message


class TicketEscortException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message is None:
            return 'Сопроводителю менее 16 лет, необходим другой сопровождающий'
        else:
            return self.message
