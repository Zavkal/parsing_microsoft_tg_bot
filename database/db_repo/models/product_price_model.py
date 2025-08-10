from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.db_repo.models.base_model import Base


class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id", ondelete="CASCADE"))
    country_code = Column(String, nullable=False)
    original_price = Column(Float)
    discounted_price = Column(Float)
    discounted_percentage = Column(Float)
    ru_price = Column(Float)

    product = relationship("Product", back_populates="prices")