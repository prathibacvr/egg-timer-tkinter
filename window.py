import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageOps 
import winsound  # For Windows beep sound
import threading



root = tk.Tk()

def close_window():
    root.destroy()

def show_selection():
    
    ready_frame.place_forget()
    details_frame.place_forget()
    start_frame.place_forget()  # Hide first page
    selection_frame.place(x=0, y=0, width=450, height=450) 

def start_countdown():
    def countdown():
        global countdown_time
        if countdown_time> 0:
            minutes, seconds= divmod(countdown_time, 60)
            timer_label.config(text=f"Time Left: {minutes}:{seconds:02d}")

            countdown_time -=1
            root.after(1000,countdown)
        else:
            # details_frame.lift()
            timer_label.config(text="Time's up!")
            # egg_ready_label.place(x=250, y=400)
            threading.Thread(target=play_beep, daemon=True).start()

    countdown()

def play_beep():
    for _ in range(3):  # Beep 5 times
        winsound.Beep(1000, 500)
    root.after(1000, show_ready_page)

def show_egg_details(egg_type,img_path, time):
    selection_frame.place_forget()
    details_frame.place(x=0,y=0,width=450,height=450)

    selected_img=Image.open(img_path)
    selected_img=selected_img.resize((150,150))
    selected_img=ImageOps.expand(selected_img, border=2, fill="#F62222")
    selected_img=ImageTk.PhotoImage(selected_img)

    image_label.config(image=selected_img)
    image_label.image = selected_img 

    egg_descriptions={
        "Soft Boiled": "> Runny yolk\n> Best with toast\n> Cooking time: 5mins",
        "Medium Boiled": "> Slightly soft yolk\n> Great for salads\n> Cooking time:8mins",
        "Hard Boiled": "> Fully cooked yolk\n> Perfect for sandwiches\n> Cooking time: 10mins",
        "Poached Eggs": "> Soft white\n> Best with hollandaise sauce\n> Cooking time: 3mins",
    }

    egg_desc.set(f"{egg_type} Egg\nTime: {time} minutes")
    details_text.set(egg_descriptions.get(egg_type,"No details available"))

    global countdown_time
    countdown_time= int(time)*60
    timer_label.config(text=f"Time Left: {countdown_time//60}:{countdown_time%60:02d}")
    # start_timer_btn.config(command=start_countdown)
    start_timer_btn.config(command=lambda: start_countdown())
 

root.overrideredirect(True)  
root.geometry("500x590")  
root.title("Egg Timer <3")

root.configure(
    bg="#E9C63D",              
    highlightbackground="#F62222", 
    highlightcolor="#F62222",       
    highlightthickness=5       
)

# Header (Custom Title Bar)
header = tk.Frame(root, bg="#E9C63D", relief="raised")
header.pack(fill="x", side="top")

header_label = tk.Label(header, text="Egg Timer <3", font=("Comic Sans MS", 20), bg="#E9C63D")
header_label.pack(side="left", padx=20, pady=20)

close_btn = tk.Button(header, text="X", font=("Comic Sans MS", 12, "bold"), bg="#F62222", fg="black", command=close_window)
close_btn.pack(side="right", padx=10)

# Content Box (Now with Solid Color, No Image)
content_box = tk.Frame(root, bg="#FCE6C3", highlightbackground="#F62222", highlightthickness=3, width=450, height=450)
content_box.pack(padx=10, pady=20)

# First Page (Start Screen)
start_frame = tk.Frame(content_box, width=450, height=450, bg="#FCE6C3")
start_frame.place(x=0, y=0, width=450, height=450)  

text_label = tk.Label(start_frame, text="Let's time your egg!", font=("Comic Sans MS", 20, "bold"), bg="#FCE6C3")
text_label.place(x=110, y=100)

start_btn = tk.Button(start_frame, text="Start", font=("Comic Sans MS", 14), bg="#F62222", command=show_selection)
start_btn.place(x=190, y=200)

# Second Page (Selection Screen)
selection_frame = tk.Frame(content_box, width=450, height=450, bg="#FCE6C3")  
selection_frame.place_forget()  # Initially hidden

select_label = tk.Label(selection_frame, text="What are you making today?", font=("Comic Sans MS", 14), bg="#FCE6C3")
select_label.place(x=120, y=20)  # Positioned at the top

egg_options =[
    ("Soft Boiled","soft-boiled.jpg","5"),
    ("Medium Boiled", "medium-boiled.jpg", "8"),
    ("Hard Boiled", "hard-boiled.jpg", "10"),
    ("Poached Eggs", "poached eggs.jpg", "3")
]
x_positions=[50,250,50,250]
y_positions=[60,60,260,260]

for i, (name,img,time) in enumerate(egg_options):
    border_color = "#F62222"  
    border_size = 2

    egg_img =Image.open(img)
    egg_img=egg_img.resize((150, 150))
    egg_img = ImageOps.expand(egg_img, border=border_size, fill=border_color)  # Add border
    egg_img = ImageTk.PhotoImage(egg_img)

    btn=tk.Button(selection_frame,image=egg_img, command=lambda n=name, p=img, t=time: show_egg_details(n,p,t))
    btn.image=egg_img
    btn.place(x=x_positions[i],y=y_positions[i])

    lbl= tk.Label(selection_frame, text=name, font=("Comic Sans MS",12,"bold"),bg="#FCE6C3")
    lbl.place(x=x_positions[i]+40,y=y_positions[i]+160)

details_frame=tk.Label(content_box, bg="#FCE6C3")
details_frame.place_forget()

back_btn= tk.Button(details_frame, text="Back to Home", font=("Comic Sans MS",14),bg="#F62222", command=lambda:show_selection())
back_btn.place(x=10, y=10)

image_label= tk.Label(details_frame, bg="#FCE6C3")
image_label.place(x=150,y=50)

timer_label= tk.Label(details_frame, text="Time Left: --",font=("Comic Sans MS", 14, "bold"), bg="#FCE6C3")
timer_label.place(x=250, y=300)
start_timer_btn =tk.Button(details_frame, text="Start Timer", font=("Comic Sans MS",12),bg="#F62222")
start_timer_btn.place(x=250, y=350)


egg_ready_label= tk.Label(details_frame, text="Egg is ready!", font=("Comic Sans MS",14, "bold"), bg="#FCE6C3", fg="red")
egg_ready_label.place_forget()  #Hide initially

egg_desc= tk.StringVar()

details_text= tk.StringVar()

desc_label= tk.Label(details_frame,textvariable=egg_desc, font=("Comic Sans MS",14,"bold"), bg="#FCE6C3")
desc_label.place(x=150, y=230)

details_label= tk.Label(details_frame, textvariable=details_text, font=("Comic Sans MS",12), bg="#FCE6C3", justify="left")
details_label.place(x=30, y=300)


ready_frame=tk.Frame(content_box, width= 450, height=450, bg="#FCE6C3")
ready_label= tk.Label(ready_frame, text="Your egg is ready!", font=("Comic Sans MS",20,"bold"),bg="#FCE6C3",fg="green")
ready_label.place(x=120, y=150)

back_btn= tk.Button(ready_frame, text="Back to Home", font=("Comic Sans MS",14),bg="#F62222", command=lambda:show_selection())
back_btn.place(x=160, y=250)

def show_ready_page():
    details_frame.place_forget()
    ready_frame.place(x=0,y=0, width=450, height=450)


root.mainloop()