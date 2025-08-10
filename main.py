from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Gestión de Empresas")

# Modelos
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str

class Cliente(BaseModel):
    id: int
    nombre: str
    direccion: str

class Factura(BaseModel):
    id: int
    cliente_id: int
    monto: float

# Datos en memoria
usuarios_db: List[Usuario] = []
clientes_db: List[Cliente] = []
facturas_db: List[Factura] = []

# Rutas para usuarios
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return usuario

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios_db

# Rutas para clientes
@app.post("/clientes")
def crear_cliente(cliente: Cliente):
    clientes_db.append(cliente)
    return cliente

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return clientes_db

# Rutas para facturas
@app.post("/facturas")
def crear_factura(factura: Factura):
    facturas_db.append(factura)
    return factura

@app.get("/facturas", response_model=List[Factura])
def listar_facturas():
    return facturas_db
