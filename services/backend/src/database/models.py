from tortoise import fields, models
import uuid


# Пример простых кастомных полей для работы с геоданными.
# Здесь они унаследованы от TextField для хранения строкового представления WKT.
# В реальном проекте следует реализовать полноценную сериализацию/десериализацию.
class GeometryField(fields.TextField):
    """ Поле для хранения геометрического объекта (например, полигон в формате WKT). """
    pass


class PointField(fields.TextField):
    """ Поле для хранения точки (например, центральная точка объекта) в формате WKT. """
    pass


class RawAddress(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)  # UUID вместо IntField
    raw_data = fields.JSONField()

    class Meta:
        table = "raw_addresses"

    def __str__(self):
        return f"RawAddress {self.id}"


class AdmArea(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "adm_areas"

    def __str__(self):
        return self.name


class District(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "districts"

    def __str__(self):
        return self.name


class House(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    unom = fields.CharField(max_length=255, unique=True)
    obj_type = fields.CharField(max_length=100)
    full_address = fields.TextField()
    simple_address = fields.TextField()

    adm_area = fields.ForeignKeyField("models.AdmArea", related_name="houses", to_field="id")
    district = fields.ForeignKeyField("models.District", related_name="houses", to_field="id")

    kad_n = fields.TextField()
    kad_zu = fields.TextField(null=True)

    geo_data = GeometryField(null=True)
    geodata_center = PointField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "houses"

    def __str__(self):
        return f"House {self.unom}"


class Role(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    role_name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "roles"

    def __str__(self):
        return self.role_name


class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128, null=True)
    role = fields.ForeignKeyField("models.Role", related_name="users", to_field="id")

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


class Review(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    house = fields.ForeignKeyField("models.House", related_name="reviews", to_field="id")
    user = fields.ForeignKeyField("models.User", related_name="reviews", to_field="id")
    rating = fields.IntField() # от 1 до 5
    review_text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "reviews"

    def __str__(self):
        return f"Review {self.id} for House {self.house_id} by User {self.user_id}"
