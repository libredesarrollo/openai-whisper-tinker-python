import customtkinter
import tkinter.filedialog as filedialog
import subprocess
import threading
import os

import torch # Necesario para detectar GPU/CPU

import whisper

# --- Configuración Básica de la Aplicación ---
customtkinter.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configurar ventana
        self.title("Whisper Transcriptor Local")
        self.geometry("800x600")

        # Configurar la grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Sidebar para Control y Configuración ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        customtkinter.CTkLabel(self.sidebar_frame, text="Configuración", font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Opciones de Modelo
        customtkinter.CTkLabel(self.sidebar_frame, text="Modelo:").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.model_option = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["small", "base", "medium", "large-v3"])
        self.model_option.set("small")
        self.model_option.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Opciones de Idioma
        customtkinter.CTkLabel(self.sidebar_frame, text="Idioma:").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.language_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="ej: es (español)")
        self.language_entry.insert(0, "es") # Valor por defecto
        self.language_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")


        # --- Frame Principal (Entrada de Archivo) ---
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew", columnspan=2)
        self.main_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(self.main_frame, text="Ruta del Video (.mp4, .mov, etc.):", font=customtkinter.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Input de ruta y botón de selección
        self.file_path_entry = customtkinter.CTkEntry(self.main_frame, placeholder_text="Selecciona un archivo de video...")
        self.file_path_entry.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")
        
        self.select_button = customtkinter.CTkButton(self.main_frame, text="Seleccionar Archivo", command=self.browse_file)
        self.select_button.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="e")

        # Botón de Transcripción
        self.transcribe_button = customtkinter.CTkButton(self.main_frame, text="INICIAR TRANSCRIPCIÓN", command=self.start_transcription_thread, height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.transcribe_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

        # --- Área de Salida de Resultados ---
        customtkinter.CTkLabel(self, text="Resultado de la Transcripción:", font=customtkinter.CTkFont(size=13)).grid(row=1, column=1, padx=(20, 20), pady=(10, 0), sticky="w", columnspan=2)
        
        self.output_textbox = customtkinter.CTkTextbox(self, width=250)
        self.output_textbox.grid(row=2, column=1, padx=(20, 20), pady=(10, 20), sticky="nsew", columnspan=2)
        self.output_textbox.insert("0.0", "Esperando archivo de video...")

    # --- Métodos ---
    
    def browse_file(self):
        """Abre el diálogo de selección de archivos y actualiza el campo de entrada."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de video o audio",
            filetypes=(("Archivos de Video/Audio", "*.mp4 *.mov *.wav *.mp3"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            self.file_path_entry.delete(0, customtkinter.END)
            self.file_path_entry.insert(0, file_path)

    def update_output(self, message):
        """Actualiza el área de texto de salida."""
        self.output_textbox.insert(customtkinter.END, message + "\n")
        self.output_textbox.see(customtkinter.END)

    def start_transcription_thread(self):
        """Inicia la transcripción en un hilo separado para no congelar la GUI."""
        file_path = self.file_path_entry.get()
        if not file_path or not os.path.exists(file_path):
            self.update_output("\nERROR: Archivo no encontrado. Por favor, selecciona un archivo válido.")
            return

        self.update_output("\n--- Iniciando Transcripción ---")
        self.transcribe_button.configure(state="disabled", text="TRANSCRBIENDO...")
        
        # Ejecutar la transcripción en un nuevo hilo
        thread = threading.Thread(target=self.run_transcription, args=(file_path,))
        thread.start()

    def run_transcription(self, file_path):
        """Ejecuta el comando Whisper y maneja la salida."""
        try:
            model = self.model_option.get()
            language = self.language_entry.get()

            # El comando 'whisper' requiere la ruta al archivo
            # # # command = [
            # # #     #"whisper",# INSTALALO DE MANERA GLOBAL FUERA DEL VENV
            # # #      "python3",
            # # #      "-m", "whisper",
            # # #     file_path,
            # # #     #"--model", model,
            # # #     "--language", language,
            # # #     "--output_dir", os.path.dirname(file_path), # Guarda el resultado en la misma carpeta que el video
            # # #     "--verbose", "False" # Desactiva la salida detallada que puede llenar la consola
            # # # ]

            self.update_output(f"Modelo: {model}, Idioma: {language}")
            self.update_output("Procesando... Esto tomará un tiempo.")



            model_name = self.model_option.get()
           # 1. Cargar el modelo
            # Detectar el dispositivo (CPU o GPU)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = whisper.load_model(model_name, device=device)
            
            # 2. Transcribir el audio
            result = model.transcribe(
                file_path, 
                language=language, 
                verbose=False # Suprime la salida de progreso
            )

            transcription_result = result["text"]




            # # # # # # Ejecutar el proceso y esperar a que termine
            # # # # # subprocess.run(command, check=True, capture_output=True, text=True)

            # 1. Leer el archivo .txt de salida
            # Whisper guarda la salida con el mismo nombre y extensión .txt
            output_basename = os.path.splitext(os.path.basename(file_path))[0]
            output_dir = os.path.dirname(file_path)
            output_path = os.path.join(output_dir, output_basename + ".txt")

            # # # # # with open(output_path, 'r', encoding='utf-8') as f:
            # # # # #     transcription_result = f.read()

            # 2. Mostrar el resultado completo en la GUI
            self.update_output("\n--- TRANSCRIPCIÓN FINALIZADA ---\n")
            self.update_output(transcription_result)
            self.update_output("\n----------------------------------")
            self.update_output(f"Archivo de texto guardado en: {output_path}")

        except subprocess.CalledProcessError as e:
            self.update_output("\nERROR DE TRANSCRIPCIÓN:")
            self.update_output(f"Verifica que FFmpeg esté en el PATH o que el archivo no esté corrupto.")
            self.update_output(f"Error de salida:\n{e.stderr}")
            
        except FileNotFoundError:
             self.update_output("\nERROR: No se pudo encontrar el comando 'whisper'. Asegúrate de estar ejecutando la app desde el entorno virtual correcto o revisa la instalación.")

        except Exception as e:
            self.update_output(f"\nERROR INESPERADO: {e}")
            
        finally:
            self.transcribe_button.configure(state="normal", text="INICIAR TRANSCRIPCIÓN")

if __name__ == "__main__":
    app = App()
    app.mainloop()