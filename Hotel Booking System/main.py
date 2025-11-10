from operator import truediv

import pandas

df_hotels = pandas.read_csv("hotels.csv")
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_secure = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    # Class variable
    watermark = "The Real Estate Company"
    def __init__(self, hotel_id: int):
        self.hotelId: int = hotel_id
        self.name = df_hotels.loc[df_hotels["id"] == self.hotelId, "name"].squeeze()
        pass

    def book(self):
        """Book a hotel by changing its availability to no"""
        df_hotels.loc[df_hotels["id"] == self.hotelId, "available"] = "no"
        df_hotels.to_csv("hotels.csv", index=False)
        pass

    def view_hotels(self):
        pass

    def available(self) -> bool:
        """
        Checks if the hotel is available
        :return Bool
        """
        availability = df_hotels.loc[df_hotels["id"] == self.hotelId, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    # Class method
    @classmethod
    def get_hotel_count(cls, data):
        return len(data)

    # Makes hotel1 == hotel2 return as true, otherwise it would be false
    def __eq__(self, other):
        if self.hotelId == other.hotelId:
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name: str, hotel_object: Hotel):
        self.customerName: str = customer_name
        self.hotel: Hotel = hotel_object

    def generate(self) -> str:
        """Generate a reservation for the user ticket holder"""
        content = f"""
        Thank you for your reservation!
        Here are your booking data
        Name: {self.customerName}
        Hotel Name: {self.hotel.name}
        """
        return content

    # Property
    @property
    def the_customer_name(self):
        name = self.customerName.strip()
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2


class CreditCard:
    def __init__(self, number):
        self.number = number
        pass

    def validate(self, expiration, holder, cvc):
        "Checks if the credit card credentials are correct"
        card_data = {"number": self.number, "expiration": expiration,
                       "holder": holder, "cvc": cvc}
        print(card_data)
        print(df_cards)
        if card_data in df_cards:
            return True
        else:
            return False

    def pay(self):
        pass


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        "Checks if the given password matches those in the database"
        password = df_cards_secure.loc[df_cards_secure["number"] == self.number, "password"]
        password = password.squeeze()
        print(password, type(password))
        if str(password) == given_password:
            return True
        else:
            return False


if __name__ == "__main__":
    print(df_hotels)
    input_id = int(input("Enter id: "))
    hotel = Hotel(input_id)

    if hotel.available():
        # Validate the credit card
        card_number = input("Enter your (fake) credit card number: ")
        credit_card = SecureCreditCard(card_number)
        if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):

            # Authenticate with password
            given_password = input("Input the password: ")
            if credit_card.authenticate(given_password):

                # Book the hotel for a certain name
                hotel.book()
                name = input("Enter your name: ")
                reservation_ticket = ReservationTicket(name, hotel)
                print(reservation_ticket.generate())
            else:
                print("Password authentification failed")
        else:
            print("Theres was error during credit card verification")
    else:
        print("Hotel is not free")
