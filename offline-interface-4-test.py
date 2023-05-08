import customtkinter as ctk
import os
from PIL import Image


class CustomButton(ctk.CTkButton):
    def __init__(self, master=None, text=None, image=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text=text, image=image, compound=ctk.LEFT, command=command)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Control ARMMIC")
        self.geometry("750x450")

        # Configura el grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar Imagenes
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files-ctk")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "ctk_logo_single.png")), size=(26, 26))
        self.large_name_home = ctk.CTkImage(Image.open(os.path.join(image_path, "large-name-home.png")), size=(500, 150))
        self.large_name_file = ctk.CTkImage(Image.open(os.path.join(image_path, "large-name-file.png")), size=(500, 150))
        self.large_name_config = ctk.CTkImage(Image.open(os.path.join(image_path, "large-name-cofig.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home-dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home-light.png")), size=(20, 20))
        self.file_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "file-dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "file-light.png")), size=(20, 20))
        self.setting_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "config-dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "config-light.png")), size=(20, 20))
        self.row_image_down = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "row_dark_down.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "row_light_down.png")), size=(20, 20))
        self.row_image_up = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "row_dark_up.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "row_light_up.png")), size=(20, 20))
        self.row_image_left = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "row_dark_left.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "row_light_left.png")), size=(20, 20))
        self.row_image_right = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "row_dark_right.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "row_light_right.png")), size=(20, 20))

        # Barra navegacion IZQ
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Control ARMMIC", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cargar GCODE",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.file_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Test",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.setting_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(20,5), sticky="s")

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="by CrisPoh", font=ctk.CTkFont(size=10))
        self.navigation_frame_label.grid(row=7)

        ########################## Frame_HOME ##########################
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        ## Imagen_Frame_HOME
        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_name_home)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        
        ## Frame Variables
        self.frame_home_vars = ctk.CTkFrame(self.home_frame)
        self.frame_home_vars.grid(column=0, row=1, pady=5)
        ###Entry Label X 0
        self.frame_def_x = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_x.grid(column=0, row=0, padx=(10, 5),pady=(10,5))
        #### Label def x
        self.nameLabel = ctk.CTkLabel(self.frame_def_x, text="Densidad X")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        #### Entry def x
        self.nameEntry = ctk.CTkEntry(self.frame_def_x, placeholder_text="Ingresar", justify="center")
        self.nameEntry.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Y 0
        self.frame_def_y = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y.grid(column=1, row=0, padx=(5, 10),pady=(10,5))
        #### Label def Y
        self.nameLabel = ctk.CTkLabel(self.frame_def_y, text="Densidad Y")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Y
        self.nameEntry = ctk.CTkEntry(self.frame_def_y, placeholder_text="Ingresar", justify="center")
        self.nameEntry.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Altura
        self.frame_def_x1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_x1.grid(column=0, row=1, padx=(10, 5),pady=(5, 10))
        #### Label def Altura
        self.nameLabel = ctk.CTkLabel(self.frame_def_x1, text="Altura Inicial")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        #### Entry def Altura
        self.nameEntry = ctk.CTkEntry(self.frame_def_x1, placeholder_text="Ingresar", justify="center")
        self.nameEntry.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Ancho
        self.frame_def_y1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y1.grid(column=1, row=1, padx=(5, 10),pady=(5, 10))
        #### Label def Ancho
        self.nameLabel = ctk.CTkLabel(self.frame_def_y1, text="Ancho Max.")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Ancho
        self.nameEntry = ctk.CTkEntry(self.frame_def_y1, placeholder_text="Ingresar", justify="center")
        self.nameEntry.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ## Boton_Frame_HOME
        self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="Iniciar Mapeo", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=3, column=0, padx=20, pady=10)

        ########################## Upload frame ##########################
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = ctk.CTkLabel(self.second_frame, text="", image=self.large_name_file)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.second_frame_button_1 = ctk.CTkButton(self.second_frame, text="Selcciona archivo", image=self.file_image, compound="right")
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.second_frame_button_2 = ctk.CTkButton(self.second_frame, text="Iniciar", image=self.image_icon_image, compound="right")
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        ########################## Test frame ##########################
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = ctk.CTkLabel(self.third_frame, text="", image=self.large_name_config)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        ## Frame Variables
        self.frame_test_mid = ctk.CTkFrame(self.third_frame)
        self.frame_test_mid.grid(column=0, row=1, pady=5)

        ### Buttons 
        self.third_frame_button_1 = ctk.CTkButton(self.frame_test_mid, text="", image=self.home_image, height=45, width=45)
        self.third_frame_button_1.grid(row=1, column=1, padx=5, pady=5)
        self.third_frame_button_2 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_up, height=60, width=45)
        self.third_frame_button_2.grid(row=0, column=1, pady=(20,5))
        self.third_frame_button_3 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_down, height=60, width=45)
        self.third_frame_button_3.grid(row=2, column=1, pady=(5,20))
        self.third_frame_button_4 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_left, height=45, width=60)
        self.third_frame_button_4.grid(row=1, column=0, padx=(20,5))
        self.third_frame_button_4 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_right, height=45, width=60)
        self.third_frame_button_4.grid(row=1, column=2, padx=(5,20))

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
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":

    app = App()
    app.mainloop()


