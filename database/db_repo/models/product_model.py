from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from database.db_repo.models.base_model import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, nullable=False)
    url_product = Column(String)
    game_name = Column(String)
    end_date_sale = Column(String)
    device = Column(String)
    description = Column(Text)
    short_description = Column(Text)
    developer_name = Column(String)
    publisher_name = Column(String)
    image_url = Column(String)
    pass_product_id = Column(String)
    release_date = Column(String)
    capabilities = Column(String)
    category = Column(String)
    link_video = Column(String)
    link_screenshot = Column(String)
    game_weight = Column(Integer)
    audio_ru = Column(Boolean)
    interface_ru = Column(Boolean)
    subtitles_ru = Column(Boolean)
    sale_product = Column(Boolean)
    dlc = Column(String)

    prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")
