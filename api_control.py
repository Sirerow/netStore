from fastapi import FastAPI, Request
import uvicorn
import json
from DBase import DB
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def read_root():
    return json.dumps({"message": "Welcome to the FastAPI server!"})

@app.post("/getAllUsers")
async def getAllUsers():
    users = DB().getAllUsers()
    usersDict = {}
    for user in users:
        id = user[0]
        login = user[1]
        password = user[2]
        status = user[3]
        usersDict[id] = {"login": login, "password": password, "status": status}
    return JSONResponse(content=usersDict)

@app.post("/addUser")
async def addUser(request: Request):
    data = await request.json()
    try:
        login = data.get("login")
        password = data.get("password")
        status = data.get("status")
        if DB().addUser(login,password,status):
            return JSONResponse(content={"Creation":"True"})
        else: return JSONResponse(content={"Creation":"False"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/getUserByLogin")
async def getUserByLogin(request: Request):
    data = await request.json()
    try:
        user=DB().getUserByLogin(data.get("login"))
        userDict={}
        user_id=user[0]
        userDict[user_id]={"login":user[1],"password":user[2],"status":user[3]}
    except:
        return JSONResponse(content="False")
    return JSONResponse(content=userDict)

@app.post("/getUser")
async def getUser(request: Request):
    data = await request.json()
    try:
        user=DB().getUser(data.get("login"), data.get("password"))
        userDict={}
        user_id=user[0]
        userDict[user_id]={"login":user[1],"password":user[2],"status":user[3]}
    except:
        return JSONResponse(content="False")
    return JSONResponse(content=userDict)

@app.post("/getAllTypes")
async def getAllTypes():
    types = DB().getAllTypes()
    typesDict = {}
    for type in types:
        id = type[0]
        name = type[1]
        typesDict[id] = {"name": name}
    return JSONResponse(content=typesDict)

@app.post("/addType")
async def addType(request: Request):
    data = await request.json()
    try:
        name = data.get("name")
        if DB().addType(name):
            return JSONResponse(content={"Creation":"True"})
        else: return JSONResponse(content={"Creation":"False"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/getTypeIdByName")
async def getTypeIdByName(request: Request):
    data = await request.json()
    try:
        type_id=DB().getTypeIdByName(data.get("type_name"))
        if type_id==False:return JSONResponse(content="False")
        typeDict={}
        typeDict[data.get("type_name")]={"type_id":type_id}
    except:
        return JSONResponse(content="False")
    return JSONResponse(content=typeDict)

@app.post("/addProduct")
async def addProduct(request: Request):
    data = await request.json()
    try:
        type1 = data.get("type")
        name = data.get("name")
        about = data.get("about")
        price = data.get("price")
        picture = data.get("picture")
        if DB().addProduct(type1, name, about, price, picture):
            return JSONResponse(content={"Creation":"True"})
        else: return JSONResponse(content={"Creation":"False"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/changeProduct")
async def changeProduct(request: Request):
    data = await request.json()
    try:
        id_product = data.get("id_product")
        new_price = data.get("new_price")
        if DB().changeProduct(id_product, new_price):
            return JSONResponse(content={"Edition":"True"})
        else: return JSONResponse(content={"Edition":"False"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/getAllProducts")
async def getAllProducts():
    products = DB().getAllProducts()
    productsDict = {}
    for product in products:
        id_product = product[0]
        id_type = product[1]
        name = product[2]
        price = product[3]
        picture = product[4]
        productsDict[id_product] = {"id_type": id_type,"name": name,"price": price,"picture": picture}
    return JSONResponse(content=productsDict)

@app.post("/addReview")
async def addReview(request: Request):
    data = await request.json()
    try:
        id_user = data.get("id_user")
        text = data.get("text")
        DB().addReview(id_user,text)
        return JSONResponse(content={"Creation":"True"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/addReview")
async def addReview(request: Request):
    data = await request.json()
    try:
        id_review = data.get("id_review")
        DB().deleteReview(id_review)
        return JSONResponse(content={"Delete":"True"})
    except:
        return JSONResponse(content="Fatal Error")

@app.post("/getAllReviews")
async def getAllReviews():
    reviews = DB().getAllReviews()
    reviewsDict = {}
    for review in reviews:
        id_review = review[0]
        id_user = review[1]
        text = review[2]
        reviewsDict[id_review] = {"id_user": id_user,"text": text}
    return JSONResponse(content=reviewsDict)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)