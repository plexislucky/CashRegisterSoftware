from tkinter import *
from tkinter import messagebox
import time

NUMBER_FIELD_CONTENT: str = ""
ITEM_LIST_TEXTBOX_CONTENT: str = ""
ITEM_PRICES: list[float] = list()
# ------ CUSTOM WIDGETS START ------

class CustomButton:
    def __init__(self, x: int, y: int, width: int = 50, height: int = 50, **kwargs) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.kwargs: dict = kwargs

        if "command" in kwargs:
            self.command = kwargs["command"]

        if "fill" in kwargs:
            self.fill = kwargs["fill"]
        else:
            self.fill = "gray"

        canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, outline="black", fill=self.fill)

        if "text" in kwargs:
            canvas.create_text((self.x+(self.width/2), self.y+(self.height/2)), text=kwargs["text"], anchor=CENTER, fill="black", font=("Helvetica 12")) 
            

    def OnMouseRelease(self):
        if "command" in self.kwargs:
            return self.command()
    
# ------ CUSTOM WIDGETS END ------

def ClickHandler(event): # This method only gets called on LEFT click
    global buttons
    for button in buttons:
        if event.x >= button.x and event.y >= button.y and event.x <= button.x+button.width and event.y <= button.y+button.height:
            button.OnMouseRelease()

def RemoveFromInputField():
    global NUMBER_FIELD_CONTENT
    NUMBER_FIELD_CONTENT = NUMBER_FIELD_CONTENT[:-1]

    canvas.itemconfig(numberFieldText, text=NUMBER_FIELD_CONTENT)

def AddToInputField(value: str):
    global NUMBER_FIELD_CONTENT

    if "." in NUMBER_FIELD_CONTENT and len(NUMBER_FIELD_CONTENT.split(".")[1]) == 2: # No more than 2 decimal places
        return
    
    if value == "." and "." in NUMBER_FIELD_CONTENT: # No more than 1 period symbol
        return
    
    if len(NUMBER_FIELD_CONTENT) < 14: # Character limit: 14
        if len(NUMBER_FIELD_CONTENT) == 0 and (value == "." or value == "00"):
            NUMBER_FIELD_CONTENT += "0."
        else:
            NUMBER_FIELD_CONTENT += value

        canvas.itemconfig(numberFieldText, text=NUMBER_FIELD_CONTENT)


def AddItem():
    global NUMBER_FIELD_CONTENT, ITEM_PRICES, ITEM_LIST_TEXTBOX_CONTENT

    ITEM_PRICES.append(float(NUMBER_FIELD_CONTENT))
    NUMBER_FIELD_CONTENT = ""

    ITEM_LIST_TEXTBOX_CONTENT = ""

    for i in ITEM_PRICES:
        ITEM_LIST_TEXTBOX_CONTENT += "{:.2f}".format(i) + "\n"

    ITEM_LIST_TEXTBOX_CONTENT += "\nTotal: " + "{:.2f}".format(sum(ITEM_PRICES))

    canvas.itemconfig(totalItemListText, text=ITEM_LIST_TEXTBOX_CONTENT)
    canvas.itemconfig(numberFieldText, text="")

def DisplayTotal():
    global ITEM_PRICES
    canvas.itemconfig(numberFieldText, text="{:.2f}".format(sum(ITEM_PRICES)))

def CancelTransaction():
    global NUMBER_FIELD_CONTENT, ITEM_PRICES, ITEM_LIST_TEXTBOX_CONTENT
    NUMBER_FIELD_CONTENT = ""
    ITEM_PRICES.clear()
    ITEM_LIST_TEXTBOX_CONTENT = ""

    canvas.itemconfig(totalItemListText, text=ITEM_LIST_TEXTBOX_CONTENT)
    canvas.itemconfig(numberFieldText, text="")

def LogTransaction(itemPrices: list, cashGiven: float):
    # transactions.dat format: unixSeconds:ITEM_PRICES:cashGiven
    logData = str(int(time.time())) + ":" # no decimals allowed in my unix timestamp >:)
    
    for i in itemPrices:
        logData += str(i) + ","

    logData = logData[:-1]
    logData += f":{cashGiven}"
        
    with open("transactions.dat", "a") as transactionLog:
        transactionLog.write(logData)

def CashPayment():
    global NUMBER_FIELD_CONTENT, ITEM_PRICES

    try:
        finalCost: float = sum(ITEM_PRICES)
        cashGiven: float = float(NUMBER_FIELD_CONTENT)

        if cashGiven >= finalCost:
            NUMBER_FIELD_CONTENT = "Change: " + "{:.2f}".format(cashGiven - finalCost)
            canvas.itemconfig(numberFieldText, text=NUMBER_FIELD_CONTENT)
                
            LogTransaction(ITEM_PRICES, cashGiven)
        else:
            raise Exception("InsufficientFunds")
        
    except Exception as e:
        if str(e) == "InsufficientFunds":
            messagebox.showerror("Insufficient funds", "The payment is less than the cost of the items!")
        else:
            messagebox.showerror("An exception occurred", str(e))

            

# ------ TKINTER BOILERPLATE BULLSHIT BELOW ------

root = Tk()
root.title("Cash register software")
root.geometry("500x500")
root.resizable(False, False)

canvas = Canvas(root, width=500, height=500)
canvas.place(x=0, y=0)

numberFieldText = canvas.create_text(490, 0, text=NUMBER_FIELD_CONTENT, font=("Helvetica 22"), anchor=NE)
totalItemListText = canvas.create_text(260, 50, text=ITEM_LIST_TEXTBOX_CONTENT, font=("Helvetica 16"), anchor=NW)

buttons: list[CustomButton] = [
    CustomButton(0, 0, text="7", command=lambda: AddToInputField("7")),
    CustomButton(51, 0, text="8", command=lambda: AddToInputField("8")),
    CustomButton(102, 0, text="9", command=lambda: AddToInputField("9")),
    CustomButton(0, 51, text="4", command=lambda: AddToInputField("4")),
    CustomButton(51, 51, text="5", command=lambda: AddToInputField("5")),
    CustomButton(102, 51, text="6", command=lambda: AddToInputField("6")),
    CustomButton(0, 102, text="1", command=lambda: AddToInputField("1")),
    CustomButton(51, 102, text="2", command=lambda: AddToInputField("2")),
    CustomButton(102, 102, text="3", command=lambda: AddToInputField("3")),
    CustomButton(0, 153, text="0", command=lambda: AddToInputField("0")),
    CustomButton(51, 153, text="00", command=lambda: AddToInputField("00")),
    CustomButton(102, 153, text=".", command=lambda: AddToInputField(".")),
    CustomButton(0, 204, width=253, text="Cash payment", fill="lime", command=CashPayment),
    CustomButton(153, 102, width=100, text="Add", command=AddItem),
    CustomButton(153, 153, width=100, text="Total", command=DisplayTotal),
    CustomButton(153, 51, width=100, text="RESET", fill="red", command=CancelTransaction),
    CustomButton(153, 0, width=100, text="CLEAR", fill="red", command=RemoveFromInputField),
    
]

root.bind("<Button-1>", ClickHandler)
root.mainloop()
