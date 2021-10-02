from tkinter import *
from Processor import *
from Bus import *
from Memory import *

window = Tk()
window.title("Modelo de protocolo para coherencia de caché en sistemas multiprocesador - Esteban Andrés Zúñiga Orozco - 2016146713")

memory = Memory()
bus = Bus(memory)
processors = []

for i in range(4):
    processors.append(Processor(i, bus))

canvas = Canvas(window, width=1000, height=610)
background = PhotoImage(file='Tablero.png')
canvas.create_image(0, 0, image=background, anchor=NW)
canvas.pack()
pause = False
processors_in_step_mode = -1

def pausa():
    global pause, processors_in_step_mode
    for i in range(len(processors)):
        processors[i].pause = not processors[i].pause
        if steps_entry.get() != '':
            processors[i].steps = int(steps_entry.get()) - 1
    if steps_entry.get() != '':
        steps_entry.delete(0, END)
        steps_entry.insert(0, '')
        processors_in_step_mode = len(processors)
        pause_button.configure(state=DISABLED)
        instruction_button.configure(state=DISABLED)
    else:
        if pause:
            pause_button.configure(text='Continuar')
            instruction_button.configure(state=NORMAL)
        else:
            pause_button.configure(text='Pausa')
            instruction_button.configure(state=DISABLED)
        pause = not pause


def next_cicle():
    for i in range(len(processors)):
        processors[i].next = True

def execute_instruction():
    instruction = instruction_entry.get()
    if instruction != '':
        parts = instruction.split(' ')
        index = int(parts[0])
        new_instruction = {'INST': '', 'OP1': '', 'OP2': ''}
        if len(parts) >= 2:
            new_instruction['INST'] = parts[1]
        if len(parts) >= 3:
            new_instruction['OP1'] = parts[2]
        if len(parts) >= 4:
            new_instruction['OP2'] = parts[3]
        processors[index].forced_instruction(new_instruction)
        instruction_entry.delete(0, END)
        instruction_entry.insert(0, '')

steps_entry = Entry(window)
pause_button = Button(window, text='Iniciar', command=pausa, font="Arial 10 bold")
pause_button.place(x=280, y=555)
next_button = Button(window, text='Siguiente ciclo', command=next_cicle, font="Arial 10 bold")
next_button.place(x=360, y=555)
instruction_entry = Entry(window)
instruction_entry.place(x=615, y=525)
instruction_button = Button(window, text='Ejecutar', command=execute_instruction, font="Arial 10 bold")
instruction_button.place(x=590, y=555)
canvas_labels = []

def init_canvas_labels():
    index = 0
    for view_data in memory.view_data(235, 320):
        label_id = canvas.create_text(view_data['x'], view_data['y'], fill="#1FCC1A", font="Arial 10 bold", text=view_data['string'])
        canvas_labels.append(label_id)
    for r in range(1):
        for c in range(-1,3):
            x = 160
            y = 150
            x_offset = 250
            for view_data in processors[index].view_data(x + (c * x_offset), y):
                label_id = canvas.create_text(view_data['x'], view_data['y'], fill="#1FCC1A", font="Arial 10 bold", text=view_data['string'])
                canvas_labels.append(label_id)
            index += 1

def draw():
    index = 0
    global processors_in_step_mode
    label_id = 0
    for view_data in memory.view_data(800, 40):
        canvas.itemconfigure(canvas_labels[label_id], text=view_data['string'])
        label_id += 1
    for r in range(1):
        for c in range(-1,3):
            x = 40
            y = 40
            x_offset = 370
            y_offset = 240
            for view_data in processors[index].view_data(x + (c * x_offset), y + (r * y_offset)):
                canvas.itemconfigure(canvas_labels[label_id], text=view_data['string'])
                label_id += 1
                if processors[index].steps == -1:
                    processors[index].steps = -2
                    processors_in_step_mode -= 1
            index += 1
    if processors_in_step_mode == 0:
        processors_in_step_mode = -1
        pause_button.configure(state=NORMAL)
        instruction_button.configure(state=NORMAL)
    canvas.update()
    canvas.after(500, draw)

def main():
    init_canvas_labels()
    draw()
    for i in range(len(processors)):
        processors[i].start()
    window.mainloop()

if __name__ == "__main__":
    main()