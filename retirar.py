from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
from conexion.ConexionArchivo import archivo
from http import cookies
import os,cgi

form = cgi.FieldStorage()
pagina="";
pagina += "".join(form.getlist("pagina"))
cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
correo = cookie['session'].value
usuario = ConeccionMysql.buscar_usuario(str(correo))
cuenta= ConeccionMysql.buscar("cuenta","usuario_documento",str(correo))
saldo=str(cuenta[0][4])
cuenta= str(cuenta[0][1])

if(len(pagina)==0):
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(ConexionHtml.html("templates/hretiro.html", {"error": "","saldo":saldo,"documento":correo,"cuenta":cuenta}))
else:
    texto=""
    texto += "".join(form.getlist("texto"))
    print("Content-Type: text/html; charset=utf-8")
    print()
    if(len(texto)==0):
        codigo = "".join(form.getlist("codigo"))
        dinero = "".join(form.getlist("monto"))
        cu=ConeccionMysql.buscar_cuenta(cuenta)
        if(float(saldo)>=float(dinero)):
            transaccion = ConeccionMysql.buscar("transaccion","id",str(codigo))
            if(len(transaccion)>0):

                if(str(transaccion[0][2])==str(cu[0][0]) and str(transaccion[0][1])==str("1")):
                    saldo=ConeccionMysql.buscar_cuenta(str(cuenta))[0][4]
                    if(float(dinero)<=1000000):
                        ConeccionMysql.actualizar_cuenta(str(cuenta), float(dinero), "retirar")
                        ConeccionMysql.actualizar_transaccion(str(transaccion[0][0]),dinero)
                        print(ConexionHtml.html("templates/hretiro.html",
                                                {"error": "Retiro realizado correctamente", "saldo": saldo, "documento": correo,
                                                 "cuenta": cuenta}))
                    else:
                        ConeccionMysql.registrarIcompletas(cuenta,codigo,dinero)
                        print(ConexionHtml.html("templates/hretiro.html",
                                                {"error": "Retiro enviado a revision", "saldo": saldo,
                                                 "documento": correo,
                                                 "cuenta": cuenta}))
                else:
                    print(ConexionHtml.html("templates/hretiro.html",
                                            {"error": "Codigo invalido", "saldo": saldo,
                                             "documento": correo, "cuenta": cuenta}))

            else:
                print(ConexionHtml.html("templates/hretiro.html",
                                        {"error": "Codigo invalido", "saldo": saldo,
                                         "documento": correo, "cuenta": cuenta}))

        else:
            print(ConexionHtml.html("templates/hretiro.html", {"error": "El monto excede el dinero de su cuenta","saldo":saldo,"documento":correo,"cuenta":cuenta}))

    else:
        tex = form['file']
        fn = "sss"
        if (tex.filename):
            fn = os.path.basename(tex.filename)
            open('./archivos/' + fn, 'wb').write(tex.file.read())
            # print("imagen "+fn +"cargarda")
            # print("ocurrio un error")
        print(fn)

        mensaje = archivo.cargarTransaccion("./archivos/"+fn,cuenta,saldo)
        saldo = ConeccionMysql.buscar_cuenta(str(cuenta))[0][4]
        print(ConexionHtml.html("templates/hretiro.html",
                                {"error": mensaje, "saldo": saldo,
                                 "documento": correo, "cuenta": cuenta}))