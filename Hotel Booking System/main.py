import pandas
from sqlalchemy.cyextension.processors import to_str


class Hotel:
    def __init__(self, hotel_id: int):
        self.hotelId: int = hotel_id
        self.name = dataframe.loc[dataframe["id"] == self.hotelId, "name"].squeeze()
        pass

    def book(self):
        """Book a hotel by changing its availability to no"""
        dataframe.loc[dataframe["id"] == self.hotelId, "available"] = "no"
        dataframe.to_csv("hotels.csv", index=False)
        pass

    def view_hotels(self):
        pass

    def available(self) -> bool:
        """
        Checks if the hotel is available
        :return Bool
        """
        availability = dataframe.loc[dataframe["id"] == self.hotelId, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customerName: str, hotelObject: Hotel):
        self.customerName: str = customerName
        self.hotel: Hotel = hotelObject

    def generate(self) -> str:
        """Generate a reservation for the user ticket holder"""
        content = f"""
        Thank you for your reservation!
        Here are your booking data
        Name: {self.customerName}
        Hotel Name: {self.hotel.name}
        """
        return content


if __name__ == "__main__":
    dataframe = pandas.read_csv("hotels.csv")
    print(dataframe)
    id = int(input("Enter id: "))
    hotel = Hotel(id)

    if hotel.available():
        hotel.book()
        name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(name, hotel)
        print(reservation_ticket.generate())
    else:
        print("Hotel is not free")
