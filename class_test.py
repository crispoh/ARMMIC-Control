import customtkinter as ctk
import os 
from PIL import Image
import time



class CustomButton(ctk.CTkButton):
    def __init__(self, master=None, text=None, image=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text=text, image=image, compound=ctk.LEFT, command=command)

root = ctk.CTk()

def iniciar_mapeo(x, n): #agregar densidad de pasos  
    #Inicia Mapeo
    j=0
    for i in range(x):
        print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
        time.sleep(1)   # Se detiene enel punto
        if i % 2 == 0:
            for j in range(n):
                print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                time.sleep(1)   # Se detiene enel punto  
        else:
            for j in range(n, 0, -1):
                print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                time.sleep(1)   # Se detiene enel punto

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files-ctk")
logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "home-dark.png")), size=(26, 26))

def hello_world():
    print("Hello World!")

btn = CustomButton(root, text="Hello", image=logo_image, command=lambda: iniciar_mapeo(16,5))
btn.pack()
btn1 = CustomButton(root, text="Hello", image=logo_image, command=hello_world)
btn1.pack()
btn2 = CustomButton(root, text="Hello", image=logo_image, command=hello_world)
btn2.pack()
btn3 = CustomButton(root, text="Hello", image=logo_image, command=hello_world)
btn3.pack()
btn5 = CustomButton(root, text="Hello", image=logo_image, command=hello_world)
btn5.pack()

root.mainloop()
