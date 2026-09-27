from __future__ import annotations
import os
import hashlib
import io
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import qrcode
from qrcode.image.svg import SvgPathImage

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
def now(): return datetime.now(timezone.utc).isoformat()

SEED = [
 {"id":"GWD-001284","container":"MSKU-784521","category":"Electronics","weight":18400,"truck":"BLA-2045","driver":"Ahmed Khan","destination":"Quetta Dry Port","origin":"Gwadar Port","status":"IN_TRANSIT","seal":"SL-90871","progress":58,"eta":"Today, 18:30","createdAt":"2026-09-27T09:00:00+00:00","events":[{"place":"CP-01 · Pasni","action":"Cargo and vehicle verified","time":"2026-09-27T12:45:00+00:00","by":"Checkpoint Officer","type":"verified"},{"place":"Gwadar Port Gate","action":"Cleared for exit","time":"2026-09-27T10:20:00+00:00","by":"Port Officer","type":"verified"},{"place":"Gwadar Port","action":"Cargo registered and documents approved","time":"2026-09-27T09:00:00+00:00","by":"Admin","type":"created"}]},
 {"id":"GWD-001285","container":"MAEU-339102","category":"Textiles","weight":12150,"truck":"KHI-8821","driver":"Bilal Ahmed","destination":"Karachi Logistics Hub","origin":"Gwadar Port","status":"AT_PORT","seal":"SL-90872","progress":8,"eta":"Tomorrow, 09:15","createdAt":"2026-09-27T10:10:00+00:00","events":[{"place":"Gwadar Port","action":"Cargo registered","time":"2026-09-27T10:10:00+00:00","by":"Admin","type":"created"}]},
 {"id":"GWD-001286","container":"COSU-190443","category":"Machinery","weight":22700,"truck":"ISB-7102","driver":"Usman Ali","destination":"Islamabad Freight Terminal","origin":"Gwadar Port","status":"ALERT","seal":"SL-90873","progress":36,"eta":"Delayed","createdAt":"2026-09-27T08:30:00+00:00","events":[{"place":"CP-02 · Ormara","action":"Vehicle mismatch: expected ISB-7102, scanned ISB-7012","time":"2026-09-27T13:15:00+00:00","by":"Checkpoint Officer","type":"alert"},{"place":"Gwadar Port Gate","action":"Cleared for exit","time":"2026-09-27T09:40:00+00:00","by":"Port Officer","type":"verified"}]}
]

SEED.extend([
 {"id":"GWD-001287","container":"TGHU-552910","category":"Medical supplies","weight":9800,"truck":"QTA-3320","driver":"Sanaullah Baloch","destination":"Quetta Medical Depot","origin":"Gwadar Port","status":"IN_TRANSIT","seal":"SL-90874","progress":76,"eta":"Today, 16:45","createdAt":"2026-09-27T07:45:00+00:00","events":[{"place":"CP-02 · Ormara","action":"Priority medical cargo verified","time":"2026-09-27T13:05:00+00:00","by":"Checkpoint Officer","type":"verified"},{"place":"Gwadar Port Gate","action":"Priority corridor clearance issued","time":"2026-09-27T08:50:00+00:00","by":"Port Officer","type":"verified"}]},
 {"id":"GWD-001288","container":"OOLU-440188","category":"Food & agriculture","weight":16750,"truck":"KHI-4477","driver":"Imran Shah","destination":"Karachi Cold Chain Hub","origin":"Gwadar Port","status":"IN_TRANSIT","seal":"SL-90875","progress":42,"eta":"Tomorrow, 05:20","createdAt":"2026-09-27T11:00:00+00:00","events":[{"place":"CP-01 · Pasni","action":"Temperature and seal verified","time":"2026-09-27T13:30:00+00:00","by":"Checkpoint Officer","type":"verified"},{"place":"Gwadar Port Gate","action":"Cleared for exit","time":"2026-09-27T11:35:00+00:00","by":"Port Officer","type":"verified"}]},
 {"id":"GWD-001289","container":"HLXU-208771","category":"Solar equipment","weight":14200,"truck":"LHR-9082","driver":"Farhan Raza","destination":"Lahore Energy Park","origin":"Gwadar Port","status":"AT_PORT","seal":"SL-90876","progress":4,"eta":"Pending port clearance","createdAt":"2026-09-27T12:20:00+00:00","events":[{"place":"Gwadar Port","action":"Documents approved; awaiting vehicle assignment","time":"2026-09-27T12:20:00+00:00","by":"Admin","type":"created"}]},
 {"id":"GWD-001290","container":"CMAU-763201","category":"Textiles","weight":11350,"truck":"FSD-3014","driver":"Zeeshan Tariq","destination":"Faisalabad Export Zone","origin":"Gwadar Port","status":"IN_TRANSIT","seal":"SL-90877","progress":24,"eta":"Tomorrow, 13:00","createdAt":"2026-09-27T09:50:00+00:00","events":[{"place":"Gwadar Port Gate","action":"Cargo, seal and vehicle verified","time":"2026-09-27T10:30:00+00:00","by":"Port Officer","type":"verified"}]},
 {"id":"GWD-001291","container":"MSCU-619043","category":"Industrial parts","weight":20100,"truck":"MUL-7210","driver":"Arslan Mahmood","destination":"Multan Industrial Estate","origin":"Gwadar Port","status":"ALERT","seal":"SL-90878","progress":61,"eta":"Delayed · review required","createdAt":"2026-09-27T06:55:00+00:00","events":[{"place":"CP-04 · Khuzdar","action":"Security seal mismatch detected","time":"2026-09-27T13:42:00+00:00","by":"Checkpoint Officer","type":"alert"},{"place":"CP-02 · Ormara","action":"Cargo and vehicle verified","time":"2026-09-27T10:55:00+00:00","by":"Checkpoint Officer","type":"verified"}]}
])

