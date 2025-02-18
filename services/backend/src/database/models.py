from tortoise import fields, models


# Пример простых кастомных полей для работы с геоданными.
# Здесь они унаследованы от TextField для хранения строкового представления WKT.
# В реальном проекте следует реализовать полноценную сериализацию/десериализацию.
class GeometryField(fields.TextField):
    """
    Поле для хранения геометрического объекта (например, полигон в формате WKT).
    Ожидается, что данные будут храниться в формате GEOMETRY(Polygon,4326).
    """
    pass


class PointField(fields.TextField):
    """
    Поле для хранения точки (например, центральная точка объекта) в формате WKT.
    Ожидается, что данные будут храниться в формате GEOMETRY(Point,4326).
    """
    pass


class RawAddress(models.Model):
    """
    Таблица для сырого хранения загруженных CSV-данных.
    Здесь можно хранить все исходные данные в формате JSON.
    """
    id = fields.IntField(pk=True)
    # В данном случае все данные сохраняются в одном поле.
    # При необходимости можно добавить отдельные поля, соответствующие колонкам CSV.
    raw_data = fields.JSONField()

    class Meta:
        table = "raw_addresses"

    def __str__(self):
        return f"RawAddress {self.id}"


class AdmArea(models.Model):
    """
    Справочник административных округов.
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "adm_areas"

    def __str__(self):
        return self.name


class District(models.Model):
    """
    Справочник муниципальных округов/поселений.
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "districts"

    def __str__(self):
        return self.name


class House(models.Model):
    """
    Основная таблица объектов недвижимости.
    """
    id = fields.IntField(pk=True)
    unom = fields.CharField(max_length=255, unique=True)
    obj_type = fields.CharField(max_length=100)  # Например: "Здание"
    full_address = fields.TextField()            # Полное юридическое описание
    simple_address = fields.TextField()          # Упрощённое описание

    # Внешние ключи на справочники
    adm_area = fields.ForeignKeyField("models.AdmArea", related_name="houses")
    district = fields.ForeignKeyField("models.District", related_name="houses")

    kad_n = fields.TextField()            # Кадастровый номер объекта недвижимости
    kad_zu = fields.TextField(null=True)    # Кадастровый номер земельного участка (если имеется)

    # Геоданные с использованием кастомных полей для PostGIS
    geo_data = GeometryField(null=True)         # GEOMETRY(Polygon,4326) – полигон объекта
    geodata_center = PointField(null=True)        # GEOMETRY(Point,4326) – центральная точка

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "houses"

    def __str__(self):
        return f"House {self.unom}"


class Role(models.Model):
    """
    Справочник ролей пользователей.
    """
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "roles"

    def __str__(self):
        return self.role_name


class User(models.Model):
    """
    Таблица пользователей. Каждый пользователь имеет одну роль.
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128, null=True)
    role = fields.ForeignKeyField("models.Role", related_name="users")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


class Review(models.Model):
    """
    Отзывы пользователей к объектам недвижимости.
    """
    id = fields.IntField(pk=True)
    house = fields.ForeignKeyField("models.House", related_name="reviews")
    user = fields.ForeignKeyField("models.User", related_name="reviews")
    rating = fields.IntField()       # Например, значение от 1 до 5
    review_text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "reviews"

    def __str__(self):
        return f"Review {self.id} for House {self.house_id} by User {self.user_id}"
