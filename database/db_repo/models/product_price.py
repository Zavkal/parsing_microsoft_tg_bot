from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.db_repo.models.base import Base


class ProductPrice(Base):
    """
        -- Полное описание бд при создании
        *1. Уник айди, \n
        *2. Уникальный id товара на сайте, \n
        *3. Код страны, \n -> ru-RU en-US es-AR tr-TR en-NG uk-UA en-IN
        *4. Ориг прайс, \n
        *5. Скидочный прайс, \n
        *6. % скидки, \n
        *7. Цена в рублях, \n
    """
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id", ondelete="CASCADE"))
    country_code = Column(String, nullable=False)
    original_price = Column(Float)
    discounted_price = Column(Float)
    discounted_percentage = Column(Float)
    ru_price = Column(Float)

    product = relationship("Product", back_populates="prices")