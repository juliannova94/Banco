from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
from conexion.ConeccionEmail import email
import cgi
import os
from http import cookies

form = cgi.FieldStorage()
id = "".join(form.getlist("id"))
numero=""
numero+="".join(form.getlist("numero"))
tipo= "".join(form.getlist("tipo"))
saldo= "".join(form.getlist("saldo"))
cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
correo = cookie['session'].value

print("Content-Type: text/html; charset=utf-8")
print()

if(len(numero)>0):
    solicitudes = ConexionHtml.html("templates/solicitudes.html",
                                    {"solicitudes": str(ConexionHtml.render("usuario", "1")),
                                     "campos": "<th>Activar</th>"})
    usuarios = ConexionHtml.html("templates/solicitudes.html",
                                 {"solicitudes": str(ConexionHtml.render("usuario", "0")),
                                  "campos": "<th>Cuenta</th><th>Tipo</th><th>Saldo</th>"})

    count=ConeccionMysql.buscar_cuenta(str(numero))
    if(len(count)>0):
        print(ConexionHtml.html("templates/index_admin.html",
                                {"cookie": str(correo), "solicitudes": str(solicitudes), "usuarios": str(usuarios),
                                 "error": "Este numero de cuenta ya existe "}))

    else:
        if(float(saldo)>=100000):
                ConeccionMysql.crearCuenta(str(numero),str(tipo),str(id),str(saldo))
                cuenta=ConeccionMysql.buscar_cuenta(str(numero))
                mensaje = ConexionHtml.crearEmail(str(cuenta[0][0]))
                usuario=ConeccionMysql.buscar_usuario(str(id))
                email.enviar(str(usuario[0][6]),str(mensaje))
                ConeccionMysql.actualizar_usuario(str(usuario[0][0]))
                print(ConexionHtml.html("templates/index_admin.html",
                                    {"cookie": str(correo), "solicitudes": str(solicitudes), "usuarios": str(usuarios),"error":"Usuario activado correctamente "}))
        else:
            print(ConexionHtml.html("templates/index_admin.html",
                                    {"cookie": str(correo), "solicitudes": str(solicitudes), "usuarios": str(usuarios),
                                     "error": "El monto inicial de la cuenta debe ser mayor o igual a $100.000 "}))

else:
    print(ConexionHtml.html("templates/cuenta_bancaria.html", {"usuario":str(id)}))

#http://librosweb.es/libro/python/capitulo_14/envio_de_e_mail_desde_python.html