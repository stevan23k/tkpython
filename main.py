import tkinter as tk
import pymysql as mysql
from tkinter import messagebox
import customtkinter


def conexion():
    try:
        conexion = mysql.connect(host="bilu4c9xkyxamq80ka98-mysql.services.clever-cloud.com",
                                port=3306,
                                user="u2lwcsolxlcwbrx2",
                                passwd="YwQK77UnN3nJeDBSaDOY",
                                db="bilu4c9xkyxamq80ka98",
                                cursorclass=mysql.cursors.DictCursor
                                ) 
        print("Conexión exitosa")
        return conexion
    except mysql.MySQLError as e:
        print("Error de conexión:", e)
        return None


# consultar reservas de usuarios
def consultarReservas(correo):
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT clientes.nombre, mesas.id_mesa, reservas.fecha, reservas.hora, reservas.nPersonas, clientes.id_cliente, reservas.id_reserva, reservas.estado
                FROM reservas
                LEFT JOIN clientes ON clientes.id_cliente = reservas.id_cliente
                LEFT JOIN mesas ON mesas.id_mesa = reservas.id_mesa
                WHERE clientes.correo = %s
                ORDER BY reservas.fecha DESC, reservas.hora DESC, reservas.estado DESC;
            """, (correo,))

            # Función para cancelar reserva
            def cancelarReserva(id_reserva, ventana, nombre, mesa):
                connection = conexion()
                if connection:
                    try:
                        cursor = connection.cursor()
                        cursor.execute("UPDATE reservas SET estado = false WHERE id_reserva = %s", (id_reserva,))
                        cursor.execute("UPDATE mesas SET ocupado = false WHERE id_mesa = %s", (mesa,))
                        connection.commit()
                        print(f"Reserva con ID {id_reserva} ha sido cancelada.")
                        messagebox.showinfo("Cancelada", f"Reserva cancelada correctamente para {nombre}")
                        ventana.destroy()
                        consultarReservas(correo)  # Refrescar la ventana después de cancelar la reserva
                    except mysql.MySQLError as e:
                        print("Error al cancelar reserva:", e)
                    finally:
                        connection.close()

            resultados = cursor.fetchall()
            if resultados:
                ventana_reserva = customtkinter.CTkToplevel()
                ventana_reserva.title("Lista de Reservas")
                ventana_reserva.geometry("400x600")
                ventana_reserva.grid_columnconfigure(0, weight=1)  # Expandir tarjetas en toda la ventana

                for i, row in enumerate(resultados):
                    # Crear una tarjeta para cada reserva
                    card_frame = customtkinter.CTkFrame(ventana_reserva)
                    card_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

                    # Texto detallado de la reserva
                    reserva_texto = (
                        f"ID Reserva: {row['id_reserva']}\n"
                        f"Cliente: {row['nombre']}\n"
                        f"Número de Mesa: {row['id_mesa']}\n"
                        f"Fecha: {row['fecha']}\n"
                        f"Hora: {row['hora']}\n"
                        f"Número de Personas: {row['nPersonas']}\n"
                        f"Estado: {'Activa' if row['estado'] else 'Cancelada'}"
                    )
                    label_reserva = customtkinter.CTkLabel(card_frame, text=reserva_texto, justify="left")
                    label_reserva.grid(row=0, column=0, padx=10, pady=5, sticky="w")

                    # Botón para cancelar la reserva si está activa
                    if row['estado'] == True:
                        btn_cancelar = customtkinter.CTkButton(
                            card_frame, text="Cancelar Reserva",
                            fg_color="red",
                            hover_color="darkred",
                            command=lambda r=row: cancelarReserva(r['id_reserva'], ventana_reserva, r['nombre'], r['id_mesa'])
                        )
                        btn_cancelar.grid(row=0, column=1, padx=10, pady=5)

            else:
                print("No se encontraron registros.")

        except mysql.MySQLError as e:
            print("Error al consultar datos:", e)
        finally:
            connection.close()

# consultar todas las reservas
def consultarReservasAll():
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT clientes.nombre, mesas.id_mesa, reservas.fecha, reservas.hora, reservas.nPersonas, clientes.id_cliente, reservas.id_reserva, reservas.estado
                FROM reservas
                LEFT JOIN clientes ON clientes.id_cliente = reservas.id_cliente
                LEFT JOIN mesas ON mesas.id_mesa = reservas.id_mesa
                ORDER BY reservas.fecha DESC, reservas.hora DESC, reservas.estado DESC;
            """)

            # Función para cancelar reserva
            def cancelarReserva(id_reserva, ventana, nombre, mesa):
                connection = conexion()
                if connection:
                    try:
                        cursor = connection.cursor()
                        cursor.execute("UPDATE reservas SET estado = false WHERE id_reserva = %s", (id_reserva,))
                        cursor.execute("UPDATE mesas SET ocupado = false WHERE id_mesa = %s", (mesa,))
                        connection.commit()
                        print(f"Reserva con ID {id_reserva} ha sido cancelada.")
                        messagebox.showinfo("Cancelada", f"Reserva cancelada correctamente para {nombre}")
                        ventana.destroy()
                        consultarReservasAll()  # Refrescar la ventana después de cancelar la reserva
                    except mysql.MySQLError as e:
                        print("Error al cancelar reserva:", e)
                    finally:
                        connection.close()

            resultados = cursor.fetchall()
            if resultados:
                ventana_reserva = customtkinter.CTkToplevel()
                ventana_reserva.title("Lista de Reservas")
                ventana_reserva.geometry("400x600")
                ventana_reserva.grid_columnconfigure(0, weight=1)  # Expandir tarjetas en toda la ventana

                for i, row in enumerate(resultados):
                    # Crear una tarjeta para cada reserva
                    card_frame = customtkinter.CTkFrame(ventana_reserva)
                    card_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

                    # Texto detallado de la reserva
                    reserva_texto = (
                        f"ID Reserva: {row['id_reserva']}\n"
                        f"Cliente: {row['nombre']}\n"
                        f"Número de Mesa: {row['id_mesa']}\n"
                        f"Fecha: {row['fecha']}\n"
                        f"Hora: {row['hora']}\n"
                        f"Número de Personas: {row['nPersonas']}\n"
                        f"Estado: {'Activa' if row['estado'] else 'Cancelada'}"
                    )
                    label_reserva = customtkinter.CTkLabel(card_frame, text=reserva_texto, justify="left")
                    label_reserva.grid(row=0, column=0, padx=10, pady=5, sticky="w")

                    # Botón para cancelar la reserva si está activa
                    if row['estado'] == True:
                        btn_cancelar = customtkinter.CTkButton(
                            card_frame, text="Cancelar Reserva",
                            fg_color="red",
                            hover_color="darkred",
                            command=lambda r=row: cancelarReserva(r['id_reserva'], ventana_reserva, r['nombre'], r['id_mesa'])
                        )
                        btn_cancelar.grid(row=0, column=1, padx=10, pady=5)

            else:
                print("No se encontraron registros.")

        except mysql.MySQLError as e:
            print("Error al consultar datos:", e)
        finally:
            connection.close()

