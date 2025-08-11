from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID, uuid4
import os

app = FastAPI(title="Gestión Pymes Servicios - Backend")

# Simulación base de datos en memoria
db_usuarios = {}
db_clientes = {}
db_facturas = {}

# Modelos Pydantic
class Usuario(BaseModel):
    id: UUID
    email: EmailStr
    nombre: str
    rol: str
    hashed_password: str

class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str
    password: str
    rol: Optional[str] = "usuario"

class Cliente(BaseModel):
    id: UUID
    nombre: str
    dni_cuit: Optional[str]
    telefono: Optional[str]
    email: Optional[EmailStr]
    direccion: Optional[str]
    condiciones_pago: Optional[str]

class ClienteCreate(BaseModel):
    nombre: str
    dni_cuit: Optional[str]
    telefono: Optional[str]
    email: Optional[EmailStr]
    direccion: Optional[str]
    condiciones_pago: Optional[str]

class Factura(BaseModel):
    id: UUID
    cliente_id: UUID
    tipo: str
    monto: float
    estado: str
    fecha: str

class FacturaCreate(BaseModel):
    cliente_id: UUID
    tipo: str
    monto: float
    fecha: str

# Endpoints usuarios
@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(user: UsuarioCreate):
    if user.email in db_usuarios:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    nuevo_usuario = Usuario(
        id=uuid4(),
        email=user.email,
        nombre=user.nombre,
        rol=user.rol,
        hashed_password=user.password + "_hashed"
    )
    db_usuarios[user.email] = nuevo_usuario
    return nuevo_usuario

@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios():
    return list(db_usuarios.values())

# Endpoints clientes
@app.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente: ClienteCreate):
    cliente_id = uuid4()
    nuevo_cliente = Cliente(id=cliente_id, **cliente.model_dump())
    db_clientes[cliente_id] = nuevo_cliente
    return nuevo_cliente

@app.get("/clientes/", response_model=List[Cliente])
def listar_clientes():
    return list(db_clientes.values())

# Endpoints facturas
@app.post("/facturas/", response_model=Factura)
def crear_factura(factura: FacturaCreate):
    factura_id = uuid4()
    nueva_factura = Factura(id=factura_id, estado="pendiente", **factura.model_dump())
    db_facturas[factura_id] = nueva_factura
    return nueva_factura

@app.get("/facturas/", response_model=List[Factura])
def listar_facturas():
    return list(db_facturas.values())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Usa el puerto de Render o 8000 por defecto
    uvicorn.run(app, host="0.0.0.0", port=port)
