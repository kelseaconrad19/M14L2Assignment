import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from model import Product as ProductModel, db
from sqlalchemy.orm import Session

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel

class Query(graphene.ObjectType):
    products = graphene.List(Product)

    def resolve_products(self, info): #resolver
        return db.session.execute(db.select(ProductModel)).scalars()

class AddProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)

    movie = graphene.Field(Product)

    def mutate(self, info, name, category, price, quantity):
        with Session(db.engine) as session:
            with session.begin():
                product = ProductModel(name=name, category=category, price=price, quantity=quantity)
                session.add(product)
            session.refresh(product)
            return AddProduct(product=product)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)

    product = graphene.Field(Product)

    def mutate(self, info, name, category, price, quantity, id):
        with Session(db.engine) as session:
            with session.begin():
                product = session.execute(db.select(ProductModel).where(ProductModel.id == id)).scalars().first()
                if product:
                    product.name = name
                    product.category = category
                    product.price = price
                    product.quantity = quantity
                else:
                    return None
            session.refresh(product)
            return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    product = graphene.Field(Product)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                product = session.execute(db.select(ProductModel).where(ProductModel.id == id)).scalars().first()
                if product:
                    session.delete(product)
                else:
                    return None
            session.refresh(product)
            return DeleteProduct(product=product)


class Mutation(graphene.ObjectType):
    add_product = AddProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

