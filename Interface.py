import customtkinter
import os
import serial 
import time
from PIL import Image



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Control ARMMIC")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Función HOME (0,0), NO FUNCIONA FALTA EL SWITCH FINAL DE CARRERA
        def go_home():
            valor = '$H' + '\n'
            ser.write(valor.encode())
            print("YENDO A HOME...")
        # Función Subir un paso
        def test_up():
            valor = '$J=G21G91Y1F51' + '\n'
            ser.write(valor.encode())
            print("UP ")
        # Función BAJAR un paso
        def test_down():
            valor = '$J=G21G91Y-1F51' + '\n'
            ser.write(valor.encode())
            print("DOWN")
        # Función un paso IZQUIERDA
        def test_left():
            valor = '$J=G21G91X1F51' + '\n'
            ser.write(valor.encode())
            print("LEFT")
        # Función un paso DERECHA
        def test_right():
            valor = '$J=G21G91X-1F51' + '\n'
            ser.write(valor.encode())
            print("RIGHT")
        # Función Mapeo
        def iniciar_mapeo(x, n): #agregar densidad de pasos  
            #Inicia Mapeo
            for i in range(x):
                test_up() #ejecuta movimiento CRECIENTE Y
                print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                time.sleep(3)   # Se detiene enel punto
                if i % 2 == 0:
                    for j in range(n):
                        test_left() #ejecuta movimiento CRECIENTE X
                        print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                        time.sleep(3)   # Se detiene enel punto  
                else:
                    for j in range(n, 0, -1):
                        test_right() #ejecuta movimiento DECRECIENTE X
                        print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                        time.sleep(3)   # Se detiene enel punto

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files-ctk")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_dark.png")), size=(20, 20))
        self.file_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "file_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "file_light.png")), size=(20, 20))
        self.setting_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "setting_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "setting_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Control ARMMIC", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cargar GCODE",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.file_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Test",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.setting_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Iniciar Mapeo", image=self.image_icon_image, compound="right", command=lambda: iniciar_mapeo(16,5))
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        # create upload frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.large_test_image)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Selcciona archivo", image=self.image_icon_image, compound="right")
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Iniciar", image=self.image_icon_image, compound="right")
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # create test frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.large_test_image)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="Set Home", image=self.image_icon_image, compound="right", command=go_home)
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.third_frame_button_2 = customtkinter.CTkButton(self.third_frame, text="UP", image=self.image_icon_image, compound="right", command=test_up)
        self.third_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.third_frame_button_3 = customtkinter.CTkButton(self.third_frame, text="DOWN", image=self.image_icon_image, compound="right", command=test_down)
        self.third_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.third_frame_button_4 = customtkinter.CTkButton(self.third_frame, text="Left", image=self.image_icon_image, compound="right", command=test_left)
        self.third_frame_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.third_frame_button_4 = customtkinter.CTkButton(self.third_frame, text="Right", image=self.image_icon_image, compound="right", command=test_right)
        self.third_frame_button_4.grid(row=5, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    # Configurar el puerto serial
    ser = serial.Serial('COM6', 115200)

    # Wake up grbl
    start = '\r\n\r\n' + '\n'
    ser.write(start.encode())
    time.sleep(2)   # Wait for grbl to initialize
    ser.flushInput()  # Flush startup text in serial input
    p_inicial = '$J=G21G91Y1F51' + '\n'
    ser.write(p_inicial.encode())

    app = App()
    app.mainloop()

    # Cerrar el puerto serial
    ser.close()
