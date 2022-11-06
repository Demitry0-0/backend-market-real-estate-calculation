import sqlalchemy
from app.models.users import users_table

metadata = sqlalchemy.MetaData()

apartments_table = sqlalchemy.Table(
    "apartments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("address", sqlalchemy.Text(), index=True),
    sqlalchemy.Column("count_rooms", sqlalchemy.Integer()),
    sqlalchemy.Column("floor", sqlalchemy.Text()),
    sqlalchemy.Column("maximum_floor", sqlalchemy.Integer()),
    sqlalchemy.Column("kitchen_area", sqlalchemy.Float()),
    sqlalchemy.Column("apartment_area", sqlalchemy.Float()),
    sqlalchemy.Column("metro_distance_in_minutes", sqlalchemy.Integer()),
    sqlalchemy.Column("is_balcony", sqlalchemy.Boolean()),
    sqlalchemy.Column("wall_material", sqlalchemy.String(20)),
    sqlalchemy.Column("segment", sqlalchemy.String(20)),
    sqlalchemy.Column("condition", sqlalchemy.String(40)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
)


apartments_price_table = sqlalchemy.Table(
    "apartments_price",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("apartment_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("price", sqlalchemy.Integer()),
)