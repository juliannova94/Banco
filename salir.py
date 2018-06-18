from conexion.ConexionHtml import ConexionHtml

print("Content-Type: text/html; charset=utf-8")
print()
diccionario = {"error": ""}
print(ConexionHtml.html("templates/CerrarSesion.html", diccionario))