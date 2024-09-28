from database import alumnos

#Definicion de la funcion de inicio de sesion
def inicioSesion(codigo,clave):
  if codigo in alumnos:
    diccAlumno=alumnos[codigo]
    claveAlumno=diccAlumno.get("clave")
    if len(claveAlumno)>8 and clave==claveAlumno:
      nombreAlumno=diccAlumno.get("nombre")
      mensaje=f"Inicio de sesión exitoso. Bienvenido {nombreAlumno}"
    else:
      mensaje="Clave incorrecta"
  else:
    mensaje="Usuario no encontrado"
  return mensaje