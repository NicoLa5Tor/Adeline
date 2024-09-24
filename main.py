import os
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
from matplotlib.figure import Figure
from Sources.op import Opreration_system

obj_op = Opreration_system()
obj_message = Message()
text = None
def fit(prediction = 0.01,mat = None,alpha = 0.5,weigth = None,writeHistorial = False):
    historial = """"""
    historial_real  = """
                       ENTRENAMIENTO ADALINE
    """
    # Creación de objetos
    obj_op = Opreration_system()
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
    diverge = True
    while True:
            E0bt = 0
            Yo = [0] * len(Yd)  # Inicializa las salidas de los patrones
            historial += f"""
            Época {epoca+1}\n
            """
            for i in range(len(Yd)):
                yd = Yd[i]
                net = obj_functions.sum_net(index=i)
                error = yd - net
                Yo[i] = net
                E0bt += abs(error)
                historial += f"""
                El patrón #{i+1} tiene un error de: {E0bt}
                """

                # Actualización de los pesos
                obj_functions.list_w = obj_functions.new_w(index=i, Yop=net)
            Eactual = E0bt / len(Yd)
            if f'Epoca+{epoca}' not in error_vs_epoca:
                error_vs_epoca[f"Epoca+{epoca}"] = Eactual

            if abs(Eactual - Eanterior) < precision:
                historial_real += f"""
                Número de épocas = {epoca+1}
                Alpha = {obj_functions.alpha}
                Error deseado = {prediction}
                Pesos ideales: \n
                {''.join(f"\nw{ii} = {value}"for ii,value in enumerate(obj_functions.list_w))}
                \nEl historial de entrenamiento fue el siguiente: \n
                {historial}
                """
                break
            elif epoca > 2000:
                historial_real += f"""
                Número de épocas = {epoca+1}
                Alpha = {obj_functions.alpha}
                Error deseado = {prediction}
                El entrenamiento fue cancelado por divergencia :´[,
                por lo tanto no hay pesos ideales.

                El en entrenamiento antes de a cancelación es:\n
                {historial}
                """
                print("sale por 5000")
                diverge = False
                break

            Eanterior = Eactual
            epoca += 1
    print(f"Épocas finales: {epoca}")
    print(f"Error final: {Eactual}")
    print(f"Salidas de patrones (Yo): {Yo}")
    print(f"Pesos finales: {obj_functions.list_w}")
    if writeHistorial == True:
            print("entra a historial")
            obj_op.create_write_file(data=historial_real,name="\HisotrialAda.txt",mess=False)
            obj_op.read_historial()
    return diverge,obj_functions.list_w, error_vs_epoca
  

    
def set_text(txt):
    global text 
    text = txt
def get_text():
    global text 
    return text
