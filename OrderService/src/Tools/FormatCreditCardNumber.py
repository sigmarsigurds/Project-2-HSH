class FormatCreditCardNumber:
    @staticmethod
    def format(card_number: str) -> str:
        """Format the credit card to have * and only show the last 4 digits"""
        return f"{'*' * (len(card_number) - 4)}{card_number[:4]}"
