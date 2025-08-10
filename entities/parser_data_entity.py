from dataclasses import dataclass


@dataclass
class ProductDataEntity:
    product_id: str
    url_product: str
    game_name: str = None
    end_date_sale: str = None
    device: str | None = None
    description: str | None = None
    short_description: str | None = None
    developer_name: str = None
    publisher_name: str = None
    image_url: str = None
    pass_product_id: str = None
    release_date: str = None
    capabilities: str = None
    category: str = None
    link_video: str = None
    link_screenshot: str = None
    game_weight: int = None
    audio_ru: bool = False
    interface_ru: bool = False
    subtitles_ru: bool = False
    sale_product: bool = False
    dlc: str = None