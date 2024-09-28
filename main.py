from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from database import alumnos 
from functions.iniciarSesion import inicioSesion 
from functions.listarCursosPorAlumno import listarCursosPorAlumno

app = FastAPI()

# Habilitar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen, cámbialo a una lista específica en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Ruta de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del curso Introducción a la programación de Kodytec"}

# Función de inicio de sesión
@app.post("/login/")
def login(codigo: str, clave: str):
    message = inicioSesion(codigo, clave)
    if "Inicio de sesión exitoso" in message:
        return {
            "is_success": True,
            "message": message,
            "data": {
                "codigo": codigo,
                "nombre": alumnos[codigo]['nombre'],
                "apellido": alumnos[codigo]['apellido']
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

# Listar cursos por alumno
@app.get("/courses/{studentCode}")
def getCourses(studentCode: str, estado: str = "todos", ordenarPorNota: bool = False):
    # Validar si el código es vacío, nulo o no existe en la lista de alumnos
    if not studentCode or studentCode not in alumnos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El alumno con código {studentCode} no existe"
        )
    
    try:
        cursos = listarCursosPorAlumno(studentCode, estado, ordenarPorNota)
        return {
            "is_success": True,
            "message": "Cursos encontrados: " + str(len(cursos)),
            "data": cursos
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario {studentCode} no existe"
        )

# Manejo de excepciones personalizadas
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "is_success": False,
            "message": exc.detail,
            "data": None
        }
    )