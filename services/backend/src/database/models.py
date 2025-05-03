import uuid

from tortoise import fields, models


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
    obj_type = fields.CharField(max_length=100, null=True)
    full_address = fields.TextField()
    simple_address = fields.TextField()

    adm_area = fields.ForeignKeyField("models.AdmArea", related_name="houses", to_field="id")
    district = fields.ForeignKeyField("models.District", related_name="houses", to_field="id")

    kad_n = fields.TextField(null=True)  # Кадастровый номер объекта недвижимости
    kad_zu = fields.TextField(null=True)  # Кадастровый номер земельного участка (если имеется)

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
    rating = fields.IntField()  # от 1 до 5
    review_text = fields.TextField()
    is_published = fields.BooleanField(default=False)
    is_deleted = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "reviews"

    def __str__(self):
        return f"Review {self.id} for House {self.house_id} by User {self.user_id}"

class Photo(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    base64_data = fields.TextField()  # Строковое представление изображения в формате Base64
    title = fields.CharField(max_length=255)
    metadata = fields.JSONField(null=True)
    
    # Если фото относится к дому, это поле заполняется:
    house = fields.ForeignKeyField("models.House", related_name="photos", null=True)
    # Если фото относится к отзыву, это поле заполняется:
    review = fields.ForeignKeyField("models.Review", related_name="photos", null=True)

    class Meta:
        table = "photos"

    def __str__(self):
        return self.title
    
class UserSettings(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    # Однозначное соответствие настроек конкретному пользователю
    user = fields.OneToOneField("models.User", related_name="settings", to_field="id")
    profile_photo = fields.ForeignKeyField("models.Photo", related_name="user_settings", null=True)
    
    # Пример дополнительных полей для изменения данных о себе
    bio = fields.TextField(null=True)
    preferences = fields.JSONField(null=True)

    class Meta:
        table = "user_settings"

    def __str__(self):
        return f"Settings for {self.user.username}"