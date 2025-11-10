import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif

# CustomTkinter theme setup
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")

class HEICConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HEIC → PNG Converter")
        self.geometry("600x420")
        self.resizable(False, False)

        # Title
        self.label_title = ctk.CTkLabel(
            self, text="HEIC → PNG Converter", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.label_title.pack(pady=20)

        # Input folder selection
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(pady=10, fill="x", padx=40)

        self.entry_input = ctk.CTkEntry(self.frame_input, placeholder_text="Select HEIC folder")
        self.entry_input.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        self.button_browse_input = ctk.CTkButton(
            self.frame_input, text="Browse", command=self.select_input_folder
        )
        self.button_browse_input.pack(side="right", padx=(5, 10), pady=10)

        # Output folder selection
        self.frame_output = ctk.CTkFrame(self)
        self.frame_output.pack(pady=10, fill="x", padx=40)

        self.entry_output = ctk.CTkEntry(self.frame_output, placeholder_text="Select PNG output folder (optional)")
        self.entry_output.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        self.button_browse_output = ctk.CTkButton(
            self.frame_output, text="Browse", command=self.select_output_folder
        )
        self.button_browse_output.pack(side="right", padx=(5, 10), pady=10)

        # Convert button
        self.button_convert = ctk.CTkButton(
            self, text="Convert", height=40, command=self.convert_images
        )
        self.button_convert.pack(pady=20)

        # Log textbox
        self.text_log = ctk.CTkTextbox(self, height=120)
        self.text_log.pack(fill="both", padx=40, pady=(10, 20))

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select HEIC folder")
        if folder:
            self.entry_input.delete(0, "end")
            self.entry_input.insert(0, folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select PNG output folder")
        if folder:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, folder)

    def log(self, text):
        self.text_log.insert("end", text + "\n")
        self.text_log.see("end")
        self.update()

    def convert_images(self):
        input_dir = self.entry_input.get().strip()
        output_dir = self.entry_output.get().strip() or input_dir

        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid HEIC folder.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        converted = 0
        skipped = 0

        for filename in os.listdir(input_dir):
            if filename.lower().endswith(".heic"):
                filepath = os.path.join(input_dir, filename)
                new_filename = os.path.splitext(filename)[0] + ".png"
                new_filepath = os.path.join(output_dir, new_filename)

                # Skip if file already exists
                if os.path.exists(new_filepath):
                    skipped += 1
                    self.log(f"⚠️ Skipped (already exists): {new_filename}")
                    continue

                self.log(f"📄 Converting: {filename}")

                try:
                    heif_file = pillow_heif.read_heif(filepath)
                    image = Image.frombytes(
                        heif_file.mode, heif_file.size, heif_file.data, "raw"
                    )
                    image.save(new_filepath, format="PNG")
                    converted += 1
                    self.log(f"✅ Saved: {new_filename}")
                except Exception as e:
                    self.log(f"❌ Error converting {filename}: {e}")

        self.log(f"\n✅ Done! {converted} converted, {skipped} skipped.")
        messagebox.showinfo("Completed", f"{converted} converted, {skipped} skipped.")

# Run the app
if __name__ == "__main__":
    app = HEICConverterApp()
    app.mainloop()
