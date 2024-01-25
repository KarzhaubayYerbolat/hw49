class ReturnTitleStrMixin:
    title = None

    def __str__(self):
        return self.title
