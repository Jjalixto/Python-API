from database import cursos

#Función para listar los cursos de un alumno
def listarCursosPorAlumno(codigo,estado,ordenarPorNota):
  listaResultado=[]
  if codigo in cursos:
    listaCursosAlumno=cursos[codigo]
    for curso in listaCursosAlumno:
      if estado=="todos" or curso["estado"]==estado:
        listaResultado.append(curso)
  return listaResultado