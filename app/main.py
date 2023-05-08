from fastapi import FastAPI
from .database import engine , SessionLocal
from .routers import user,product,auth,cart,admin,order
from fastapi.middleware import cors 
from . import models




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    middleware_class= cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"messge":"Hello World Nice To meet Ya"}