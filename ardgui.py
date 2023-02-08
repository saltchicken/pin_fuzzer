import serial, customtkinter, threading, queue

message_queue = queue.Queue()
read_input_queue = queue.Queue()

def serial_loop(stop_event):
    with serial.Serial('COM4', 9600) as ser:
        x = ser.readline()
        print(x.decode())
        buffer = ""
        while not stop_event.is_set():
            try:
                message = message_queue.get(block=False)
                if message:
                    ser.write(message.encode())
            except queue.Empty:
                if ser.in_waiting > 0:
                    buffer += ser.read(ser.in_waiting).decode()
                    lines = buffer.split("\n")
                    for line in lines[:-1]:
                        try:
                            read_input_queue.put_nowait(line)
                        except queue.Full:
                            read_input_queue.get_nowait()
                            read_input_queue.put_nowait(line)
                    buffer = lines[-1]
        ser.close()
        print("Closed Serial")
            


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# label = customtkinter.CTkLabel(master=frame, text="stuff")
# label.pack(pady=12, padx=10)

# entry = customtkinter.CTkEntry(master=frame, placeholder_text="placeholder")
# entry.pack(pady=12, padx=10)

def create_func(i):
    def function(event):
        if str(event.widget).endswith("label"):
            if state[i] == True:
                event.widget.config(background="green")
            else:
                event.widget.config(background="red") 
            state[i] = not state[i]
            message_queue.put(f"{i}-{int(state[i])}")
    return function

global state
state = [False, False, False, False, False, False, False, False]; 

inputGrid = [customtkinter.CTkLabel(frame, text=f"{i+1}", width=30, height=10, bg_color="blue") for i in range(8)]

for i in range(8):
    callback = create_func(i)
    button = customtkinter.CTkLabel(frame, text=f"{i+1}", width=30, height=10, bg_color="green")
    button.bind("<Button-1>", callback)
    button.grid(row=1, column=i)
    inputGrid[i].grid(row=2, column=i)

# checkbox = customtkinter.CTkCheckBox(master=frame, text="Check me")
# checkbox.pack(pady=12, padx=10)

stop_event = threading.Event()
thread = threading.Thread(target=serial_loop, args=(stop_event,))
thread.start()
def read_input_loop():
    input = read_input_queue.get()
    # TODO This is embarassing
    for i, bit in enumerate(input):
        if i > 7:
            break
        if bit == "1":
            inputGrid[i].configure(bg_color="yellow")
        else:
            inputGrid[i].configure(bg_color="blue")

    root.after(10, read_input_loop)
read_input_loop()

def on_closing():
    print("Closing")
    stop_event.set()
    thread.join()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()