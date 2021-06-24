from tkinter import *
import math

root = Tk()
top = Frame(root)
top.pack(side='top')

hwtext = Label(top, text='Hello, World! The sine of')
hwtext.pack(side='left')

r = StringVar()
r.set('1.2')
r_entry = Entry(top, width=6, textvariable=r)
r_entry.pack(side='left')
b_entry = Entry(top, width=6, textvariable=r)
b_entry.pack(side='right')

s = StringVar()
def comp_b(event):
    print('hello')

def comp_s(event):
    global s
    s.set('%g' % math.sin(float(r.get()))) # construct string

r_entry.bind('<Return>', comp_s)
b_entry.bind('<Return>', comp_b)

compute = Label(top, text=' equals ')
compute.pack(side='left')

s_label = Label(top, textvariable=s, width=18)
s_label.pack(side='left')

root.mainloop()
