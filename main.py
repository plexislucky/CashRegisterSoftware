from tkinter import *

NUMBER_FIELD_CONTENT: str = ""
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
        if len(NUMBER_FIELD_CONTENT) == 0 and value == ".": # Add 0 before decimal if decimal is first input
            NUMBER_FIELD_CONTENT += "0."
        else:
            NUMBER_FIELD_CONTENT += value

        canvas.itemconfig(numberFieldText, text=NUMBER_FIELD_CONTENT)




# ------ TKINTER BOILERPLATE BULLSHIT BELOW ------

root = Tk()
root.title("v2")
root.geometry("500x500")
root.resizable(False, False) # please excuse my dope ass swag

canvas = Canvas(root, width=500, height=500)
canvas.place(x=0, y=0)

numberFieldText = canvas.create_text(490, 0, text=NUMBER_FIELD_CONTENT, font=("Helvetica 22"), anchor=NE)

# C++ developers fear my long ass manually-filled lists...
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
    CustomButton(51, 153, text=".", command=lambda: AddToInputField(".")),
    CustomButton(102, 153, width=151, text="Cash payment", fill="lime"),
    CustomButton(153, 102, width=100, text="Total"),
    CustomButton(153, 51, width=100, text="CANCEL", fill="red"),
    CustomButton(153, 0, width=100, text="CLEAR", fill="red", command=RemoveFromInputField),
    
]

root.bind("<Button-1>", ClickHandler)
root.mainloop()