# consultar clientes
def consultar_clientes():
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes")
            resultados = cursor.fetchall()
            if resultados:
                # Crear una nueva ventana para mostrar los clientes
                global ventana_clientes
                ventana_clientes = customtkinter.CTkToplevel()
                ventana_clientes.title("Lista de Clientes")
                ventana_clientes.geometry("600x600")
                ventana_clientes.grid_columnconfigure(0, weight=1)  # Expandir tarjetas en toda la ventana

                # Crear tarjeta para cada cliente
                for i, row in enumerate(resultados):
                    # Crear un frame para cada tarjeta de cliente
                    card_frame = customtkinter.CTkFrame(ventana_clientes)
                    card_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

                    # Mostrar la información del cliente en la tarjeta
                    cliente_texto = (
                        f"ID Cliente: {row['id_cliente']}\n"
                        f"Nombre: {row['nombre']}\n"
                        f"Correo: {row['correo']}\n"
                        f"Teléfono: {row['telefono']}"
                    )
                    label_cliente = customtkinter.CTkLabel(card_frame, text=cliente_texto, justify="left")
                    label_cliente.grid(row=0, column=0, padx=10, pady=5, sticky="w")

                    # Botón de Editar
                    btn_editar = customtkinter.CTkButton(
                        card_frame, text="Editar", command=lambda r=row: editar_cliente(r['id_cliente'])
                    )
                    btn_editar.grid(row=0, column=1, padx=10, pady=5)

                    # Botón de Eliminar
                    btn_eliminar = customtkinter.CTkButton(
                        card_frame, text="Eliminar", fg_color="red", hover_color="darkred",
                        command=lambda r=row: eliminar_cliente(r['id_cliente'], ventana_clientes)
                    )
                    btn_eliminar.grid(row=0, column=2, padx=10, pady=5)

            else:
                print("No se encontraron registros.")

        except mysql.MySQLError as e:
            print("Error al consultar datos:", e)
        finally:
            connection.close()
