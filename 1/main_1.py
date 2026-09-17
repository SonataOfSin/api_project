from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Product Management API")


@app.get("/products")
def get_products():
    return {
        "status": "success",
        "message": "პროდუქტების სია მიღებულია წარმატებით",
        "data": [
            {"id": 1, "name": "ლეპტოპი", "price": 2500},
            {"id": 2, "name": "ტელეფონი", "price": 1200},
        ],
    }


@app.post("/products")
def create_product():
    return {
        "status": "success",
        "message": "პროდუქტი შეიქმნა წარმატებით",
        "product_id": 3,
    }


@app.put("/products/{product_id}")
def update_product_full(product_id: int):
    return {
        "status": "success",
        "message": f"პროდუქტი ID {product_id}-ით სრულად განახლდა წარმატებით",
    }


@app.patch("/products/{product_id}")
def update_product_partial(product_id: int):
    return {
        "status": "success",
        "message": f"პროდუქტის ID {product_id}-ის მონაცემები ნაწილობრივ განახლდა წარმატებით",
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {
        "status": "success",
        "message": f"პროდუქტი ID {product_id}-ით წაიშალა წარმატებით",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)