def btn_aplicacion(inputs,outputs,weights,error,alpha,hit = False):
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
    
        div,list_w, erro_ve_epoca = fit(mat=matriz,prediction=err,alpha=alp,weigth=weigt_list,writeHistorial=hit)
        if div == False or list_w[0] > 10:
            print("Entra")
            obj_message.show_message_info(message="El entrenamiento fue interrumpido por divergencia")
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
    # Variables globales
    global root, obj_message

    # Función para cargar archivo .txt y almacenar su contenido
    # Función para cargar archivo .txt y almacenar su contenido
    def cargar_archivo(entry_field=None):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            try:
                with open(archivo, 'r') as file:
                    data = file.read()
                    if entry_field:
                        entry_field.configure(text=archivo)  # Mostrar nombre del archivo cargado
                    set_text(txt=data)
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
        # Variables y widgets locales a esta función
        def intermediate_ajecutar():
            # Obtener los valores ingresados por el usuario desde la interfaz
            inputs = entradas_manual_entry.get()
            outputs = salidas_manual_entry.get()
            weights = pesos_manual_entry.get()
            error = error_deseado_entry.get()
            alpha = alpha_entry.get()

            # Llamar a la función btn_aplicacion() con los valores obtenidos
            list_w, err_ep = btn_aplicacion(
                inputs=inputs,
                outputs=outputs,
                weights=weights,
                error=error,
                alpha=alpha,
            )
            # Crear una lista de épocas y errores a partir de err_ep
            epocas = list(err_ep.keys())
            errores = list(err_ep.values())

            # Eliminar prefijos innecesarios y dejar solo el número (si existe un prefijo "Epoca+")
            etiquetas_simplificadas = [etiqueta.replace('Epoca+', '') for etiqueta in epocas]

            # Limpiar cualquier gráfica anterior en el frame superior izquierdo (top_left_frame)
            for widget in top_left_frame.winfo_children():
                widget.destroy()

            # Crear la gráfica usando matplotlib en modo oscuro
            fig = Figure(figsize=(4, 3), dpi=85)
            ax = fig.add_subplot(111)

            # Modo oscuro: cambiar colores de fondo y de texto
            fig.patch.set_facecolor('#2e2e2e')  # Fondo del gráfico
            ax.set_facecolor('#2e2e2e')  # Fondo del área de la gráfica
            ax.spines['bottom'].set_color('white')  # Eje X
            ax.spines['left'].set_color('white')    # Eje Y
            ax.xaxis.label.set_color('white')       # Etiqueta eje X
            ax.yaxis.label.set_color('white')       # Etiqueta eje Y
            ax.tick_params(axis='x', colors='white')  # Etiquetas del eje X
            ax.tick_params(axis='y', colors='white')  # Etiquetas del eje Y
            ax.title.set_color('white')             # Título de la gráfica

            # Graficar los datos
            ax.plot(etiquetas_simplificadas, errores, marker='o', color='#1f77b4')  # Color de la línea y puntos
            ax.set_title("Error por Época")
            ax.set_xlabel("Época")
            ax.set_ylabel("Error")

            # Ajustar la cuadrícula (grid) en modo oscuro
            ax.grid(True, which='both', linestyle='--', linewidth=1.5, color='gray')

            # Mostrar solo algunas etiquetas en el eje X (por ejemplo, cada 10 épocas)
            step = max(1, len(etiquetas_simplificadas) // 10)
            ax.set_xticks([i for i in range(0, len(etiquetas_simplificadas), step)])
            ax.set_xticklabels([etiquetas_simplificadas[i] for i in range(0, len(etiquetas_simplificadas), step)],
                               rotation=45, ha='right', fontsize=8)

            # Insertar la gráfica en el área designada (top_left_frame)
            canvas = FigureCanvasTkAgg(fig, master=top_left_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

            # Limpiar cualquier contenido anterior en bottom_left_frame
            for widget in bottom_left_frame.winfo_children():
                widget.destroy()

            
            # Crear un frame scrollable para la tabla de pesos
            scrollable_frame = ctk.CTkScrollableFrame(bottom_left_frame, height=200, width=800)
            scrollable_frame.pack(pady=10, padx=10, fill='both', expand=True)

            # Función para crear celdas con borde
            def create_cell(parent, text, row, column, border_width=1):
                frame = ctk.CTkFrame(parent, border_width=border_width, border_color='gray')
                frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")
                
                label = ctk.CTkLabel(frame, text=text, padx=10, pady=5)
                label.pack(fill='both', expand=True)
                
                return frame

            # Función para crear líneas de separación entre filas
            def create_row_separator(parent, row):
                separator = ctk.CTkFrame(parent, height=1, border_width=1, border_color='gray')
                separator.grid(row=row, column=0, columnspan=2, sticky="ew")
                return separator

            # Configurar expansión de filas y columnas
            scrollable_frame.grid_rowconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=1)

            # Título de la tabla
            create_cell(scrollable_frame, "Pesos ideales", 0, 0, border_width=0).grid(columnspan=2, pady=10, padx=10)

            # Crear la tabla de pesos
            create_cell(scrollable_frame, "Peso", 1, 0)
            create_cell(scrollable_frame, "Valor", 1, 1)

            # Crear líneas de separación entre el encabezado y los datos
            create_row_separator(scrollable_frame, 2)

            # Agregar los pesos a la tabla
            for i, w in enumerate(list_w):
                create_cell(scrollable_frame, f"w{i}", i+2, 0)
                create_cell(scrollable_frame, str(w), i+2, 1)  # Convertir el peso a string sin redondear
                
                # Crear líneas de separación entre filas
                create_row_separator(scrollable_frame, i+3)

            # Ajustar expansión de filas y columnas
            for i in range(len(list_w) + 2):
                scrollable_frame.grid_rowconfigure(i + 2, weight=1)
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=1)


        limpiar_interfaz()

        # Parte superior para imagen y título
        frame_superior = ctk.CTkFrame(root)
        frame_superior.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Cargar la imagen `Udec.jpg`
        try:
            path = obj_op.search_doc(name='Udec.jpg')
            img_udec = Image.open(path)

        except:
            path = 'Udec.jpg'
            img_udec = Image.open(path)
        img_udec = img_udec.resize((900, 200))  # Ajustar tamaño de la imagen
        img_udec_tk = ImageTk.PhotoImage(img_udec)

        # Mostrar la imagen
        udec_label = ctk.CTkLabel(frame_superior, image=img_udec_tk, text="")
        udec_label.image = img_udec_tk
        udec_label.pack()

        # Texto sobre la imagen
        texto_label = ctk.CTkLabel(frame_superior, text="RNA ADALINE APLICACIÓN", font=ctk.CTkFont(size=24, weight="bold"))
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        # Parte inferior: dos columnas
        left_frame = ctk.CTkScrollableFrame(root,height=345)
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
        try:
            txt = obj_op.read_file()
            txt = [a.strip() for a in txt]
            entradas_manual_entry.insert(0,txt[0])
            salidas_manual_entry.insert(0,txt[1])
            pesos_manual_entry.insert(0,txt[2])
            error_deseado_entry.insert(0,txt[3])
            alpha_entry.insert(0,txt[4])
        except Exception as e:
            print(e)
        # Botón para ejecutar
        ejecutar_button = ctk.CTkButton(data_frame, text="Ejecutar", command=intermediate_ajecutar)
        ejecutar_button.pack(pady=20)

    # Función para mostrar la interfaz de Entrenamiento
    def mostrar_entrenamiento():
        # Variables y widgets locales a esta función
        def intermediate_ajecutar_entrenamiento():
            try:
                txt = get_text()
                error = error_deseado_entry.get()
                alpha = alpha_entry.get()

                if txt is None:
                    raise ValueError("No se ha cargado ningún archivo de datos.")

                # Procesar los datos del archivo cargado
                lines = txt.strip().split('\n')
                if len(lines) < 3:
                    raise ValueError("El archivo debe contener al menos 3 líneas: patrones, salidas y pesos.")

                list_patrones = lines[0].strip()
                list_salidas = lines[1].strip()
                list_pesos = lines[2].strip()

                # Llamar a la función de entrenamiento
                list_w, err_ep = btn_aplicacion(
                    inputs=list_patrones,
                    outputs=list_salidas,
                    weights=list_pesos,
                    error=error,
                    alpha=alpha,
                    hit= True
                )
                print(err_ep)
                data = f"""{list_patrones}
                {list_salidas}
                {list_w}
                {error}
                {alpha}"""
                obj_op.create_write_file(data=data)

                # Crear una lista de épocas y errores a partir de err_ep
                epocas = list(err_ep.keys())
                errores = list(err_ep.values())

                # Eliminar prefijos innecesarios y dejar solo el número
                etiquetas_simplificadas = [etiqueta.replace('Epoca+', '') for etiqueta in epocas]

                # Limpiar cualquier gráfica anterior en el frame superior izquierdo (top_left_frame)
                for widget in top_left_frame.winfo_children():
                    widget.destroy()

                # Crear la gráfica usando matplotlib en modo oscuro
                fig = Figure(figsize=(5, 3), dpi=90)
                ax = fig.add_subplot(111)

                # Modo oscuro: cambiar colores de fondo y de texto
                fig.patch.set_facecolor('#2e2e2e')  # Fondo del gráfico
                ax.set_facecolor('#2e2e2e')  # Fondo del área de la gráfica
                ax.spines['bottom'].set_color('white')  # Eje X
                ax.spines['left'].set_color('white')    # Eje Y
                ax.xaxis.label.set_color('white')       # Etiqueta eje X
                ax.yaxis.label.set_color('white')       # Etiqueta eje Y
                ax.tick_params(axis='x', colors='white')  # Etiquetas del eje X
                ax.tick_params(axis='y', colors='white')  # Etiquetas del eje Y
                ax.title.set_color('white')             # Título de la gráfica

                # Graficar los datos
                ax.plot(etiquetas_simplificadas, errores, marker='o', color='#1f77b4')  # Color de la línea y puntos
                ax.set_title("Error por Época")
                ax.set_xlabel("Época")
                ax.set_ylabel("Error")

                # Ajustar la cuadrícula (grid) en modo oscuro
                ax.grid(True, which='both', linestyle='--', linewidth=1.5, color='gray')

                # Mostrar solo algunas etiquetas en el eje X
                step = max(1, len(etiquetas_simplificadas) // 10)
                ax.set_xticks([i for i in range(0, len(etiquetas_simplificadas), step)])
                ax.set_xticklabels(
                    [etiquetas_simplificadas[i] for i in range(0, len(etiquetas_simplificadas), step)],
                    rotation=45, ha='right', fontsize=8
                )

                # Insertar la gráfica en el área designada (top_left_frame)
                canvas = FigureCanvasTkAgg(fig, master=top_left_frame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

                # Limpiar cualquier contenido anterior en bottom_left_frame
                for widget in bottom_left_frame.winfo_children():
                    widget.destroy()

            except Exception as e:
                msg = f"""
                Error al ejecutar el entrenamiento:\n
                ~ {str(e)}
                """
                obj_message.show_message_error(message=msg)

        limpiar_interfaz()

        # Parte superior para imagen y título
        frame_superior = ctk.CTkFrame(root)
        frame_superior.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        root.grid_rowconfigure(1, weight=0)  # Fila de la imagen no se expande

        # Cargar la imagen `Udec.jpg`
        try:
            path = obj_op.search_doc(name='Udec.jpg')
            img_udec = Image.open(path)

        except:
            path = 'Udec.jpg'
            img_udec = Image.open(path)
        img_udec = img_udec.resize((850, 200))  # Ajustar tamaño de la imagen
        img_udec_tk = ImageTk.PhotoImage(img_udec)
        print("Cargando imagen desde:", os.path.abspath("Udec.jpg"))

        # Mostrar la imagen
        udec_label = ctk.CTkLabel(frame_superior, image=img_udec_tk, text="")
        udec_label.image = img_udec_tk
        udec_label.grid(row=0, column=0)

        # Texto sobre la imagen
        texto_label = ctk.CTkLabel(frame_superior, text="RNA ADALINE ENTRENAMIENTO",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        texto_label.place(relx=0.5, rely=0.5, anchor="center")

        # Parte inferior: dos columnas
        left_frame = ctk.CTkScrollableFrame(root)
        left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        data_frame = ctk.CTkScrollableFrame(root, height=345)
        data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el tamaño de las columnas (izquierda más grande que derecha)
        root.grid_columnconfigure(0, weight=3)  # Columna izquierda más grande
        root.grid_columnconfigure(1, weight=1)  # Columna derecha más pequeña
        root.grid_rowconfigure(2, weight=1)     # Fila 2 se expande

        # Configurar el left_frame
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Parte superior del left_frame (Gráfica Error vs Épocas)
        top_left_frame = ctk.CTkFrame(left_frame)
        top_left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        top_left_frame.grid_rowconfigure(1, weight=1)
        top_left_frame.grid_columnconfigure(0, weight=1)

        top_left_label = ctk.CTkLabel(top_left_frame, text="Gráfica Error vs Épocas",
                                      font=ctk.CTkFont(size=16, weight="bold"))
        top_left_label.grid(row=0, column=0, padx=10, pady=10)

        # Parte inferior del left_frame (No se muestra en entrenamiento)
        # Eliminamos o no creamos el bottom_left_frame en la vista de Entrenamiento
        bottom_left_frame = ctk.CTkFrame(left_frame)
        bottom_left_frame.grid_forget()  # No mostramos este frame en Entrenamiento

        # Botón para cargar el archivo de datos
        cargar_label = ctk.CTkLabel(data_frame, text="Cargar Datos:")
        cargar_label.pack(pady=5)
        cargar_button = ctk.CTkButton(data_frame, text="Cargar Archivo", command=lambda: cargar_archivo(cargar_label))
        cargar_button.pack(pady=5)

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

        # Botón para ejecutar
        ejecutar_button = ctk.CTkButton(data_frame, text="Ejecutar", command=intermediate_ajecutar_entrenamiento)
        ejecutar_button.pack(pady=20)

    # Función para limpiar la interfaz sin borrar los botones de selección
    def limpiar_interfaz():
        for widget in root.grid_slaves():
            if widget.grid_info()['row'] != 0:  # Deja intacta la fila con los botones de selección
                widget.destroy()

    def centrar_ventana(root):
    # Obtén las dimensiones de la pantalla
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()

        # Obtén las dimensiones de la ventana
        ancho_ventana = 850
        alto_ventana = 640

        # Calcula la posición de la ventana
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2)) -30

        # Establece la geometría de la ventana
        root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    # Crear la ventana principal
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("blue")  # Tema azul por defecto

    root = ctk.CTk()
    root.title("Adeline | Juan Moreno - Nicolás Rodríguez Torres")
    root.geometry("850x650")
    try:
        root.iconbitmap(obj_op.search_doc(name='logo.ico'))
    except:
        root.iconbitmap('logo.ico')

    centrar_ventana(root=root)
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