# Función para editar un cliente
def editar_cliente(id_cliente):
    ventana_clientes.destroy()
    def guardar_cliente(id_cliente, nombre, correo, telefono, ventana):
        connection = conexion()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE clientes SET nombre = %s, correo = %s, telefono = %s WHERE id_cliente = %s", (nombre, correo, telefono, id_cliente))
                connection.commit()
                print(f"Cliente con ID {id_cliente} actualizado.")
                
                ventana.destroy()
                ventana_clientes.destroy()
                consultar_clientes()

                messagebox.showinfo("Guardado", "Cliente actualizado correctamente")
                ventana_editar.destroy()

            except mysql.MySQLError as e:
                print("Error al editar cliente:", e)
            finally:
                connection.close()

    print(f"Editar cliente con ID: {id_cliente}") 
    connection = conexion()
    if connection:
        try:
            ventana_editar = customtkinter.CTkToplevel()
            ventana_editar.title("Editar Cliente")
            ventana_editar.geometry("1000x400")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
            cliente = cursor.fetchone()
            if cliente:
                label_nombre = customtkinter.CTkLabel(ventana_editar, text="Nombre:")
                label_nombre.pack(pady=5)
                entry_nombre = customtkinter.CTkEntry(ventana_editar)
                entry_nombre.insert(0, cliente['nombre'])
                entry_nombre.pack(pady=5)

                label_correo = customtkinter.CTkLabel(ventana_editar, text="Correo:")
                label_correo.pack(pady=5)
                entry_correo = customtkinter.CTkEntry(ventana_editar)
                entry_correo.insert(0, cliente['correo'])
                entry_correo.pack(pady=5)
                
                label_telefono = customtkinter.CTkLabel(ventana_editar, text="Telefono:")
                label_telefono.pack(pady=5)
                entry_telefono = customtkinter.CTkEntry(ventana_editar)
                entry_telefono.insert(0, cliente['telefono'])
                entry_telefono.pack(pady=5)

                # Botón de Guardar
                boton_editar = customtkinter.CTkButton(ventana_editar, text="Guardar", command=lambda: guardar_cliente(id_cliente, entry_nombre.get(), entry_correo.get(), entry_telefono.get(), ventana_editar))
                boton_editar.pack(pady=10)
                # Botón de Cancelar
                boton_cancelar = customtkinter.CTkButton(ventana_editar, text="Cancelar", command=ventana_editar.destroy)
                boton_cancelar.pack(padx=10)
        except mysql.MySQLError as e:
            print("Error al editar cliente:", e)                
    
# Función para eliminar un cliente
def eliminar_cliente(id_cliente, ventana):
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            connection.commit()
            print(f"Cliente con ID {id_cliente} eliminado.")
            # Cierra y vuelve a abrir la ventana para refrescar la lista
            ventana.destroy()
            consultar_clientes()
        except mysql.MySQLError as e:
            print("Error al eliminar cliente:", e)
        finally:
            connection.close()

