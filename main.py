import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi import Depends
from schemas import ProductCreate, Product
import db
import models

app = FastAPI(title="iPavlov test task")


def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_product_by_id(id_: int, session: Session):
    return session.query(models.Product).get(id_)


@app.post(
    "/products/",
    response_model=Product,
)
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    new_product = models.Product(name=product.name, price=product.price)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@app.put(
    "/products/{id_}",
    response_model=Product,
)
async def update_product(product: ProductCreate, id_: int, session: Session = Depends(get_session)):
    db_product = get_product_by_id(id_, session)

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.commit()
    session.refresh(db_product)

    return db_product


@app.get(
    "/products/{id_}",
    response_model=Product,
)
async def get_product(id_: int, session: Session = Depends(get_session)):
    return get_product_by_id(id_, session)


@app.get("/products/")
async def get_products_list(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.query(models.Product).offset(offset).limit(limit).all()


if __name__ == "__main__":

    table = models.Product.__table__
    metadata = db.Base.metadata
    metadata.create_all(db.engine)

    uvicorn.run(app, host="0.0.0.0", port=8000)
