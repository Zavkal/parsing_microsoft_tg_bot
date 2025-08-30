from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from apps.core.database.db_repo.models.base import Base, BaseMixin


class Product(Base, BaseMixin):
    """
    ru-RU en-US es-AR tr-TR en-NG uk-UA en-IN \n -- Полное описание бд при создании
    *1. Уникальный id товара на сайте, \n
    *2. Ссылка на товар, \n
    *3. Название игры, \n
    *4. Окончание скидки, \n
    *5. Поддерживаемые платформы, \n
    *6. Описание, \n
    *7. Короткое описание, \n
    *8. Разработчик, \n
    *9. Публичное название разработчика, \n
    *10. Ссылка на постер товара, \n
    *11. Гейм пассы, \n
    *12. Дата выхода игры, \n
    *13. Возможности игры, \n
    *14. Категории, \n
    *15. Ссылка на трейлер, \n
    *16. Ссылка на скриншоты, \n
    *17. Вес игры
    *18. Русс озвучка, \n
    *19. Русс интерфейс, \n
    *20. Русс субтитры, \n
    *21. Является распродажей, \n
    *22. Основная игра этой dlc, \n
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=False)
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

