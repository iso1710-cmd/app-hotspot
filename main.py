from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Aquí guardaremos los tickets pendientes temporalmente
tickets_pendientes = []

class Ticket(BaseModel):
    ficha: str
    perfil: str

@app.get("/")
def home():
    return {"mensaje": "Sistema de Cola de Tickets Activo"}

# La App usará esto para ENVIAR el ticket a la cola
@app.post("/crear-ticket")
def crear_ticket(ticket: Ticket):
    # Aquí es donde estaba el error: cambiamos txt por ficha
    tickets_pendientes.append({"name": ticket.ficha, "profile": ticket.perfil})
    return {"status": "En espera", "msg": f"Ticket {ticket.ficha} guardado en la nube"}

# El MikroTik usará esto para RECOGER los tickets
@app.get("/get-tickets")
def get_tickets():
    global tickets_pendientes
    copia_tickets = list(tickets_pendientes)
    tickets_pendientes = [] # Limpiamos la cola después de entregarlos
    return copia_tickets
