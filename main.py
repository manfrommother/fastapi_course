from fastapi import FastAPI, Query, Body
import uvicorn
app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Moscow", "name": "moscow"},
]

@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None= Query(None, description="Название отеля"),
):
    if id and title:
        return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]
    else:
        return hotels

@app.delete("/hotel/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                   "title": title })
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}")
def update_hotel_info(id: int, title: str = Body(), name: str = Body()):
    global hotels
    for item in hotels:
        if item["id"] == id:
            item["title"] = title
            item["name"] = name
            break

    return {"result": "OK"}

@app.patch("/hotels/{hotel_id}")
def update_hotel_info(id: int, title: str | None = Body(None), name: str | None = Body(None)):
    global hotels
    for item in hotels:
        if item["id"] == id:
            if title:
                item["title"] = title
            if name:
                item["name"] = name
            break



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
