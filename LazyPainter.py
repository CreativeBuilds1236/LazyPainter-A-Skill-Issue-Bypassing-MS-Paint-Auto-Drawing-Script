import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import pyautogui
import threading
import keyboard
import time
import random

# --- SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class LazyPainter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lazy Painter v2.5 - Stable Edition")
        self.geometry("900x650") 
        self.current_image_path = None
        self.is_drawing = False

        # --- 1. THE HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 20))
        self.label = ctk.CTkLabel(self.header_frame, text="LAZY PAINTER", font=("Impact", 50))
        self.label.pack()
        self.sublabel = ctk.CTkLabel(self.header_frame, text="Artistic Talent is a Myth. Automation is Real.", font=("Arial", 14, "italic"), text_color="gray")
        self.sublabel.pack()

        # --- 2. MAIN CONTENT AREA ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=40)
        self.main_frame.grid_columnconfigure(0, weight=1) 
        self.main_frame.grid_columnconfigure(1, weight=1) 

        # LEFT COLUMN
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="n", padx=20)
        self.preview_frame = ctk.CTkFrame(self.left_frame, width=400, height=300, fg_color="#1a1a1a")
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False) 
        self.preview_text = ctk.CTkLabel(self.preview_frame, text="No Image Loaded", font=("Arial", 16))
        self.preview_text.place(relx=0.5, rely=0.5, anchor="center")
        self.upload_btn = ctk.CTkButton(self.left_frame, text="Upload Photo", height=40, font=("Arial", 14, "bold"), fg_color="gray30", command=self.upload_image)
        self.upload_btn.pack(pady=15, fill="x")

        # RIGHT COLUMN
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="n", padx=20, pady=20)
        ctk.CTkLabel(self.right_frame, text="How much effort should I fake?", font=("Arial", 16)).pack(anchor="w", pady=(0, 5))
        self.quality_var = ctk.StringVar(value="Picasso")
        self.quality_menu = ctk.CTkOptionMenu(self.right_frame, values=["Good Enough", "Amazing", "Picasso"], variable=self.quality_var, width=250, height=35)
        self.quality_menu.pack(anchor="w", pady=(0, 20))
        self.start_btn = ctk.CTkButton(self.right_frame, text="START HIJACKING PAINT", font=("Arial", 16, "bold"), height=50, width=250, fg_color="#00C853", hover_color="#009624", command=self.start_drawing_thread)
        self.start_btn.pack(anchor="w", pady=(0, 30))
        
        # SATIRE INSTRUCTIONS
        instruction_text = (
            "Have you ever wanted to draw like Picasso, but you have extensive skill issues?\n"
            "Fear being rejected from art school and accidentally becoming a dictator?\n"
            "Fear not! Lazy Painter is your solution. Why spend decades mastering\n"
            "the brush when you can spend 5s letting a script take your mouse hostage?\n\n"
            "⚠️ MS Paint may crash/freeze. Do not panic, let it load!"
        )
        self.info_label = ctk.CTkLabel(self.right_frame, text=instruction_text, font=("Arial", 12), justify="left", text_color="orange")
        self.info_label.pack(anchor="w")

        self.kill_label = ctk.CTkLabel(self.right_frame, text="HOLD 'ESC' TO EMERGENCY STOP", font=("Arial", 14, "bold"), text_color="red")
        self.kill_label.pack(anchor="w", pady=(20, 0))

        self.status_label = ctk.CTkLabel(self.right_frame, text="Status: Idle", font=("Courier", 14))
        self.status_label.pack(anchor="w", pady=(10, 0))

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_path:
            img = Image.open(file_path)
            preview_w, preview_h = 400, 300
            ratio = min(preview_w/img.width, preview_h/img.height)
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            img_display = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img_display)
            self.preview_text.configure(image=self.tk_img, text="")
            self.current_image_path = file_path
            self.status_label.configure(text="Status: Ready!", text_color="green")

    def start_drawing_thread(self):
        if not self.current_image_path:
            self.status_label.configure(text="Status: ERROR - NO IMAGE", text_color="red")
            return
        self.is_drawing = True
        threading.Thread(target=self.drawing_engine, daemon=True).start()

    def drawing_engine(self):
        # Countdown
        for i in range(5, 0, -1):
            self.status_label.configure(text=f"Status: CLICK PAINT! {i}s", text_color="yellow")
            time.sleep(1)
        
        self.status_label.configure(text="Status: Processing...", text_color="cyan")
        
        # RESOLUTION CAP (600+ causes buffer overflows in Paint)
        quality_map = {"Good Enough": 150, "Amazing": 250, "Picasso": 400}
        target_width = quality_map[self.quality_var.get()]
        
        # Processing
        img = Image.open(self.current_image_path)
        img = ImageEnhance.Contrast(img).enhance(2.0).convert('L')
        aspect = img.height / img.width
        img = img.resize((target_width, int(target_width * aspect)))
        img = img.convert('1', dither=Image.FLOYDSTEINBERG).convert('RGB')
        
        start_x, start_y = pyautogui.position()
        
        # Gather pixels
        pixels = []
        for y in range(img.height):
            for x in range(img.width):
                if img.getpixel((x, y))[0] < 128:
                    pixels.append((x, y))
        
        random.shuffle(pixels) # Shuffle to look more artistic and prevent linear buffer buildup
        total = len(pixels)
        
        # --- THE DOUBLE BRAKE SYSTEM ---
        pyautogui.PAUSE = 0.001 
        
        for i, (px, py) in enumerate(pixels):
            if keyboard.is_pressed('esc') or not self.is_drawing:
                self.is_drawing = False
                break
            
            # 1. Update UI less often (every 500 px) to save CPU
            if i % 500 == 0:
                self.status_label.configure(text=f"Drawing: {i}/{total}")
                # 2. LONG BREATHER for Windows every 500 clicks
                time.sleep(0.1) 

            # SHORT BREATHER every 100 clicks
            elif i % 100 == 0:
                time.sleep(0.01)

            pyautogui.click(start_x + px, start_y + py)

        self.status_label.configure(text="Status: FINISHED!", text_color="#00C853")
        self.is_drawing = False

if __name__ == "__main__":
    app = LazyPainter()
    app.mainloop()