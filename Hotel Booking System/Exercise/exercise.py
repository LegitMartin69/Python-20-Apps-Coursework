from fpdf import FPDF
from fpdf.enums import XPos, YPos
import pandas


# Load dataframe
dataframe = pandas.read_csv("articles.csv")


class Item:
    def __init__(self, id):
        self.id = id
        self.name = dataframe.loc[dataframe["id"] == self.id, "name"].squeeze()
        self.price = dataframe.loc[dataframe["id"] == self.id, "price"].squeeze()
        self.stock = dataframe.loc[dataframe["id"] == self.id, "in stock"].squeeze()


class Transaction:
    def __init__(self, item: Item):
        self.item_handled = item
        pass

    def reduce_amount(self, amount):
        """Reduces the amount of stock in the csv file"""

        dataframe.loc[dataframe["id"] == item_id, "in stock"] = self.item_handled.stock - amount
        dataframe.to_csv("articles.csv", index=False)
        print(f"Stock of {self.item_handled.name} went down by {amount} and is now "
              f"{dataframe.loc[dataframe["id"] == item_id, "in stock"].squeeze()}")
        pass


    def print_receipt(self):
        """Prints a pdf receipt, along with all the details"""

        # PDF Formating
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Receipt nr.1", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Article: {self.item_handled.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Price: {self.item_handled.price}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output("receipt.pdf")
        pass


if __name__ == "__main__":
    # Show the available goods
    print(dataframe)

    # Ask for item id
    item_id = int(input("Choose an article to buy (id): "))

    # Make an Item to sell
    item_to_sell = Item(dataframe.loc[dataframe["id"] == item_id, "id"].squeeze())
    # print(item_to_sell.id, item_to_sell.name, item_to_sell.price, item_to_sell.stock)

    # Initialize Transaction class
    transaction = Transaction(item_to_sell)

    # Reduce stock by 1
    transaction.reduce_amount(1)

    # Print a receipt
    transaction.print_receipt()


"""
NOTES
Print out the available items (csv file)
Prompt the user to input an id
Generate a receipt
Lower the "in stock" count
"""


