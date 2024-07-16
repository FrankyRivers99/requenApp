import gui
import funciones as df
import tkinter as tk
import xml_funciones as xml_df

# Llamamos a la función para crear la ventana principal
ventana_principal = gui.crear_ventana_principal()

#Declaramos los botonos o funciones que tendra nuestra aplicacion
bttn_buscar_certificados = tk.Button(ventana_principal, text='Buscar certificados vigentes .cer', command= df.buscar_cer_vigentes, width=15, height=3, wraplength=70)
bttn_buscar_certificados.config(bg='#8DFF8B')
bttn_buscar_certificados.place(x=100, y=75) 

bttn_buscar_llaves = tk.Button(ventana_principal, text='Buscar llaves .keys', command=df.buscar_keys, width=15, height=3, wraplength=70)
bttn_buscar_llaves.config(bg='#8DFF8B')
bttn_buscar_llaves.place(x=250, y=75) 

bttn_facturas_emitidas = tk.Button(ventana_principal, text='Simplifacion de facturas xml a excel', command=xml_df.main, width=15, height=3, wraplength=70)
bttn_facturas_emitidas.config(bg='#8DFF8B')
bttn_facturas_emitidas.place(x=400, y=75) 


bttn_consejos = tk.Button(ventana_principal, text='SAT hacks', command=df.hack_secreto, width=15, height=3, wraplength=70)
bttn_consejos.config(bg='#8DFF8B')
bttn_consejos.place(x=150, y=150) 


ventana_principal.mainloop()