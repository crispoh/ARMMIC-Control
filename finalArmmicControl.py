from tkinter import messagebox #Crear ventanas emergentes
import customtkinter as ctk #Interfaz gráfica
import os #Para crear directorios
from PIL import Image #Para mostrar imágenes
import math #Para operaciones matemáticas
import time #Para medir el tiempo
import csv #Para guardar los datos en un archivo csv
import pyvisa #Para comunicarse con el osciloscopio
import numpy as np #Para manejos de arrays
import serial #Para comunicarse con el arduino

class CustomButton(ctk.CTkButton):
    def __init__(self, master=None, text=None, image=None, command=None, **kwargs): 
        super().__init__(master, **kwargs) 
        self.configure(text=text, image=image, compound=ctk.LEFT, command=command)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Control ARMMIC")
        self.geometry("800x450")

        # Configura el grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ############# BRAZO CONFIG #############

        armX = 500 #mm
        armY = 1500 #mm

        ############# DEF PAG HOME #############

        # Función HOME (0,0), NO FUNCIONA FALTA EL SWITCH FINAL DE CARRERA
        def go_home():
            valor = '$H' + '\n'
            ser.write(valor.encode())
            print("YENDO A HOME...: " + valor)
        # Función Subir un paso
        def test_up(a):
            valor = '$J=G21G91Y'+ str(a) +'F60' + '\n'
            ser.write(valor.encode())
            print("UP: " + str(a) + "mm = " + valor)
        # Función BAJAR un paso
        def test_down(a):
            valor = '$J=G21G91Y-'+ str(a) +'F60' + '\n'
            ser.write(valor.encode())
            print("DOWN: " + str(a) + "mm = " + valor)
        # Función un paso IZQUIERDA
        def test_left(a):
            valor = '$J=G21G91X-'+ str(a) +'F60' + '\n'
            ser.write(valor.encode())
            print("LEFT: " + str(a) + "mm = " + valor)
        # Función un paso DERECHA
        def test_right(a):
            valor = '$J=G21G91X'+ str(a) +'F60' + '\n'
            ser.write(valor.encode())
            print("RIGHT: " + str(a) + "mm = " + valor)

        
        ############# Configuración de los datos #############
        def config_map():

            X = self.nameEntryX.get() ## desplazamiento en X (mm)
            Y = self.nameEntryY.get() ## desplazamiento en Y (mm)
            AI = self.nameEntryAI.get() ## Altura inicial (mm)
            AF = self.nameEntryAF.get() ## Altura final (mm)
            BI = self.nameEntryBI.get() ## Ancho inicial (mm)
            BF= self.nameEntryBF.get() ## Ancho final (mm)
            ##Configuración de los datos
            ##ceros
            if int(X) == 0 and int(Y) == 0:
                messagebox.showerror("Error", "El desplazamiento en X e Y no pueden ser 0")

            ## new config arm x
            if int(BF) > 0 and int(BF) <= armX:
                new_armX = int(BF) ## nuevo ancho del brazo
            else:
                messagebox.showerror("Error", "El ancho final está fuera del rango" + "\n" + "Rango: 1mm - " +str(armX)+ "mm" )
                print("Error: El ancho final está fuera del rango. Rango: 1mm - " +str(armX)+ "mm")
            
            if int(AF) > 0 and int(AF) <= armY:
                new_armY = int(AF) ## nuevo ancho del brazo
            else:
                messagebox.showerror("Error", "El Alto final está fuera del rango" + "\n" + "Rango: 1mm - " +str(armY)+ "mm" )
                print("Error: El alto final está fuera del rango. Rango: 1mm - " +str(armY)+ "mm")

            ## new config arm y
            if int(AI) >= 0 and int(AI) <= new_armY:
                if int(AI) == 0:
                    trozoY = new_armY ## trozo Y del work zone
                else:
                    trozoY = new_armY - int(AI)
            else:
                messagebox.showerror("Error", "La altitud del brazo está fuera del rango" + "\n" + "Rango: 0mm - " +str(new_armY)+ "mm" )
                print("Error: La altitud del brazo está fuera del rango. Rango: 0mm - " +str(new_armY)+ "mm")

            ## new config arm x
            if int(BI) >= 0 and int(BI) <= new_armX:
                if int(BI) == 0:
                    trozoX = new_armX ## trozo X del work zone
                else:
                    trozoX= new_armX - int(BI)
            else:
                messagebox.showerror("Error", "El ancho del brazo está fuera del rango" + "\n" + "Rango: 0mm - " +str(new_armX)+ "mm" )
                print("Error: El ancho del brazo está fuera del rango. Rango: 0mm - " +str(new_armX)+ "mm")

            ## pasos en X
            if int(X) > new_armX:
                ## Error X
                messagebox.showerror("Error", "El desplazamiento en X es mayor que el largo del brazo" + "\n" + "MAX: " +str(new_armX)+ "mm")
                print("Error: El desplazamiento en X es mayor que el largo del brazo " + str(new_armX))
            else:
                ## pasos en Y
                if int(Y) > new_armY:
                    ## Error Y
                    messagebox.showerror("Error", "El desplazamiento en Y es mayor que el ancho del brazo" + "\n" + "MAX: " +str(new_armY)+ "mm")
                    print("Error: El desplazamiento en Y es mayor que el ancho del brazo " + str(new_armY))
                else:
                    ## pasos en X
                    pasosX = trozoX/int(X)
                    ##Aproximamos a un numero entero
                    pasosX_floor = math.floor(pasosX)

                    ## pasos en Y
                    pasosY = trozoY/int(Y)
                    ##Aproximamos a un numero entero
                    pasosY_floor = math.floor(pasosY)
                    ##Tiempo total del mapeo
                    tiempo = 5
                    total_pasos = (int(pasosY_floor)+1)*int((pasosX_floor)+1)
                    tiempo_ejecucion = (total_pasos * (tiempo + 1))/60
                    messagebox.showinfo("Datos", "Se va a ejecutar el mapeo con los siguientes datos:" + "\n" 
                                        + str(pasosX_floor) + " pasos con desplazamiento en X cada " + str(X) + "mm" + "\n"
                                        + str(pasosY_floor) + " pasos con desplazamiento en Y cada " + str(Y) + "mm" + "\n" 
                                        + "Total de pasos: " + str(total_pasos) + "\n"
                                        + "Altura Final: " + str(AF) + "mm" + "\n" 
                                        + "Altura Inicial: " + str(AI) + "mm" + "\n" 
                                        + "Ancho Final: " + str(BF) + "mm"+ "\n" 
                                        + "Ancho Inicial: " + str(BI) + "mm"+ "\n" 
                                        + "Work Zone: Alto=" + str(trozoY) + "mm x Ancho:" + str(trozoX) + "mm")
                    ##Confirmar datos por el usuario con un messagebox de aceptar o cancelar    
                    if messagebox.askokcancel("Confirmar", "¿Desea continuar con el mapeo?" + "\n"
                                        + "Tiempo Aproximado de Ejecución: " + str(tiempo_ejecucion)+ " minutos"):
                        ##Iniciar mapeo
                        start_maping(pasosX_floor, pasosY_floor, X, Y, AI, BI, tiempo )
                    else:
                        print("Mapeo cancelado")

        ############# Crear .csv y crea nombres de columnas #############

        def crear_csv():
            # Nombres de las columnas
            columnas = ['x', 'y', "Datos"]
            # Crear el archivo CSV y escribir los nombres de las columnas
            with open('datos.csv', 'w', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow(columnas)

        ############# Añade el dato del mapeo a la ultima fila #############

        def mandar_osciloscopio(ejeX, ejeY, datos):
            ##almacenar coordenadas en un archivo .csv y concatenar
            # Abrir el archivo CSV en modo de escritura
            with open('datos.csv', 'a', newline='') as archivo_csv:
                # Crear un objeto escritor CSV
                escritor_csv = csv.writer(archivo_csv)
        
                # Escribir una nueva fila con los datos de "x", "y" y "Datos"
                escritor_csv.writerow([ejeX, ejeY, datos])

        ############# Inicia toma de datos del osciloscopio y almacena arreglo #############

        def toma_datos_osciloscopio(x, y):
            # Obtener los datos de la forma de onda
            datos_binarios = osciloscopio.query_binary_values("CURV?", datatype='h', container=np.array)

            #almacenar datos en un archivo .csv
            mandar_osciloscopio(x,y,datos_binarios[:1000])
            print("Datos almacenados en .csv")

        ############# Iniciar mapeo con los datos ingresados #############

        def start_maping(XF, YF, X, Y, AI,BI, t):

            print("Iniciando mapeo")
            ##Setear configuracion inicial
            # Configurar el osciloscopio para adquirir los datos de la forma de onda
            osciloscopio.write("DAT:SOU CH1")  # Configurar la fuente de datos como Canal 1
            osciloscopio.write("DAT:ENC RPB")  # Configurar el formato de datos como binario sin comprimir
            osciloscopio.write("DAT:WID 2")    # Configurar el ancho de datos en 2 bytes (int16)
            osciloscopio.write("DAT:STAR 1")   # Configurar el punto de inicio de los datos en 1
            osciloscopio.write("DAT:STOP 1000")# Configurar el punto de parada de los datos en 1000
            ##obtener escala    
            go_home() #ejecuta movimiento HOME
            ##genera el .csv
            crear_csv()
            print("Archivo .csv creado")
            test_up(AI) #ejecuta movimiento CRECIENTE Y
            print("Desplazamiento en Y: "+str(AI)+"mm")
            test_right(BI) #ejecuta movimiento CRECIENTE x
            print("Desplazamiento en X: "+str(BI)+"mm")
            ##EJECUTAR MAPEO
            j,i = 0,0
            for i in range(XF):
                test_up(X) #ejecuta movimiento CRECIENTE Y
                print("("+str(i)+","+str(j)+")") #ejecuta SERVO O SEÑAL
                time.sleep(t) # Se detiene en el punto
                if i % 2 == 0:
                    for j in range(YF):
                        test_right(Y) #ejecuta movimiento CRECIENTE X
                        print("("+str(i)+","+str(j)+")") ##muestra coordenadas en consola
                        #EJECUTAR OBTENCION DE DATOS DEL OSCILOSCOPIO
                        time.sleep(t)   # Se detiene enel punto  
                        toma_datos_osciloscopio(i,j)
                        
                else:
                    for j in range(YF, 0, -1):
                        test_left(Y) #ejecuta movimiento DECRECIENTE X
                        print("("+str(i)+","+str(j)+")") ##muestra coordenadas en consola
                        #EJECUTAR OBTENCION DE DATOS DEL OSCILOSCOPIO
                        time.sleep(t)   # Se detiene enel punto  
                        toma_datos_osciloscopio(i,j)

            ##EJECUTar mapeo terminado
            mapeo_terminado()

        ############# FIN MAPEO #############

        def mapeo_terminado():
            print("Mapeo terminado")
            ##mesage si desea iir a home 
            if messagebox.askokcancel("Mapeo Terminado", "¿Desea ir a Home?"):
                go_home()
                messagebox.showinfo("Mapeo Terminado", "Mapeo Terminado con exito")
            else:
                messagebox.showinfo("Mapeo Terminado", "Mapeo Terminado con exito")


        ############# Cargar Imagenes #############
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files-ctk")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.arm_setup_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "setup_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "setup_dark.png")), size=(500, 430))
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
        self.setup_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "book-dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "book-light.png")), size=(20, 20))
        self.row_image_down = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_down.png")), size=(20, 20))
        self.row_image_up = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_up.png")), size=(20, 20))
        self.row_image_left = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_left.png")), size=(20, 20))
        self.row_image_right = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_right.png")), size=(20, 20))

        ##Proxima implementacion...
        ##self.row_image_down_left = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_down_left.png")), size=(20, 20))
        ##self.row_image_down_right = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_down_right.png")), size=(20, 20))
        ##self.row_image_up_left = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_up_left.png")), size=(20, 20))
        ##self.row_image_up_right = ctk.CTkImage(Image.open(os.path.join(image_path, "row_light_up_right.png")), size=(20, 20))

        ############# Barra navegacion IZQ #############
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

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

        self.frame_4_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Guia",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.setup_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(20,5), sticky="s")

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="by CrisPoh", font=ctk.CTkFont(size=10))
        self.navigation_frame_label.grid(row=7)

        ############# Frame_HOME #############
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
        self.frame_def_x.grid(row=0, column=0, padx=(10, 5),pady=(10,5))
        #### Label def x
        self.nameLabel = ctk.CTkLabel(self.frame_def_x, text="Densidad X")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        #### Entry def x ## DATO A INGRESAR
        self.nameEntryX = ctk.CTkEntry(self.frame_def_x, placeholder_text="Ingresar", justify="center")
        self.nameEntryX.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Y 0
        self.frame_def_y = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y.grid(row=1, column=0, padx=(10, 5),pady=(5,10))
        #### Label def Y
        self.nameLabel = ctk.CTkLabel(self.frame_def_y, text="Densidad Y")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Y ## DATO A INGRESAR
        self.nameEntryY = ctk.CTkEntry(self.frame_def_y, placeholder_text="Ingresar", justify="center")
        self.nameEntryY.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Altura min
        self.frame_def_x1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_x1.grid(row=1, column=1, padx=5,pady=(5, 10))
        #### Label def Altura
        self.nameLabel = ctk.CTkLabel(self.frame_def_x1, text="Altura Inicial")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        #### Entry def Altura ## DATO A INGRESAR
        self.nameEntryAI = ctk.CTkEntry(self.frame_def_x1, placeholder_text="Ingresar", justify="center")
        self.nameEntryAI.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Alto max
        self.frame_def_y1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y1.grid(row=1, column=2, padx=(5, 10),pady=(5, 10))
        #### Label def Alto max
        self.nameLabel = ctk.CTkLabel(self.frame_def_y1, text="Alto Max.")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Alto max
        self.nameEntryAF = ctk.CTkEntry(self.frame_def_y1, placeholder_text="Ingresar", justify="center")
        self.nameEntryAF.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ###Entry Label Ancho min
        self.frame_def_y1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y1.grid(row=0, column=1, padx=5,pady=(10, 5))
        #### Label def Ancho min
        self.nameLabel = ctk.CTkLabel(self.frame_def_y1, text="Ancho Inicial")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Ancho min ## DATO A INGRESAR
        self.nameEntryBI = ctk.CTkEntry(self.frame_def_y1, placeholder_text="Ingresar", justify="center")
        self.nameEntryBI.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )
        
        ###Entry Label Ancho max
        self.frame_def_y1 = ctk.CTkFrame(self.frame_home_vars, width=70)
        self.frame_def_y1.grid(row=0, column=2, padx=(5, 10),pady=(10, 5))
        #### Label def Ancho
        self.nameLabel = ctk.CTkLabel(self.frame_def_y1, text="Ancho Max.")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=(10,3), sticky="ew")
        ##### Entry def Ancho ## DATO A INGRESAR
        self.nameEntryBF = ctk.CTkEntry(self.frame_def_y1, placeholder_text="Ingresar", justify="center")
        self.nameEntryBF.grid(row=1, column=0, padx=20, pady=(3,15), sticky="ew", )

        ## Boton_Frame_HOME
        self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="Iniciar Mapeo", image=self.image_icon_image, compound="right", command=config_map)
        self.home_frame_button_2.grid(row=3, column=0, padx=20, pady=10)

        ############# Fin Frame_HOME #############

        ############# Upload frame #############
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = ctk.CTkLabel(self.second_frame, text="", image=self.large_name_file)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.second_frame_button_1 = ctk.CTkButton(self.second_frame, text="Selcciona archivo", image=self.file_image, compound="right")
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.second_frame_button_2 = ctk.CTkButton(self.second_frame, text="Iniciar", image=self.image_icon_image, compound="right")
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        ############# Fin Frame_Upload #############

        ############# Test frame #############
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = ctk.CTkLabel(self.third_frame, text="", image=self.large_name_config)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        ## Frame Variables
        self.frame_test_mid = ctk.CTkFrame(self.third_frame)
        self.frame_test_mid.grid(column=0, row=1, pady=5)

        ### Buttons 
        self.third_frame_button_1 = ctk.CTkButton(self.frame_test_mid, text="", image=self.home_image, height=45, width=45, command= go_home)
        self.third_frame_button_1.grid(row=1, column=1, padx=5, pady=5)
        self.third_frame_button_2 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_up, height=60, width=45, command= lambda: test_up(10))
        self.third_frame_button_2.grid(row=0, column=1, pady=(20,5))
        self.third_frame_button_3 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_down, height=60, width=45, command= lambda: test_down(10))
        self.third_frame_button_3.grid(row=2, column=1, pady=(5,20))
        self.third_frame_button_4 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_left, height=45, width=60, command= lambda: test_left(10))
        self.third_frame_button_4.grid(row=1, column=0, padx=(20,5))
        self.third_frame_button_4 = ctk.CTkButton(self.frame_test_mid, text="", image=self.row_image_right, height=45, width=60, command= lambda: test_right(10))
        self.third_frame_button_4.grid(row=1, column=2, padx=(5,20))

        ############# Fin Frame_Test #############

        ############# Config frame #############
        self.four_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.four_frame.grid_columnconfigure(0, weight=1)

        self.four_frame_large_image_label = ctk.CTkLabel(self.four_frame, text="", image=self.arm_setup_image)
        self.four_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        ############# Fin Frame_Config #############

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

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
        if name == "frame_4":
            self.four_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.four_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    
    # Crear instancia del administrador de recursos
    rm = pyvisa.ResourceManager()

    # Abrir conexión con el osciloscopio
    osciloscopio = rm.open_resource("USB0::0x0699::0x0367::C050620::INSTR")

    # Configurar el puerto serial
    ser = serial.Serial('COM4', 115200)

    # Wake up grbl
    start = '\r\n\r\n' + '\n'
    ser.write(start.encode())
    time.sleep(2)   # Wait for grbl to initialize
    ser.flushInput()  # Flush startup text in serial input

    app = App()
    app.mainloop()

    # Cerrar el puerto serial
    ser.close()
    # Cerrar la conexión con el osciloscopio
    osciloscopio.close()


