from conexion.ConexionHtml import ConexionHtml
from conexion.ConeccionMysql import ConeccionMysql
from http import cookies
import os,cgi
from conexion.ConexionArchivo import archivo
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
    print(ConexionHtml.html("templates/htransferencia.html", {"error": "","saldo":saldo,"documento":correo,"cuenta":cuenta}))
else:
    texto = ""
    texto += "".join(form.getlist("texto"))
    print("Content-Type: text/html; charset=utf-8")
    print()
    if (len(texto) == 0):
        codigo = "".join(form.getlist("codigo"))
        dinero = "".join(form.getlist("monto"))
        cuentad = "".join(form.getlist("cuentat"))
        rescuenta=ConeccionMysql.buscar_cuenta(str(cuentad))
        if(len(rescuenta)>0):
            cu=ConeccionMysql.buscar_cuenta(cuenta)
            if(float(saldo)>=float(dinero)):
                transaccion = ConeccionMysql.buscar("transaccion","id",str(codigo))
                if(len(transaccion)>0):
                    if(str(transaccion[0][2])==str(cu[0][0]) and str(transaccion[0][1])==str("1")):
                        saldo=ConeccionMysql.buscar_cuenta(str(cuenta))[0][4]
                        if (float(dinero) <= 1000000):
                            ConeccionMysql.transferencia(str(transaccion[0][0]),dinero,rescuenta[0][0])
                            ConeccionMysql.actualizar_cuenta(str(cuenta), float(dinero), "retirar")
                            ConeccionMysql.actualizar_cuenta(str(cuentad), float(dinero))
                            print(ConexionHtml.html("templates/htransferencia.html",
                                                    {"error": "Transferencia realizada correctamente", "saldo": saldo, "documento": correo,
                                                     "cuenta": cuenta}))
                        else:
                            ConeccionMysql.registrarIcompletas(cuenta, codigo, dinero,cuentad)
                            print(ConexionHtml.html("templates/htransferencia.html",
                                                    {"error": "Transferencia realizada correctamente", "saldo": saldo,
                                                     "documento": correo,
                                                     "cuenta": cuenta}))
                    else:
                        print(ConexionHtml.html("templates/htransferencia.html",
                                                {"error": "Codigo invalido", "saldo": saldo,
                                                 "documento": correo, "cuenta": cuenta}))

                else:
                    print(ConexionHtml.html("templates/htransferencia.html",
                                            {"error": "Codigo invalido", "saldo": saldo,
                                             "documento": correo, "cuenta": cuenta}))

            else:
                print(ConexionHtml.html("templates/htransferencia.html", {"error": "El monto excede el dinero de su cuenta","saldo":saldo,"documento":correo,"cuenta":cuenta}))

        else:
            print(ConexionHtml.html("templates/htransferencia.html",
                                    {"error": "la cuenta destino no existe", "saldo": saldo, "documento": correo,
                                     "cuenta": cuenta}))

    else:
        tex = form['file']
        fn = "sss"
        if (tex.filename):
            fn = os.path.basename(tex.filename)
            open('./archivos/' + fn, 'wb').write(tex.file.read())
            # print("imagen "+fn +"cargarda")
            # print("ocurrio un error")
        print(fn)

        mensaje = archivo.cargarTransferencia("./archivos/"+fn,cuenta,saldo)
        saldo = ConeccionMysql.buscar_cuenta(str(cuenta))[0][4]
        print(ConexionHtml.html("templates/htransferencia.html",
                                {"error": mensaje, "saldo": saldo,
                                 "documento": correo, "cuenta": cuenta}))