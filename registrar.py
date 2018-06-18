from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
import cgi
import random
import os
from http import cookies

form = cgi.FieldStorage()
pagina="";
pagina += "".join(form.getlist("pagina"))
documento = "".join(form.getlist("documento"))
password = "".join(form.getlist("clave"))
nombre = "".join(form.getlist("nombre"))
apellido = "".join(form.getlist("apellido"))
telefono = "".join(form.getlist("telefono"))
direccion = "".join(form.getlist("direccion"))
correo = "".join(form.getlist("correo"))
ciudad = "".join(form.getlist("ciudad"))

usuario = ConeccionMysql.buscar_usuario(correo)
print("Content-Type: text/html; charset=utf-8")
print()
if(str(pagina)=="admin"):
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    sesion = cookie['session'].value
    solicitudes = ConexionHtml.html("templates/solicitudes.html",
                                    {"solicitudes": str(ConexionHtml.render("usuario", "1")),
                                     "campos": "<th>Activar</th>"})
    usuarios = ConexionHtml.html("templates/solicitudes.html",
                                 {"solicitudes": str(ConexionHtml.render("usuario", "0")),
                                  "campos": "<th>Cuenta</th><th>Tipo</th><th>Saldo</th>"})
    var = ""
    if len(usuario) > 0:
        var = "Ya existe un usuario registrado con este correo "
    usuario = ConeccionMysql.buscar_usuario(documento)
    if (str(var) == ""):
        token = "" + str(random.randrange(10)) + "" + str(random.randrange(10)) + "" + str(
            random.randrange(10)) + "" + str(random.randrange(10)) + "" + str(random.randrange(10))
        ConeccionMysql.registrarUsuario(documento, password, nombre, apellido, telefono, direccion, correo, ciudad,
                                        token,'EMPLEADO','1');

        print(ConexionHtml.html("templates/index_admin.html",
                                {"cookie": str(sesion), "solicitudes": str(solicitudes), "usuarios": str(usuarios),"error": "empleado " + str(documento) + " registrado correctamente"}))


    else:
        print(ConexionHtml.html("templates/index_admin.html",
                                {"cookie": str(sesion), "solicitudes": str(solicitudes), "usuarios": str(usuarios),
                                 "error": var}))
else:
    var=""
    if len(usuario)>0:
        var="Ya existe un usuario registrado con este correo "
    usuario = ConeccionMysql.buscar_usuario(documento)
    if len(usuario)>0:
        var="Ya existe un usuario registrado con este documento "

    if(str(var)==""):
        token=""+str(random.randrange(10))+""+str(random.randrange(10))+""+str(random.randrange(10))+""+str(random.randrange(10))+""+str(random.randrange(10))
        ConeccionMysql.registrarUsuario(documento,password,nombre,apellido,telefono,direccion,correo,ciudad,token);
        if(str(pagina)=="empleado"):
            print(ConexionHtml.html("templates/Login_cliente.html", {"error":"cliente "+str(documento)+" registrado correctamente"}))

    else:
        if (str(pagina) == "empleado"):
            print(ConexionHtml.html("templates/Registrar.html",{"error": var}))
    #http://librosweb.es/libro/python/capitulo_14/envio_de_e_mail_desde_python.html