def enrich(item):
 item["risk"] = "HIGH" if item["status"] == "ALERT" else "LOW"
 item["integrity"] = 100 if item["status"] != "ALERT" else 72
 for event in item.get("events", []):
  raw=f'{item["id"]}|{event.get("time")}|{event.get("place")}|{event.get("action")}'
  event["proof"]=hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
 return item

class Store:
 def __init__(self):
  self.items=[dict(x,events=[dict(e) for e in x["events"]]) for x in SEED]; self.collection=None; self.client=None
 async def connect(self):
  uri=os.getenv("MONGODB_URL","")
  if not uri or "xxxxx" in uri: return
  try:
   from motor.motor_asyncio import AsyncIOMotorClient
   self.client=AsyncIOMotorClient(uri,serverSelectionTimeoutMS=3500); await self.client.admin.command("ping")
   self.collection=self.client.gwadar_cargo_network.shipments
   if await self.collection.count_documents({}) == 0: await self.collection.insert_many(self.items)
  except Exception as exc: print(f"MongoDB unavailable; using demo memory store: {exc}"); self.collection=None
 async def close(self):
  if self.client: self.client.close()
 async def all(self):
  if self.collection is not None: return await self.collection.find({}, {"_id":0}).sort("createdAt",-1).to_list(200)
  return [enrich(x) for x in self.items]
 async def find(self,cargo_id):
  if self.collection is not None: return await self.collection.find_one({"id":cargo_id.upper()},{"_id":0})
  item=next((x for x in self.items if x["id"]==cargo_id.upper()),None)
  return enrich(item) if item else None
 async def create(self,item):
  if self.collection is not None: await self.collection.insert_one(dict(item))
  else: self.items.insert(0,item)
  return item
 async def save(self,item):
  if self.collection is not None: await self.collection.replace_one({"id":item["id"]},item,upsert=True)

store=Store()
class Hub:
 def __init__(self): self.clients=[]
 async def connect(self,socket): await socket.accept(); self.clients.append(socket)
 async def broadcast(self,event,data):
  for socket in list(self.clients):
   try: await socket.send_json({"type":event,"data":data})
   except Exception:
    if socket in self.clients: self.clients.remove(socket)
hub=Hub()

@asynccontextmanager
async def lifespan(_):
 await store.connect(); yield; await store.close()

app=FastAPI(title="Gwadar Smart Cargo Network",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.middleware("http")
async def fresh_frontend_assets(request:Request,call_next):
 response=await call_next(request)
 if request.url.path.startswith("/static/") and (request.url.path.endswith((".js",".css",".svg",".html"))): response.headers["Cache-Control"]="no-store, no-cache, must-revalidate"
 return response
app.mount("/static",StaticFiles(directory=str(FRONTEND)),name="static")

class CargoCreate(BaseModel):
 container:str=Field(min_length=4,max_length=30); category:str; weight:int=Field(gt=0,le=100000); truck:str=Field(min_length=4,max_length=20); driver:str=Field(min_length=2,max_length=80); destination:str=Field(min_length=2,max_length=120); seal:str=Field(min_length=3,max_length=30)
class Verification(BaseModel):
 cargo_id:str; truck:str; seal:str; place:str; officer:str="Officer"
class DriverReport(BaseModel): message:str=Field(min_length=3,max_length=300)

@app.get("/")
async def home(): return FileResponse(FRONTEND/"index.html")
@app.get("/health")
async def health(): return {"status":"healthy","database":"mongodb" if store.collection is not None else "demo-memory"}
@app.get("/api/qr/{cargo_id}")
async def cargo_qr(cargo_id:str,request:Request):
 item=await store.find(cargo_id)
 if not item: raise HTTPException(404,"Cargo ID not found")
 target=f'{str(request.base_url).rstrip("/")}/static/driver/index.html?cargoId={item["id"]}'
 code=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=8,border=4); code.add_data(target); code.make(fit=True)
 image=code.make_image(image_factory=SvgPathImage); output=io.BytesIO(); image.save(output)
 return Response(output.getvalue(),media_type="image/svg+xml",headers={"Cache-Control":"no-cache"})
