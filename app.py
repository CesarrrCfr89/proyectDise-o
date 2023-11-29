from flask import Flask
from flask import render_template, request,redirect
import pymysql
import plotly.express as px
import pandas as pd


app = Flask(__name__)

conn=None


def establecer_conexion():
    global conn
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3305,
            user='root',
            password='12345',  # ¡Asegúrate de que la contraseña sea correcta!
            db='sitio'
        )
        cursor = conn.cursor()
        print('Conexión exitosa')
        return conn, cursor
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None, None


#######################################

def obtener_datos_desde_bd():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3305,
            user='root',
            password='12345',  # ¡Asegúrate de que la contraseña sea correcta!
            db='sitio'
        )

        # Consulta SQL para obtener datos de la tabla 'ingresos_gastos'
        query = "SELECT localidad, poblacion FROM localidad"
        
        # Ejecutar la consulta y obtener los datos en un DataFrame de Pandas
        df = pd.read_sql(query, conn)

        return df

    except Exception as e:
        print(f"Error al obtener datos desde la base de datos: {e}")
    finally:
        if conn:
            conn.close()

##########################################################

def obtener_datos_desde_bd2():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3305,
            user='root',
            password='12345',  # ¡Asegúrate de que la contraseña sea correcta!
            db='sitio'
        )

        # Consulta SQL para obtener datos de la tabla 'ingresos_gastos'
        query = "SELECT municipio, poblacion FROM municipio"
        
        # Ejecutar la consulta y obtener los datos en un DataFrame de Pandas
        df = pd.read_sql(query, conn)

        return df

    except Exception as e:
        print(f"Error al obtener datos desde la base de datos: {e}")
    finally:
        if conn:
            conn.close()

#######################################################


def obtener_datos_desde_bd3():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3305,
            user='root',
            password='12345',  # ¡Asegúrate de que la contraseña sea correcta!
            db='sitio'
        )

        # Consulta SQL para obtener datos de la tabla 'ingresos_gastos'
        query = "SELECT entidad, poblacion FROM entidade"
        
        # Ejecutar la consulta y obtener los datos en un DataFrame de Pandas
        df = pd.read_sql(query, conn)

        return df

    except Exception as e:
        print(f"Error al obtener datos desde la base de datos: {e}")
    finally:
        if conn:
            conn.close()


@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/viviendas')
def viviendas():
    return render_template('sitio/viviendas.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/cerrar')
def mostrar_cerrar():
    return render_template('admin/cerrar.html')


