from tkinter import *


# ------ CUSTOM WIDGETS START ------

class CustomButton:
    def __init__(self, x, y, **kwargs) -> None:
        self.x: int = x
        self.y: int = y
        self.kwargs = kwargs

        if "command" in kwargs:
            self.command = kwargs["command"]

        canvas.create_rectangle(self.x, self.y, self.x+50, self.y+50, outline="black", fill="gray")

        if "text" in kwargs:
            canvas.create_text((self.x+25.5, self.y+25.5), text=kwargs["text"], anchor=CENTER, fill="black", font=("Helvetica 12")) 
            

    def OnMouseRelease(self):
        if "command" in self.kwargs:
            return self.command()
    
# ------ CUSTOM WIDGETS END ------

def ClickHandler(event): # This method only gets called on LEFT click
    global buttons
    for button in buttons:
        if event.x >= button.x and event.y >= button.y and event.x <= button.x+50 and event.y <= button.y+50:
            button.OnMouseRelease()


# ------ TKINTER BOILERPLATE BULLSHIT BELOW ------

root = Tk()
root.title("v2")
root.geometry("500x500")

canvas = Canvas(root, width=500, height=500)
canvas.place(x=0, y=0)

# I have no idea why my button list has to be in the middle of this shit bro
buttons: list[CustomButton] = [
    CustomButton(10, 10, text="CLR", command=lambda: print("CLR")),
    CustomButton(150, 150)
]

root.bind("<Button-1>", ClickHandler)
root.mainloop()