# agregar clientes 
def agregarClientes():
    ventanna_agregar = customtkinter.CTkToplevel() 
    ventanna_agregar.title("Agregar Cliente")
    ventanna_agregar.geometry("1000x400")

    label_nombre = customtkinter.CTkLabel(ventanna_agregar, text="Nombre:")
    label_nombre.pack(pady=5)
    entry_nombre = customtkinter.CTkEntry(ventanna_agregar)
    entry_nombre.pack(pady=5)
    
    label_correo = customtkinter.CTkLabel(ventanna_agregar, text="Correo:")
    label_correo.pack(pady=5)
    entry_correo = customtkinter.CTkEntry(ventanna_agregar)
    entry_correo.pack(pady=5)
    
    label_telefono = customtkinter.CTkLabel(ventanna_agregar, text="Telefono:")
    label_telefono.pack(pady=5)
    entry_telefono = customtkinter.CTkEntry(ventanna_agregar)
    entry_telefono.pack(pady=5)
    
    def insertar_datos():
        connection = conexion()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s)", (entry_nombre.get(), entry_correo.get(), entry_telefono.get()))
                connection.commit()
                print("Cliente insertado correctamente.")
                messagebox.showinfo("Guardado", "Cliente insertado correctamente")
                ventanna_agregar.destroy()
                consultar_clientes()
            except mysql.MySQLError as e:
                print("Error al insertar datos:", e)
            finally:
                connection.close()
    
    boton_insertar = customtkinter.CTkButton(ventanna_agregar, text="Insertar", command=insertar_datos)
    boton_insertar.pack(pady=10)
    
    boton_cancelar = customtkinter.CTkButton(ventanna_agregar, fg_color="red", text="Cancelar", command=ventanna_agregar.destroy)
    boton_cancelar.pack(pady=10)
    
    

          
# inisiar session
def iniciarSesion(nombre, contraseña, ventana):
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM administradores")
            resultados = cursor.fetchall()
            if resultados:
                for row in resultados:
                    if row['nombre'] == nombre and row['contrasena'] == contraseña:
                        print("Inicio de sesión exitoso")
                        messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
                        ventana.destroy()
                        # abrir ventana de administrador
                        global admin
                        admin = customtkinter.CTkToplevel()
                        admin.title("Administrador")
                        admin.geometry("1000x400") 

                        # agregar clientes
                        label_agregar = customtkinter.CTkLabel(admin, text="Agregar Cliente")
                        label_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="w")
                        boton_agregar = customtkinter.CTkButton(admin, text="Agregar", command=agregarClientes)
                        boton_agregar.grid(row=1, column=0, padx=10, pady=10, sticky="w")

                        # ver todos los clientes
                        label_all_clientes = customtkinter.CTkLabel(admin, text="Ver todos los clientes")
                        label_all_clientes.grid(row=2, column=0, padx=10, pady=10, sticky="w")
                        boton_all_clientes = customtkinter.CTkButton(admin, text="Ver todos los clientes", command=consultar_clientes)
                        boton_all_clientes.grid(row=3, column=0, padx=10, pady=10, sticky="w")

                        # crear reservas
                        label_reservas = customtkinter.CTkLabel(admin, text="crear reservas")
                        label_reservas.grid(row=0, column=1, padx=10, pady=10, sticky="w")
                        boton_reservas = customtkinter.CTkButton(admin, text="crear",)
                        boton_reservas.grid(row=1, column=1, padx=10, pady=10, sticky="w")
 
                        # ver todas las reservas
                        label_all_reservas = customtkinter.CTkLabel(admin, text="Ver todas las reservas")
                        label_all_reservas.grid(row=0, column=2, padx=10, pady=10, sticky="w")
                        boton_all_reservas = customtkinter.CTkButton(admin, text="Ver todas las reservas", command=consultarReservasAll)
                        boton_all_reservas.grid(row=1, column=2, padx=10, pady=10, sticky="w")

                        # buscar reservas por correo o por fecha
                        label_buscar = customtkinter.CTkLabel(admin, text="Buscar reservas")
                        label_buscar.grid(row=0, column=3, padx=10, pady=10, sticky="w")

                        correo_label = customtkinter.CTkLabel(admin, text="Correo:")
                        correo_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
                        
                        correo_entry = customtkinter.CTkEntry(admin)
                        correo_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

                        fecha_label = customtkinter.CTkLabel(admin, text="Fecha:")
                        fecha_label.grid(row=3, column=3, padx=10, pady=10, sticky="w")

                        fecha_entry = customtkinter.CTkEntry(admin)
                        fecha_entry.grid(row=4, column=3, padx=10, pady=10, sticky="w")

                        boton_buscar = customtkinter.CTkButton(admin, text="Buscar", command=lambda: consultarReservas(correo_entry.get()))
                        boton_buscar.grid(row=5, column=3, padx=10, pady=10, sticky="w")

                    else:
                        print("Inicio de sesión fallido")
                        messagebox.showinfo("Inicio de sesión", "Inicio de sesión fallido")
        except mysql.MySQLError as e:    
            print("Error al iniciar sesión:", e)    