@app.route('/admin/login' , methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form['txtUsuario']
        contrasena = request.form['txtPassword']
        
        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                sql = "SELECT * FROM `usuarios` WHERE `usuario` = %s AND `contrasena` = %s"
                cursor.execute(sql, (usuario, contrasena))
                usuario_encontrado = cursor.fetchone()
                
                if usuario_encontrado:
                    # Iniciar sesión exitosa, redirigir a la página de viviendas
                    return redirect('/admin/viviendas')
                else:
                    # Usuario o contraseña incorrectos, redirigir a la página de login nuevamente
                    return render_template('admin/login.html', mensaje='Usuario o contraseña incorrectos')
            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
            finally:
                cursor.close()
                conn.close()
    return render_template('admin/login.html', mensaje='')

############################################################
@app.route('/admin/cerrar')
def cerrar_sistema():
    # Cerrar la conexión a la base de datos si está abierta
    if 'conn' in globals() and conn is not None:
        conn.close()
        print('Conexión a la base de datos cerrada')

    # Mensaje para indicar que el sistema se ha cerrado
    mensaje = 'Sistema cerrado correctamente. ¡Hasta luego!'
    return render_template('admin/cerrar.html', mensaje=mensaje)

##########################################################################


@app.route('/admin/viviendas')
def admin_viviendas():
    conn, cursor = establecer_conexion()
    datos = []

    if conn is not None and cursor is not None:
        try:
            conn.ping(reconnect=True)  # Intenta reconectar si la conexión se perdió
            print('Conexión exitosa en admin_viviendas')
            
            sql = "SELECT * FROM `viviendas`"
            cursor.execute(sql)
            datos = cursor.fetchall()  # Recupera todos los datos obtenidos de la consulta
            print("Consulta exitosa")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template("admin/viviendas.html", datos=datos)



@app.route('/admin/clientes')
def admin_clientes():
    conn, cursor = establecer_conexion()
    datos = []

    if conn is not None and cursor is not None:
        try:
            conn.ping(reconnect=True)  # Intenta reconectar si la conexión se perdió
            print('Conexión exitosa en admin_clientes')
            
            sql = "SELECT * FROM `clientes`"
            cursor.execute(sql)
            datos = cursor.fetchall()  # Recupera todos los datos obtenidos de la consulta
            print("Consulta exitosa")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

   
     

    return render_template("admin/clientes.html", datos=datos)


@app.route('/admin/clientes/guardar', methods=['POST'])
def admin_clientes_guardar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        _nombre = request.form['txtNombre']
        _sexo = request.form['txtSexo']
        _direccion = request.form['txtDireccion']
        _telefono = request.form['txtTelefono']
        _ciudad = request.form['txtCiudad']
        
        try:
            sql = "INSERT INTO `clientes` (`nombre`, `sexo`, `direccion` , `telefono`,`ciudad`) VALUES (%s, %s, %s,%s ,%s)"
            cursor.execute(sql, (_nombre, _sexo, _direccion,_telefono,_ciudad ))
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()
    

    return redirect('/admin/clientes')



@app.route('/admin/clientes/borrar', methods=['POST'])
def admin_clientes_borrar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        try:
            _id = request.form['txtID']
            sql = "DELETE FROM `clientes` WHERE `id` = %s"
            cursor.execute(sql, (_id,))
            conn.commit()
            print("Cliente eliminado correctamente")
        except Exception as e:
            print(f"Error al eliminar la vivienda: {e}")
        finally:
            cursor.close()
            conn.close()
    
   
    return redirect('/admin/clientes')  # Redirigir de vuelta a la página de viviendas

@app.route('/admin/clientes/editar', methods=['POST'])
def editar_clientes():
    if request.method == 'POST':
        cliente_id = request.form['txtID']
        nuevo_nombre = request.form['nuevoNombre']
        nuevo_sexo = request.form['nuevoSexo']
        nuevo_direccion = request.form['nuevoDireccion']
        nuevo_telefono = request.form['nuevoTelefono']
        nuevo_ciudad = request.form['nuevoCiudad']

        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                # Consulta SQL para actualizar los datos en la base de datos
                sql = "UPDATE clientes SET nombre=%s, sexo=%s , direccion=%s , telefono=%s , ciudad=%s WHERE id=%s"
                cursor.execute(sql, (nuevo_nombre, nuevo_sexo, nuevo_direccion, nuevo_telefono, nuevo_ciudad, cliente_id))
                conn.commit()
                # Actualización exitosa
            except Exception as e:
                print(f"Error al actualizar los datos: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()


    return redirect('/admin/clientes')  # Redirige de vuelta a la página de viviendas después de editar








@app.route('/admin/viviendas/guardar', methods=['POST'])
def admin_viviendas_guardar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        _nombre = request.form['txtNombre']
        _url = request.form['txtLocacion']
        _archivo = request.files['txtImagen']
        
        try:
            sql = "INSERT INTO `viviendas` (`nombre`, `imagen`, `locacion`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (_nombre, _archivo.filename, _url))
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/admin/viviendas')

@app.route('/admin/viviendas/borrar', methods=['POST'])
def admin_viviendas_borrar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        try:
            _id = request.form['txtID']
            sql = "DELETE FROM `viviendas` WHERE `id` = %s"
            cursor.execute(sql, (_id,))
            conn.commit()
            print("Vivienda eliminada correctamente")
        except Exception as e:
            print(f"Error al eliminar la vivienda: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/admin/viviendas')  # Redirigir de vuelta a la página de viviendas


@app.route('/admin/viviendas/editar', methods=['POST'])
def editar_vivienda():
    if request.method == 'POST':
        vivienda_id = request.form['txtID']
        nuevo_nombre = request.form['nuevoNombre']
        nueva_locacion = request.form['nuevaLocacion']

        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                # Consulta SQL para actualizar los datos en la base de datos
                sql = "UPDATE viviendas SET nombre=%s, locacion=%s WHERE id=%s"
                cursor.execute(sql, (nuevo_nombre, nueva_locacion, vivienda_id))
                conn.commit()
                # Actualización exitosa
            except Exception as e:
                print(f"Error al actualizar los datos: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    return redirect('/admin/viviendas')  # Redirige de vuelta a la página de viviendas después de editar


###################################################################

@app.route('/admin/clientesporvi')
def admin_clientesporvi():
    conn, cursor = establecer_conexion()
    datos = []

    if conn is not None and cursor is not None:
        try:
            conn.ping(reconnect=True)  # Intenta reconectar si la conexión se perdió
            print('Conexión exitosa en admin_clientesporvi')
            
            sql = "SELECT * FROM `clientesporvi`"
            cursor.execute(sql)
            datos = cursor.fetchall()  # Recupera todos los datos obtenidos de la consulta
            print("Consulta exitosa")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

   
     

    return render_template("admin/clientesporvi.html", datos=datos)

@app.route('/admin/clientesporvi/guardar', methods=['POST'])
def admin_clientesporvi_guardar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        _tipodevivienda = request.form['txtTipoDeVivienda']
        _habitante = request.form['txtHabitante']
        _cantidad = request.form['txtCantidad']
        _localidad = request.form['txtLocalidad']
      
        try:
            sql = "INSERT INTO `clientesporvi` (`tipovi`, `habitante`, `cantidad`, `locacion`) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (_tipodevivienda, _habitante, _cantidad, _localidad))
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/admin/clientesporvi')

@app.route('/admin/clientesporvi/borrar', methods=['POST'])
def admin_clientesporvi_borrar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        try:
            _id = request.form['txtID']
            sql = "DELETE FROM `clientesporvi` WHERE `id` = %s"
            cursor.execute(sql, (_id,))
            conn.commit()
            print("registro eliminado correctamente")
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")
        finally:
            cursor.close()
            conn.close()
 

    return redirect('/admin/clientesporvi')  # Redirigir de vuelta a la página de viviendas


@app.route('/admin/clientesporvi/editar', methods=['POST'])
def editar_clientesporvi():
    if request.method == 'POST':
        clientesporvi_id = request.form['txtID']
        nuevo_tipovi = request.form['nuevoTipoVi']
        nuevo_habitante = request.form['nuevoHabitante']
        nueva_cantidad= request.form['nuevaCantidad']
        nueva_localidad = request.form['nuevaLocalidad']

        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                # Consulta SQL para actualizar los datos en la base de datos
                sql = "UPDATE clientesporvi SET tipovi=%s, habitante=%s, cantidad=%s, locacion=%s WHERE id=%s"
                cursor.execute(sql, (nuevo_tipovi, nuevo_habitante,  nueva_cantidad, nueva_localidad, clientesporvi_id))
                conn.commit()
                # Actualización exitosa
            except Exception as e:
                print(f"Error al actualizar los datos: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    return redirect('/admin/clientesporvi')  # Redirige de vuelta a la página de viviendas después de editar

 
##########################################################################

@app.route('/admin/actividadeseconomicas')
def admin_actividadeseconomicas():
    conn, cursor = establecer_conexion()
    datos = []

    if conn is not None and cursor is not None:
        try:
            conn.ping(reconnect=True)  # Intenta reconectar si la conexión se perdió
            print('Conexión exitosa en admin_actividadeseconimicas')
            
            sql = "SELECT * FROM `actividadeseconomicas`"
            cursor.execute(sql)
            datos = cursor.fetchall()  # Recupera todos los datos obtenidos de la consulta
            print("Consulta exitosa")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conn.close()
    
  
   
     

    return render_template("admin/actividadeseconomicas.html", datos=datos)


    
@app.route('/admin/actividadeseconomicas/guardar', methods=['POST'])
def admin_actividadeseconomicas_guardar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        _tipovi = request.form['txtTipoVi']
        _acteco = request.form['txtActEco']
        _municipio = request.form['txtMunicipio']
      
        try:
            sql = "INSERT INTO `actividadeseconomicas` (`tipovi`, `acteco`, `municipo`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (_tipovi, _acteco, _municipio))
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/admin/actividadeseconomicas')
    
            

   


@app.route('/admin/actividadeseconomicas/borrar', methods=['POST'])
def admin_actividadeseconomicas_borrar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        try:
            _id = request.form['txtID']
            sql = "DELETE FROM `actividadeseconomicas` WHERE `id` = %s"
            cursor.execute(sql, (_id,))
            conn.commit()
            print("registro eliminado correctamente")
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")
        finally:
            cursor.close()
            conn.close()
 

    return redirect('/admin/actividadeseconomicas')  # Redirigir de vuelta a la página de viviendas



@app.route('/admin/actividadeseconomicas/editar', methods=['POST'])
def editar_actividadeseconomicas():
    if request.method == 'POST':
        actividadeseconomicas_id = request.form['txtID']
        nuevo_tipovi = request.form['nuevoTipoVi']
        nueva_acteconomica= request.form['nuevaActEconomica']
        nueva_municipio = request.form['nuevoMunicipio']

        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                # Consulta SQL para actualizar los datos en la base de datos
                sql = "UPDATE actividadeseconomicas SET tipovi=%s, acteco=%s, municipo=%s WHERE id=%s"
                cursor.execute(sql, (nuevo_tipovi, nueva_acteconomica, nueva_municipio, actividadeseconomicas_id))
                conn.commit()
                # Actualización exitosa
            except Exception as e:
                print(f"Error al actualizar los datos: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    return redirect('/admin/actividadeseconomicas')  # Redirige de vuelta a la página de viviendas después de editar

###############################################################################################

@app.route('/admin/tipodevihab')
def admin_tipodevihab():
    conn, cursor = establecer_conexion()
    datos = []

    if conn is not None and cursor is not None:
        try:
            conn.ping(reconnect=True)  # Intenta reconectar si la conexión se perdió
            print('Conexión exitosa en admin_tipovihab')
            
            sql = "SELECT * FROM `tipodevihab`"
            cursor.execute(sql)
            datos = cursor.fetchall()  # Recupera todos los datos obtenidos de la consulta
            print("Consulta exitosa")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

   
     

    return render_template("admin/tipodevihab.html", datos=datos)

@app.route('/admin/tipodevihab/guardar', methods=['POST'])
def admin_tipodevihab_guardar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        _tipovi = request.form['txtTipoDeVi']
        _personas = request.form['txtPersonas']
        
      
        try:
            sql = "INSERT INTO `tipodevihab` (`tipodevi`, `personas`) VALUES (%s,%s)"
            cursor.execute(sql, (_tipovi, _personas))
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()

    return redirect('/admin/tipodevihab')

@app.route('/admin/tipodevihab/borrar', methods=['POST'])
def admin_tipodevihab_borrar():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        try:
            _id = request.form['txtID']
            sql = "DELETE FROM `tipodevihab` WHERE `id` = %s"
            cursor.execute(sql, (_id,))
            conn.commit()
            print("registro eliminado correctamente")
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")
        finally:
            cursor.close()
            conn.close()
 

    return redirect('/admin/tipodevihab')  # Redirigir de vuelta a la página de viviendas


@app.route('/admin/tipodevihab/editar', methods=['POST'])
def editar_tipodevihab():
    if request.method == 'POST':
        tipodevihab_id = request.form['txtID']
        nuevo_tipodevi = request.form['nuevoTipoDeVi']
        nuevo_personas = request.form['nuevoPersonas']
       
        conn, cursor = establecer_conexion()
        if conn and cursor:
            try:
                # Consulta SQL para actualizar los datos en la base de datos
                sql = "UPDATE tipodevihab SET tipodevi=%s, personas=%s WHERE id=%s"
                cursor.execute(sql, (nuevo_tipodevi, nuevo_personas,  tipodevihab_id))
                conn.commit()
                # Actualización exitosa
            except Exception as e:
                print(f"Error al actualizar los datos: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    return redirect('/admin/tipodevihab')  # Redirige de vuelta a la página de viviendas después de editar

###################################################################################################################

@app.route('/admin/dashboard_localidad')
def visualizacion():
    

    # Crear un DataFrame de Pandas con los datos
    df = obtener_datos_desde_bd()

    # Crear un gráfico de líneas con Plotly Express
    fig = px.line(df, x='localidad', y=['poblacion'], title='Ingresos vs Gastos por Año')
    
    # Convertir el gráfico a HTML para mostrarlo en la plantilla
    graph_html = fig.to_html(full_html=False)

    return render_template('admin/dashboard_localidad.html', graph_html=graph_html)


#################################################################

@app.route('/admin/dashboard_municipio')
def dashboardmunicipio():
    

    # Crear un DataFrame de Pandas con los datos
    df = obtener_datos_desde_bd2()

    # Crear un gráfico de líneas con Plotly Express
    fig = px.line(df, x='municipio', y=['poblacion'], title='Ingresos vs Gastos por Año')
    
    # Convertir el gráfico a HTML para mostrarlo en la plantilla
    graph_html = fig.to_html(full_html=False)

    return render_template('admin/dashboard_municipio.html', graph_html=graph_html)


###############################################

@app.route('/admin/dashboard_entidad')
def dashboardentidad():
    

    # Crear un DataFrame de Pandas con los datos
    df = obtener_datos_desde_bd3()

    # Crear un gráfico de líneas con Plotly Express
    fig = px.line(df, x='entidad', y=['poblacion'], title='Ingresos vs Gastos por Año')
    
    
    # Convertir el gráfico a HTML para mostrarlo en la plantilla
    graph_html = fig.to_html(full_html=False)

    return render_template('admin/dashboard_entidad.html', graph_html=graph_html)



          
    
if __name__ =='__main__':
    app.run(debug=True)