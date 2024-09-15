from Sources.opreations_sistem import Operations
from Sources.patrones import Patrones
from Sources.Functions import Functions
from Sources.message import Message
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
obj_message = Message()

def fit(prediction = 0.01,mat = None,alpha = 0.5,weigth = None):
    # Creación de objetos
    obj_op = Operations()
    obj_patrons = Patrones()
    obj_functions = Functions()

    # Declaración de variables del problema
    precision = prediction
    epoca = 0
    Eanterior = float("inf")
    error_vs_epoca ={}

    # Declaración y agregación de variables
    # Inicializa pesos
    matriz = obj_patrons.option_1() if mat == None else mat
    print(matriz)
    Yd = [fila[-1] for fila in matriz]  # Salidas deseadas
    obj_op.iteration = len(matriz[0])-1
    w = obj_op.w() if weigth == None else weigth
    print(w)
    obj_functions.alpha = alpha
    obj_functions.list_w = w  
    obj_functions.logical = matriz  

    # Entrenamiento
    while True:
        E0bt = 0
        Yo = [0] * len(Yd)  # Inicializa las salidas de los patrones

        for i in range(len(Yd)):
            yd = Yd[i]
            net = obj_functions.sum_net(index=i)
            error = yd - net
            Yo[i] = net
            E0bt += abs(error)

            # Actualización de los pesos
            obj_functions.list_w = obj_functions.new_w(index=i, Yop=net)
        Eactual = E0bt / len(Yd)
        if f'Epoca+{epoca}' not in error_vs_epoca:
            error_vs_epoca[f"Epoca+{epoca}"] = Eactual

        if abs(Eactual - Eanterior) < precision:
            break

        Eanterior = Eactual
        epoca += 1

    print(f"Épocas finales: {epoca}")
    print(f"Error final: {Eactual}")
    print(f"Salidas de patrones (Yo): {Yo}")
    print(f"Pesos finales: {obj_functions.list_w}")
    return obj_functions.list_w, error_vs_epoca
def btn_aplicacion(inputs,outputs,weights,error,alpha):
    global obj_message
    try:
        inp = str(inputs)[1:-1]
        out = str(outputs)[1:-1]
        weigth = str(weights)[1:-1]
        err = float(error)
        alp = float(alpha)
       
        list_inputs = inp.split(",")
        list_out = out.split(",")
        list_weigts = weigth.split(",")
        if not list_inputs or inp == "" or len(inp) < 1:
            msg_inp =f"""
            Error con los patrones:  {inputs}\n
            ~ No digite caracteres diferentes a números, comas, o corchetes cerrados "[]"\n
            ~ No deje espacios en la entrada\n
            ~ Colóquelos entre corchetes cerrados [] y separe por comas
            Ejemplo:\n
            [1111,0000,1111,1010]
            """
            obj_message.show_message_error(message=msg_inp)
        if not list_out or out == "" or len(out) < 1:
            msg_inp =f"""
            Error con las salidas {outputs}\n
            ~ No digite caracteres diferentes a numeros, comas, o corchetes cerrados "[]"\n
            ~ No deje espacios en la entrada\n
            ~ Colóquelos entre corchetes cerrados [] y separe por comas
            Ejemplo:\n
            [1,2,3,4]
            """
            obj_message.show_message_error(message=msg_inp)
        #variables para entrenar
        print(weigth)
        matriz = []
        for index,cadena in enumerate(list_inputs):
            row = []
            for caracter in cadena:
                row.append(int(caracter))
            row.append(-1)
            row.append(int(list_out[index]))
            matriz.append(row)
        tam = len(matriz[0]) - 1
        weigt_list = [float(list_weigts[a]) for a in range(tam)]
        print("el error no es aqui")
        list_w, erro_ve_epoca = fit(mat=matriz,prediction=err,alpha=alp,weigth=weigt_list)
        return list_w,erro_ve_epoca

        #datos para enviar al entrenamiento
        
       

                
    except Exception as e:
        msg = f"""
        Error...\n

        ~ Ocurrió algo con lo datos, Por favor revise que esten bien escritos.\n
        ~ Las entradas para pesos, error y alpha no pueden tener caracteres no numéricos \n
        ~ Deben ser la misma cantidad de patrones y de salidas deseadas \n
        ~ El error es: {e}

        """
        obj_message.show_message_error(message=msg)

    

