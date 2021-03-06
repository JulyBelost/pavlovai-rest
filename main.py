from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi import Depends
from schemas import ProductCreate, Product, ProductUpdate
import db
import models

app = FastAPI(title="iPavlov test task")

metadata = db.Base.metadata
metadata.create_all(db.engine)


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
async def update_product(product: ProductUpdate, id_: int, session: Session = Depends(get_session)):
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


@app.get(
    "/products/",
    response_model=List[Product],
)
async def get_products_list(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.query(models.Product).order_by(models.Product.id.asc()).offset(offset).limit(limit).all()
