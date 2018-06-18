from conexion.ConeccionMysql import ConeccionMysql
from conexion.ConexionHtml import ConexionHtml
from http import cookies
import cgi,os

form = cgi.FieldStorage()
cuenta="".join(form.getlist("cuenta"))
codigo="".join(form.getlist("codigo"))
monto="".join(form.getlist("monto"))
cuenta_dos="";
cuenta_dos += "".join(form.getlist("cuenta_dos"))
cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
correo = cookie['session'].value
ConeccionMysql.eliminar("icompletas", str(codigo))
usuario=ConeccionMysql.buscar_usuario(correo)
solicitudes=ConexionHtml.html("templates/solicitudes.html",{"solicitudes":str(ConexionHtml.render("usuario","1")),"campos":"<th>Activar</th>"})
usuarios=ConexionHtml.html("templates/solicitudes.html",{"solicitudes":str(ConexionHtml.render("usuario","0")),"campos":"<th>Cuenta</th><th>Tipo</th><th>Saldo</th>"})
reviciones = ConexionHtml.html("templates/revision.html",{"solicitudes":str(ConexionHtml.revision("usuario"))})
print(ConexionHtml.html("templates/index_admin.html", {"cookie": str(usuario[0][0]),"solicitudes":str(solicitudes),"usuarios":str(usuarios),"error":"","revision":reviciones}))