def graficar():
    # Función para cargar archivo .txt y mostrar su contenido
    def cargar_archivo(entry_field):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            try:
                with open(archivo, 'r') as file:
                    data = file.read()
                    entry_field.configure(text=data)  # Mostrar contenido en el label
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    # Función de validación para permitir solo números y un punto decimal
    def validate_float(new_value):
        if new_value == "" or new_value == ".":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    # Función para mostrar la interfaz de Aplicación
    def mostrar_aplicacion():
        def intermediate_ajecutar():
            list_w,err_ep = btn_aplicacion( inputs=entradas_manual_entry.get(),
                            outputs=salidas_manual_entry.get(),
                            weights=pesos_manual_entry.get(),
                            error=error_deseado_entry.get(),
                            alpha=alpha_entry.get(),
                            )
            
        # Limpiar la interfaz, pero dejar los botones de selección
        limpiar_interfaz()

        # Parte superior para imagen y título
        frame_superior = ctk.CTkFrame(root)
        frame_superior.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Cargar la imagen `Udec.jpg`
        img_udec = Image.open("Udec.jpg")
        img_udec = img_udec.resize((800, 200))  # Ajustar tamaño de la imagen
        img_udec_tk = ImageTk.PhotoImage(img_udec)

        # Mostrar la imagen
        udec_label = ctk.CTkLabel(frame_superior, image=img_udec_tk, text="")
        udec_label.image = img_udec_tk
        udec_label.pack()

        # Texto sobre la imagen
        texto_label = ctk.CTkLabel(frame_superior, text="RNA ADALINE APLICACIÓN", font=ctk.CTkFont(size=24, weight="bold"))
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        # Parte inferior: dos columnas
        left_frame = ctk.CTkFrame(root)
        left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        data_frame = ctk.CTkScrollableFrame(root, height=345)
        data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el tamaño de las columnas (izquierda más grande que derecha)
        root.grid_columnconfigure(0, weight=3)  # Columna izquierda más grande
        root.grid_columnconfigure(1, weight=1)  # Columna derecha más pequeña

        # Dividir el left_frame en dos filas (superior más grande que inferior)
        left_frame.grid_rowconfigure(0, weight=3)  # Fila superior con más peso
        left_frame.grid_rowconfigure(1, weight=1)  # Fila inferior con menos peso
        left_frame.grid_columnconfigure(0, weight=1)  # Aseguramos que las columnas tomen todo el ancho

        # Parte superior del left_frame (Gráfica Error vs Épocas)
        top_left_frame = ctk.CTkFrame(left_frame)
        top_left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        top_left_label = ctk.CTkLabel(top_left_frame, text="Gráfica Error vs Épocas", font=ctk.CTkFont(size=16, weight="bold"))
        top_left_label.pack(pady=10)  # Colocar el texto

        # Parte inferior del left_frame (Pesos Finales)
        bottom_left_frame = ctk.CTkFrame(left_frame)
        bottom_left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        bottom_left_label = ctk.CTkLabel(bottom_left_frame, text="Pesos Finales", font=ctk.CTkFont(size=16, weight="bold"))
        bottom_left_label.pack(pady=10)  # Colocar el texto

        # Entradas manuales
        entradas_label = ctk.CTkLabel(data_frame, text="Entradas (Ej: [0000,....,1111]):")
        entradas_label.pack(pady=5)
        entradas_manual_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: [0000, 0001, ..., 1111]")
        entradas_manual_entry.pack(pady=5)

        # Salidas manuales
        salidas_manual_label = ctk.CTkLabel(data_frame, text="Salidas (Ej: [0,1,2,3,...,15]):")
        salidas_manual_label.pack(pady=5)
        salidas_manual_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej:[0, 1, ..., 15]")
        salidas_manual_entry.pack(pady=5)

        # Pesos manuales
        pesos_manual_label = ctk.CTkLabel(data_frame, text="Pesos (Ej: [2.5, 3.5]):")
        pesos_manual_label.pack(pady=5)
        pesos_manual_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: 2.5, 3.5")
        pesos_manual_entry.pack(pady=5)

        # Error deseado
        error_deseado_label = ctk.CTkLabel(data_frame, text="Error Deseado:")
        error_deseado_label.pack(pady=5)
        vcmd = (root.register(validate_float), "%P")
        error_deseado_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: 0.001")
        error_deseado_entry.pack(pady=5)
        error_deseado_entry.configure(validate="key", validatecommand=vcmd)

        # Alpha
        alpha_label = ctk.CTkLabel(data_frame, text="Alpha:")
        alpha_label.pack(pady=5)
        alpha_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: 0.5")
        alpha_entry.pack(pady=5)
        alpha_entry.configure(validate="key", validatecommand=vcmd)
        

        # Botón para ejecutar (sin funcionalidad)
        ejecutar_button = ctk.CTkButton(data_frame, text="Ejecutar",command=intermediate_ajecutar)
        ejecutar_button.pack(pady=20)

    # Función para mostrar la interfaz de Entrenamiento
    def mostrar_entrenamiento(data = None):
        limpiar_interfaz()

        # Parte superior para imagen y título
        frame_superior = ctk.CTkFrame(root)
        frame_superior.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Cargar la imagen `Udec.jpg`
        img_udec = Image.open("Udec.jpg")
        img_udec = img_udec.resize((850, 200))  # Ajustar tamaño de la imagen
        img_udec_tk = ImageTk.PhotoImage(img_udec)

        # Mostrar la imagen
        udec_label = ctk.CTkLabel(frame_superior, image=img_udec_tk, text="")
        udec_label.image = img_udec_tk
        udec_label.pack()

        # Texto sobre la imagen
        texto_label = ctk.CTkLabel(frame_superior, text="RNA ADALINE ENTRENAMIENTO", font=ctk.CTkFont(size=24, weight="bold"))
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        # Parte inferior: dos columnas
        left_frame = ctk.CTkScrollableFrame(root)
        left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        data_frame = ctk.CTkScrollableFrame(root,height=345)
        data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el tamaño de las columnas (izquierda más grande que derecha)
        root.grid_columnconfigure(0, weight=3)  # Columna izquierda más grande
        root.grid_columnconfigure(1, weight=1)  # Columna derecha más pequeña

                # Gráfica Error vs Épocas en el left_frame
                # Datos de ejemplo en un diccionario
       
        
        datos = data
        # Crear la figura y los ejes de Matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(datos['Épocas'], datos['Error'], label='Seno')
        ax.set_xlabel('Épocas')
        ax.set_ylabel('Error')
        ax.set_title('Gráfica Error vs Épocas')
        ax.legend()

            # Configurar la ventana principal
        root = ctk.CTk()
        root.title("Mostrar Gráfica")

            # Crear un frame para organizar los widgets
        left_frame = ctk.CTkFrame(root)
        left_frame.pack(padx=20, pady=20)

            # Etiqueta para la gráfica
        grafica_label = ctk.CTkLabel(left_frame, text="Gráfica Error vs Épocas", font=ctk.CTkFont(size=16, weight="bold"))
        grafica_label.pack(pady=10)

            # Crear un canvas para la gráfica y agregarlo a la interfaz
        canvas = FigureCanvasTkAgg(fig, master=left_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10, fill='both', expand=True)

            # Dibujar la gráfica
        canvas.draw()

        # Entradas manuales
        entradas_label = ctk.CTkLabel(data_frame, text="Cargar Entradas:")
        entradas_label.pack(pady=5)
        entradas_button = ctk.CTkButton(data_frame, text="Cargar Entradas", command=lambda: cargar_archivo(entradas_label))
        entradas_button.pack(pady=5)

        # Salidas manuales
        salidas_label = ctk.CTkLabel(data_frame, text="Cargar Salidas:")
        salidas_label.pack(pady=5)
        salidas_button = ctk.CTkButton(data_frame, text="Cargar Salidas", command=lambda: cargar_archivo(salidas_label))
        salidas_button.pack(pady=5)

        # Pesos manuales
        pesos_label = ctk.CTkLabel(data_frame, text="Cargar Pesos:")
        pesos_label.pack(pady=5)
        pesos_button = ctk.CTkButton(data_frame, text="Cargar Pesos", command=lambda: cargar_archivo(pesos_label))
        pesos_button.pack(pady=5)

        # Error deseado
        error_deseado_label = ctk.CTkLabel(data_frame, text="Error Deseado:")
        error_deseado_label.pack(pady=5)
        vcmd = (root.register(validate_float), "%P")
        error_deseado_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: 0.001")
        error_deseado_entry.pack(pady=5)
        error_deseado_entry.configure(validate="key", validatecommand=vcmd)

        # Alpha
        alpha_label = ctk.CTkLabel(data_frame, text="Alpha:")
        alpha_label.pack(pady=5)
        alpha_entry = ctk.CTkEntry(data_frame, width=200, placeholder_text="Ej: 0.5")
        alpha_entry.pack(pady=5)
        alpha_entry.configure(validate="key", validatecommand=vcmd)

        # Botón para ejecutar (sin funcionalidad)
        ejecutar_button = ctk.CTkButton(data_frame, text="Ejecutar")
        ejecutar_button.pack(pady=20)
        print(error_deseado_entry.get())
    

    # Función para limpiar la interfaz sin borrar los botones de selección
    def limpiar_interfaz():
        for widget in root.grid_slaves():
            if widget.grid_info()['row'] != 0:  # Deja intacta la fila con los botones de selección
                widget.destroy()

    # Crear la ventana principal
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("blue")  # Tema azul por defecto

    root = ctk.CTk()
    root.title("Selector de Aplicación y Entrenamiento")
    root.geometry("840x640")

    # Botones de selección entre "Aplicación" y "Entrenamiento", siempre visibles
    
    frame_seleccion = ctk.CTkFrame(root)
    frame_seleccion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    boton_aplicacion = ctk.CTkButton(frame_seleccion, text="Aplicación", command=mostrar_aplicacion)
    boton_aplicacion.pack(side="left", padx=20)

    boton_entrenamiento = ctk.CTkButton(frame_seleccion, text="Entrenamiento", command=mostrar_entrenamiento)
    boton_entrenamiento.pack(side="left", padx=20)

    # Iniciar con la vista de "Aplicación" como predeterminada
    mostrar_aplicacion()

    # Iniciar la aplicación
    root.mainloop()
graficar()