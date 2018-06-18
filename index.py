from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
from http import cookies
import os,cgi

form = cgi.FieldStorage()
pagina="";
pagina += "".join(form.getlist("pagina"))
cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
if('session' in cookie.keys()):
    correo = cookie['session'].value
    usuario = ConeccionMysql.buscar_usuario(str(correo))
    if(str(usuario[0][9])=="CLIENTE"):
        print("Content-Type: text/html; charset=utf-8")
        print()
        transacciones=ConexionHtml.transacciones(str(usuario[0][0]))
        tabla=ConexionHtml.html("templates/transferencias.html",{"datos":transacciones})
        print(ConexionHtml.html("templates/index_cliente.html", {"cookie": str(usuario[0][0]),"tabla":tabla}))
    else:
        solicitudes = ConexionHtml.html("templates/solicitudes.html",
                                        {"solicitudes": str(ConexionHtml.render("usuario", "1")),
                                         "campos": "<th>Activar</th>"})
        usuarios = ConexionHtml.html("templates/solicitudes.html",
                                     {"solicitudes": str(ConexionHtml.render("usuario", "0")),
                                      "campos": "<th>Cuenta</th><th>Tipo</th><th>Saldo</th>"})
        reviciones = ConexionHtml.html("templates/revision.html",
                                       {"solicitudes": str(ConexionHtml.revision("usuario"))})
        print(ConexionHtml.html("templates/index_admin.html",
                                {"cookie": str(usuario[0][0]), "solicitudes": str(solicitudes),
                                 "usuarios": str(usuarios), "error": "","revision":reviciones}))


else:
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(pagina)
    if(len(pagina)==0):
        print(ConexionHtml.html("templates/index.html",{"error":""}))
    else:
        print(ConexionHtml.html("templates/"+str(pagina), {"error":""}))

    #http://librosweb.es/libro/python/capitulo_14/envio_de_e_mail_desde_python.html