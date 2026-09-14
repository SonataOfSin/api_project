from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# საბაზისო სქემა საერთო ველებით
class MovieBase(BaseModel):
    title: str
    genre: str
    # წელი უნდა იყოს რეალისტური (მაგ: კინემატოგრაფიის დაწყებიდან დღემდე)
    year: int = Field(..., gt=1880, le=2100)
    # რეიტინგი მკაცრად 0-დან 10-მდე
    rating: float = Field(..., ge=0, le=10)
    description: Optional[str] = None

# სქემა შექმნისთვის (მემკვიდრეობით იღებს MovieBase-ს)
class MovieCreate(MovieBase):
    pass

# სქემა განახლებისთვის (ყველა ველი Optional-ია)
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = Field(None, gt=1880, le=2100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None

# სქემა Response-ისთვის (ამატებს ID-ს)
class MovieResponse(MovieBase):
    id: int

    # Pydantic V2 კონფიგურაცია SQLAlchemy ობიექტების წასაკითხად
    model_config = ConfigDict(from_attributes=True)