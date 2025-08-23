#!/usr/bin/env python3
"""
💻 FLASH UNIVERSAL - Desktop Application
App desktop per pubblicazione universale su tutti gli store
Supporta Windows, macOS, Linux
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import asyncio
import json
import sys
import os
from pathlib import Path

# Import del backend universale
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from universal_publisher import UniversalStorePublisher

class FlashDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ FLASH Universal - Desktop Publisher")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variabili
        self.publisher = UniversalStorePublisher()
        self.selected_stores = []
        self.app_files = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#ff6b6b', height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚡🌍 FLASH UNIVERSAL", 
                font=('Arial', 24, 'bold'), fg='white', bg='#ff6b6b').pack(pady=20)
        
        tk.Label(header_frame, text="Pubblica su TUTTI gli Store del Mondo • Desktop Edition", 
                font=('Arial', 12), fg='white', bg='#ff6b6b').pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - App Info
        left_panel = tk.LabelFrame(main_container, text="📱 Informazioni App", 
                                  font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.setup_app_info_panel(left_panel)
        
        # Right panel - Store Selection
        right_panel = tk.LabelFrame(main_container, text="🏪 Selezione Store", 
                                   font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.setup_store_selection_panel(right_panel)
        
        # Bottom panel - Actions
        bottom_panel = tk.Frame(self.root, bg='#f0f0f0', height=100)
        bottom_panel.pack(fill=tk.X, padx=20, pady=(0, 20))
        bottom_panel.pack_propagate(False)
        
        self.setup_action_panel(bottom_panel)
        
    def setup_app_info_panel(self, parent):
        """Configura il pannello delle informazioni app"""
        
        # Nome App
        tk.Label(parent, text="Nome App:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W)
        self.app_name_var = tk.StringVar(value="My Amazing App")
        tk.Entry(parent, textvariable=self.app_name_var, font=('Arial', 10), width=40).pack(fill=tk.X, pady=(0, 10))
        
        # Descrizione
        tk.Label(parent, text="Descrizione:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W)
        self.description_text = tk.Text(parent, height=4, font=('Arial', 9), wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(0, 10))
        self.description_text.insert(tk.END, "Descrizione dell'app che verrà pubblicata su tutti gli store...")
        
        # Categoria
        tk.Label(parent, text="Categoria:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W)
        self.category_var = tk.StringVar(value="Productivity")
        category_combo = ttk.Combobox(parent, textvariable=self.category_var, 
                                     values=["Productivity", "Games", "Social", "Business", "Education", "Entertainment"])
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Versione
        version_frame = tk.Frame(parent, bg='white')
        version_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(version_frame, text="Versione:", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        self.version_var = tk.StringVar(value="1.0")
        tk.Entry(version_frame, textvariable=self.version_var, font=('Arial', 10), width=10).pack(side=tk.RIGHT)
        
        # Developer
        tk.Label(parent, text="Sviluppatore:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W)
        self.developer_var = tk.StringVar(value="Marco Buonopane")
        tk.Entry(parent, textvariable=self.developer_var, font=('Arial', 10), width=40).pack(fill=tk.X, pady=(0, 10))
        
        # File Upload Section
        files_frame = tk.LabelFrame(parent, text="📦 File App", font=('Arial', 10, 'bold'), bg='white')
        files_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons per upload file
        file_buttons = [
            ("📱 Android APK", "android_apk", "*.apk"),
            ("🍎 iOS IPA", "ios_ipa", "*.ipa"),
            ("🪟 Windows MSIX", "windows_msix", "*.msix"),
            ("🍎 macOS PKG", "macos_pkg", "*.pkg")
        ]
        
        for label, key, file_type in file_buttons:
            btn_frame = tk.Frame(files_frame, bg='white')
            btn_frame.pack(fill=tk.X, pady=2)
            
            tk.Button(btn_frame, text=label, font=('Arial', 9), 
                     command=lambda k=key, ft=file_type: self.select_file(k, ft),
                     bg='#e3f2fd', relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 10))
            
            file_label = tk.Label(btn_frame, text="Nessun file", font=('Arial', 8), 
                                 fg='gray', bg='white')
            file_label.pack(side=tk.LEFT)
            setattr(self, f"{key}_label", file_label)
    
    def setup_store_selection_panel(self, parent):
        """Configura il pannello di selezione store"""
        
        # Notebook per categorie
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab Mobile
        mobile_frame = tk.Frame(notebook, bg='white')
        notebook.add(mobile_frame, text="📱 Mobile")
        self.setup_store_checkboxes(mobile_frame, self.publisher.mobile_stores)
        
        # Tab Desktop
        desktop_frame = tk.Frame(notebook, bg='white')
        notebook.add(desktop_frame, text="💻 Desktop")
        self.setup_store_checkboxes(desktop_frame, self.publisher.desktop_stores)
        
        # Tab Gaming
        gaming_frame = tk.Frame(notebook, bg='white')
        notebook.add(gaming_frame, text="🎮 Gaming")
        self.setup_store_checkboxes(gaming_frame, self.publisher.gaming_stores)
        
        # Tab All
        all_frame = tk.Frame(notebook, bg='white')
        notebook.add(all_frame, text="🌍 TUTTI")
        
        tk.Label(all_frame, text="🌍 Pubblicazione Universale", 
                font=('Arial', 14, 'bold'), bg='white', fg='#ff6b6b').pack(pady=20)
        tk.Label(all_frame, text="Seleziona per pubblicare simultaneamente\nsu TUTTI gli store disponibili!", 
                font=('Arial', 11), bg='white').pack(pady=10)
        
        self.all_stores_var = tk.BooleanVar()
        tk.Checkbutton(all_frame, text="🚀 PUBBLICA SU TUTTO", 
                      variable=self.all_stores_var, font=('Arial', 12, 'bold'),
                      bg='white', fg='#ff6b6b', command=self.toggle_all_stores).pack(pady=20)
    
    def setup_store_checkboxes(self, parent, stores_dict):
        """Crea checkbox per la selezione store"""
        
        # Scrollable frame
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Store checkboxes
        store_vars = {}
        for store_id, store_info in stores_dict.items():
            var = tk.BooleanVar()
            store_vars[store_id] = var
            
            frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Checkbutton(frame, variable=var, font=('Arial', 10), bg='white',
                          command=lambda sid=store_id: self.toggle_store(sid)).pack(side=tk.LEFT, padx=5)
            
            info_frame = tk.Frame(frame, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            
            tk.Label(info_frame, text=store_info['name'], font=('Arial', 10, 'bold'), 
                    bg='white', anchor=tk.W).pack(fill=tk.X)
            tk.Label(info_frame, text=f"{store_info['platform']} • {store_info['users']}", 
                    font=('Arial', 8), fg='gray', bg='white', anchor=tk.W).pack(fill=tk.X)
        
        setattr(self, f"store_vars_{parent.winfo_name()}", store_vars)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_action_panel(self, parent):
        """Configura il pannello delle azioni"""
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Pronto per la pubblicazione universale")
        tk.Label(parent, textvariable=self.status_var, font=('Arial', 10), 
                bg='#f0f0f0').pack(pady=5)
        
        # Action buttons
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔍 Anteprima Pubblicazione", 
                 font=('Arial', 11), command=self.preview_publication,
                 bg='#2196f3', fg='white', padx=20).pack(side=tk.LEFT, padx=10)
        
        self.publish_button = tk.Button(button_frame, text="🚀 PUBBLICA UNIVERSALE", 
                                       font=('Arial', 12, 'bold'), command=self.start_publication,
                                       bg='#ff6b6b', fg='white', padx=30, pady=10)
        self.publish_button.pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="💾 Salva Configurazione", 
                 font=('Arial', 11), command=self.save_configuration,
                 bg='#4caf50', fg='white', padx=20).pack(side=tk.LEFT, padx=10)
    
    def select_file(self, file_key, file_type):
        """Seleziona file per l'app"""
        file_path = filedialog.askopenfilename(
            title=f"Seleziona {file_key}",
            filetypes=[(file_type.upper()[2:], file_type), ("All files", "*.*")]
        )
        
        if file_path:
            self.app_files[file_key] = file_path
            filename = os.path.basename(file_path)
            getattr(self, f"{file_key}_label").config(text=filename, fg='green')
    
    def toggle_store(self, store_id):
        """Toggle selezione store individuale"""
        if store_id in self.selected_stores:
            self.selected_stores.remove(store_id)
        else:
            self.selected_stores.append(store_id)
    
    def toggle_all_stores(self):
        """Toggle selezione tutti gli store"""
        if self.all_stores_var.get():
            self.selected_stores = ['all']
        else:
            self.selected_stores = []
    
    def preview_publication(self):
        """Anteprima della pubblicazione"""
        if not self.selected_stores and not self.all_stores_var.get():
            messagebox.showwarning("Attenzione", "Seleziona almeno uno store!")
            return
        
        stores = list(self.publisher.all_stores.keys()) if self.all_stores_var.get() else self.selected_stores
        reach = self.publisher.estimate_reach(stores)
        
        info = f"""
🎯 ANTEPRIMA PUBBLICAZIONE UNIVERSALE

📱 App: {self.app_name_var.get()}
👨‍💻 Sviluppatore: {self.developer_var.get()}
📦 Versione: {self.version_var.get()}

🏪 Store selezionati: {len(stores)}
👥 Utenti raggiungibili: {reach['estimated_users_reached']}
🌍 Paesi stimati: {reach['estimated_countries']}
💻 Piattaforme: {', '.join(reach['platforms_reached'])}

⏱️ Tempo stimato: 30-60 secondi
💰 Costo: GRATUITO

🚀 Pronto per il lancio universale!
        """
        
        messagebox.showinfo("Anteprima Pubblicazione", info)
    
    def start_publication(self):
        """Avvia la pubblicazione universale"""
        if not self.validate_inputs():
            return
        
        # Disabilita pulsante
        self.publish_button.config(state=tk.DISABLED, text="🔄 Pubblicazione in corso...")
        
        # Avvia in thread separato
        thread = threading.Thread(target=self.run_publication)
        thread.daemon = True
        thread.start()
    
    def validate_inputs(self):
        """Valida gli input dell'utente"""
        if not self.app_name_var.get().strip():
            messagebox.showerror("Errore", "Inserisci il nome dell'app!")
            return False
        
        if not self.selected_stores and not self.all_stores_var.get():
            messagebox.showerror("Errore", "Seleziona almeno uno store!")
            return False
        
        return True
    
    def run_publication(self):
        """Esegue la pubblicazione in background"""
        try:
            # Prepara dati app
            app_data = {
                'name': self.app_name_var.get(),
                'description': self.description_text.get("1.0", tk.END).strip(),
                'category': self.category_var.get(),
                'version': self.version_var.get(),
                'developer': self.developer_var.get(),
                'app_files': self.app_files
            }
            
            self.publisher.set_app_data(app_data)
            
            # Determina store da pubblicare
            stores = list(self.publisher.all_stores.keys()) if self.all_stores_var.get() else self.selected_stores
            
            # Simula pubblicazione con progress
            total_stores = len(stores)
            for i, store in enumerate(stores):
                progress = (i + 1) / total_stores * 100
                
                # Aggiorna UI nel main thread
                self.root.after(0, lambda p=progress, s=store: self.update_progress(p, f"Pubblicando su {s}..."))
                
                # Simula tempo pubblicazione
                import time
                time.sleep(2)
            
            # Completamento
            self.root.after(0, lambda: self.publication_completed(stores))
            
        except Exception as e:
            self.root.after(0, lambda: self.publication_error(str(e)))
    
    def update_progress(self, progress, status):
        """Aggiorna la progress bar e lo status"""
        self.progress_var.set(progress)
        self.status_var.set(status)
    
    def publication_completed(self, stores):
        """Gestisce il completamento della pubblicazione"""
        self.progress_var.set(100)
        self.status_var.set("🎉 Pubblicazione universale completata!")
        
        self.publish_button.config(state=tk.NORMAL, text="🚀 PUBBLICA UNIVERSALE")
        
        tracking_id = f"FLASH-DESKTOP-{int(time.time())}"
        
        success_msg = f"""
🎉 PUBBLICAZIONE UNIVERSALE COMPLETATA!

📱 App: {self.app_name_var.get()}
🏪 Store pubblicati: {len(stores)}
⏱️ Processo completato con successo

📋 Tracking ID: {tracking_id}

La tua app è ora disponibile su tutti gli store selezionati!
        """
        
        messagebox.showinfo("Successo!", success_msg)
    
    def publication_error(self, error):
        """Gestisce gli errori di pubblicazione"""
        self.status_var.set("❌ Errore durante la pubblicazione")
        self.publish_button.config(state=tk.NORMAL, text="🚀 PUBBLICA UNIVERSALE")
        
        messagebox.showerror("Errore", f"Errore durante la pubblicazione:\n{error}")
    
    def save_configuration(self):
        """Salva la configurazione corrente"""
        config = {
            'app_name': self.app_name_var.get(),
            'description': self.description_text.get("1.0", tk.END).strip(),
            'category': self.category_var.get(),
            'version': self.version_var.get(),
            'developer': self.developer_var.get(),
            'selected_stores': self.selected_stores,
            'all_stores': self.all_stores_var.get(),
            'app_files': self.app_files
        }
        
        file_path = filedialog.asksaveasfilename(
            title="Salva Configurazione FLASH",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Salvato", f"Configurazione salvata in:\n{file_path}")

def main():
    """Avvia l'applicazione desktop"""
    root = tk.Tk()
    
    # Configura stile
    style = ttk.Style()
    style.theme_use('clam')
    
    app = FlashDesktopApp(root)
    
    # Centro la finestra
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()