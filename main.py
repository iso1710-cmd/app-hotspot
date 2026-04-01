from fastapi import FastAPI
import routeros_api

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Servidor de Tickets Activo"}

@app.post("/crear-ticket")
def crear_ticket(ip: str, puerto: int, user: str, password: str, ficha: str, perfil: str):
    try:
        connection = routeros_api.RouterOsApiPool(
            ip, username=user, password=password, port=puerto, plaintext_login=True
        )
        api = connection.get_api()
        hotspot = api.get_resource('/ip/hotspot/user')
        
        # Crea el usuario en el MikroTik
        hotspot.add(name=ficha, password=ficha, profile=perfil)
        
        connection.disconnect()
        return {"status": "OK", "ticket": ficha}
    except Exception as e:
        return {"status": "Error", "detalle": str(e)}