@app.get("/api/cargo")
async def cargo_list(): return [enrich(x) for x in await store.all()]
@app.get("/api/cargo/{cargo_id}")
async def cargo_detail(cargo_id:str):
 item=await store.find(cargo_id)
 if not item: raise HTTPException(404,"Cargo ID not found")
 return item
@app.post("/api/cargo",status_code=201)
async def cargo_create(payload:CargoCreate):
 items=await store.all(); next_number=max([int(x["id"].split("-")[-1]) for x in items]+[1283])+1; data=payload.model_dump()
 item={"id":f"GWD-{next_number:06d}","origin":"Gwadar Port","status":"AT_PORT","progress":5,"eta":"Pending port clearance","createdAt":now(),**{**data,"container":data["container"].upper(),"truck":data["truck"].upper(),"seal":data["seal"].upper()},"events":[{"place":"Gwadar Port","action":"Cargo registered and digital pass issued","time":now(),"by":"Admin","type":"created"}]}
 await store.create(item); await hub.broadcast("cargo_created",item); return item
@app.post("/api/verify")
async def verify(payload:Verification):
 item=await store.find(payload.cargo_id)
 if not item: raise HTTPException(404,"Cargo ID not found")
 truck_ok=payload.truck.upper()==item["truck"].upper(); seal_ok=payload.seal.upper()==item["seal"].upper(); verified=truck_ok and seal_ok
 action="Cargo, seal and vehicle verified" if verified else "Verification failed: "+", ".join(x for x,ok in [("vehicle mismatch",truck_ok),("seal mismatch",seal_ok)] if not ok)
 item["status"]="IN_TRANSIT" if verified else "ALERT"; item["progress"]=min(92,int(item.get("progress",0))+(18 if verified else 0)); item["eta"]=item.get("eta") if verified else "Delayed · review required"
 item["events"].insert(0,{"place":payload.place,"action":action,"time":now(),"by":payload.officer,"type":"verified" if verified else "alert"}); await store.save(item)
 result={"verified":verified,"truck_ok":truck_ok,"seal_ok":seal_ok,"cargo":item}; await hub.broadcast("cargo_updated",result); return result
@app.post("/api/cargo/{cargo_id}/report")
async def driver_report(cargo_id:str,payload:DriverReport):
 item=await store.find(cargo_id)
 if not item: raise HTTPException(404,"Cargo ID not found")
 item["status"]="ALERT"; item["events"].insert(0,{"place":"Driver App","action":f"Driver report: {payload.message}","time":now(),"by":item["driver"],"type":"alert"}); await store.save(item); await hub.broadcast("alert_created",item); return item
@app.post("/api/cargo/{cargo_id}/resolve")
async def resolve_alert(cargo_id:str):
 item=await store.find(cargo_id)
 if not item: raise HTTPException(404,"Cargo ID not found")
 item["status"]="IN_TRANSIT"; item["events"].insert(0,{"place":"Control Room","action":"Alert reviewed and resolved","time":now(),"by":"Admin","type":"resolved"}); await store.save(item); await hub.broadcast("cargo_updated",item); return item
@app.get("/api/dashboard")
async def dashboard():
 items=await store.all(); verified=sum(e.get("type")=="verified" for x in items for e in x.get("events",[])); return {"total":len(items),"at_port":sum(x["status"]=="AT_PORT" for x in items),"in_transit":sum(x["status"]=="IN_TRANSIT" for x in items),"alerts":sum(x["status"]=="ALERT" for x in items),"verified_events":verified,"cargo_weight":sum(x.get("weight",0) for x in items),"integrity_rate":round(100*(len(items)-sum(x["status"]=="ALERT" for x in items))/max(len(items),1)),"paper_documents_saved":len(items)*7,"avg_progress":round(sum(x.get("progress",0) for x in items)/max(len(items),1))}
@app.websocket("/ws")
async def websocket_endpoint(socket:WebSocket):
 await hub.connect(socket)
 try:
  while True: await socket.receive_text()
 except WebSocketDisconnect:
  if socket in hub.clients: hub.clients.remove(socket)

if __name__=="__main__":
 import uvicorn
 uvicorn.run(app,host="0.0.0.0",port=int(os.getenv("PORT","8000")))
