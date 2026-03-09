import customtkinter
import tkinter.filedialog as filedialog
import threading
import os
import sys
import torch 
import whisper
import queue

# --- Configuración de la App ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Whisper Transcriptor Local - Pro Edition")
        self.geometry("800x600")
        
        # Cola para mensajes entre hilos
        self.msg_queue = queue.Queue()
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_frame, text="Configuración", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=20)
        
        self.model_option = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["small", "base", "medium"])
        self.model_option.set("small")
        self.model_option.grid(row=1, column=0, padx=20, pady=10)

        # --- Main UI ---
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.file_path_entry = customtkinter.CTkEntry(self.main_frame, placeholder_text="Selecciona un archivo...")
        self.file_path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.select_button = customtkinter.CTkButton(self.main_frame, text="Buscar", command=self.browse_file)
        self.select_button.grid(row=0, column=1, padx=10, pady=10)

        self.transcribe_button = customtkinter.CTkButton(self.main_frame, text="INICIAR", command=self.start_transcription_thread, height=40)
        self.transcribe_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.output_textbox = customtkinter.CTkTextbox(self)
        self.output_textbox.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="nsew")
        
        # Iniciar chequeo de la cola
        self.after(100, self.process_queue)

    def process_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self.output_textbox.insert(customtkinter.END, msg + "\n")
                self.output_textbox.see(customtkinter.END)
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_entry.delete(0, customtkinter.END)
            self.file_path_entry.insert(0, file_path)

    def start_transcription_thread(self):
        file_path = self.file_path_entry.get()
        if not os.path.exists(file_path):
            self.msg_queue.put("Error: Archivo no encontrado.")
            return
        threading.Thread(target=self.run_transcription, args=(file_path,), daemon=True).start()

    def run_transcription(self, file_path):
        try:
            # --- BLOQUEADOR DE ERRORES ---
            # Si estamos congelados (en ejecutable), redirigimos stderr a un archivo
            # para evitar que intente escribir en un objeto nulo
            if getattr(sys, 'frozen', False):
                devnull = open(os.devnull, 'w')
                sys.stderr = devnull
            
            self.msg_queue.put("Cargando modelo...")
            model = whisper.load_model(self.model_option.get(), device="cpu")
            
            self.msg_queue.put("Transcribiendo...")
            result = model.transcribe(file_path, verbose=False)
            
            texto = result["text"]
            # Guardar en una ruta absoluta y segura (Escritorio del usuario)
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop, "transcripcion.txt")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(texto)
                
            self.msg_queue.put(f"--- FINALIZADO ---\nGuardado en: {output_path}")
            
        except Exception as e:
            # Esto nos dirá exactamente qué archivo está causando el error
            self.msg_queue.put(f"ERROR: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()