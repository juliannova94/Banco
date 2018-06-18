from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
import cgi

form = cgi.FieldStorage()
pagina="";
pagina += "".join(form.getlist("pagina"))
documento = "".join(form.getlist("documento"))
password = "".join(form.getlist("contra"))

print("Content-Type: text/html; charset=utf-8")
print()
print(pagina)
if(len(pagina)==0):
    usuario = ConeccionMysql.iniciarSesion(documento, password,'EMPLEADO')
    print(usuario)
    if (len(usuario)>0):
        solicitudes=ConexionHtml.html("templates/solicitudes.html",{"solicitudes":str(ConexionHtml.render("usuario","1")),"campos":"<th>Activar</th>"})
        usuarios=ConexionHtml.html("templates/solicitudes.html",{"solicitudes":str(ConexionHtml.render("usuario","0")),"campos":"<th>Cuenta</th><th>Tipo</th><th>Saldo</th>"})
        reviciones = ConexionHtml.html("templates/revision.html",{"solicitudes":str(ConexionHtml.revision("usuario"))})
        print(ConexionHtml.html("templates/index_admin.html", {"cookie": str(usuario[0][0]),"solicitudes":str(solicitudes),"usuarios":str(usuarios),"error":"","revision":reviciones}))
    else:
        print(ConexionHtml.html("templates/login_bancario.html", {"error": "Documento o contraseña invalidos"}))
else:
    usuario =ConeccionMysql.iniciarSesion(documento,password)
    print(usuario)
    if(len(usuario)>0):
        if(str(usuario[0][10])=="1"):
            transacciones = ConexionHtml.transacciones(str(usuario[0][0]))
            tabla = ConexionHtml.html("templates/transferencias.html", {"datos": transacciones})
            print(ConexionHtml.html("templates/index_cliente.html", {"cookie": str(usuario[0][0]), "tabla": tabla}))
        else:
            print(ConexionHtml.html("templates/login_cliente.html", {"error": "Esta cuenta de usuario no ha sido validada "}))

    else:
        print(ConexionHtml.html("templates/login_cliente.html", {"error": "Documento o contraseña invalidos"}))


        #http://librosweb.es/libro/python/capitulo_14/envio_de_e_mail_desde_python.html