from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
from http import cookies
import os,cgi

form = cgi.FieldStorage()
pagina="";
pagina += "".join(form.getlist("pagina"))
cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])

if(len(pagina)==0):
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(ConexionHtml.html("templates/hconsignacion.html", {"error": ""}))
else:
    print("Content-Type: text/html; charset=utf-8")
    print()
    cuenta = "".join(form.getlist("cuenta"))
    dinero = "".join(form.getlist("dinero"))
    cu=ConeccionMysql.buscar_cuenta(cuenta)
    if(len(cu)>0):
        ConeccionMysql.actualizar_cuenta(str(cuenta),float(dinero))
        print(ConexionHtml.html("templates/hconsignacion.html", {"error": "Consignacion realizada correctamente"}))
    else:
        print(ConexionHtml.html("templates/hconsignacion.html", {"error": "La cuenta "+str(cuenta)+" no existe"}))