# Configurar la interfaz de usuario
app = customtkinter.CTk()
app.geometry("1000x500")
app.title("Consultar reserva")

# Crear y posicionar los elementos de la interfaz

lable_consulta = customtkinter.CTkLabel(app, text="Consulta de reservas")
lable_consulta.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_correo = customtkinter.CTkLabel(app, text="Correo:")
label_correo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_correo = customtkinter.CTkEntry(app)
entry_correo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

boton_consultar = customtkinter.CTkButton(app, text="Consultar", command=lambda: consultarReservas(entry_correo.get()))
boton_consultar.grid(row=2, column= 1,pady=10)

boton_editar = customtkinter.CTkButton(app, text="Editar", command=consultar_clientes)
boton_editar.grid(row=3, column= 1,pady=10)


label_inicio = customtkinter.CTkLabel(app, text="Inicio de sesión como administrador")
label_inicio.grid(row=0, column=3, padx=(80,10), pady=10, sticky="w")
label_usuario = customtkinter.CTkLabel(app, text="Usuario:")
label_usuario.grid(row=1, column=3, padx=(80,10), pady=10, sticky="w")
lbel_contrseña = customtkinter.CTkLabel(app, text="Contraseña:")
lbel_contrseña.grid(row=2, column=3, padx=(80,10), pady=10, sticky="w")
entry_usuario = customtkinter.CTkEntry(app)
entry_usuario.grid(row=1, column=4,  pady=10, sticky="w")
entry_contraseña = customtkinter.CTkEntry(app)
entry_contraseña.grid(row=2, column=4,  pady=10, sticky="w")
boton_iniciar = customtkinter.CTkButton(app, text="Iniciar sesión", command=lambda: iniciarSesion(entry_usuario.get(), entry_contraseña.get(), app))
boton_iniciar.grid(row=3, column=4, pady=10, sticky="w")




"""
label_nombre = customtkinter.CTkLabel(admin, text="Nombre:")
label_nombre.pack(pady=5)

entry_nombre = customtkinter.CTkEntry(admin)
entry_nombre.pack(pady=5)

label_telefono = customtkinter.CTkLabel(admin, text="Telefono:")
label_telefono.pack(pady=5)

entry_telefono = customtkinter.CTkEntry(admin)
entry_telefono.pack(pady=5)

boton_insertar = customtkinter.CTkButton(admin, text="Insertar", command=insertar_datos)
boton_insertar.pack(pady=10)

btn_mostrar_clientes = customtkinter.CTkButton(admin, text="Mostrar Clientes", command=consultar_datos)
btn_mostrar_clientes.pack(pady=5)
"""

app.mainloop()

