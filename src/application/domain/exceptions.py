
class BaseCoreException(Exception):
    default_message = "Base exception"

    def __init__(self, message: str = None, detail: str = None, cause_entity: str = None):
        super().__init__()
        self.message = message or self.default_message
        self.detail = detail
        self.cause_entity = cause_entity


class ItemNotFound(BaseCoreException):
    default_message = "Item not found"


class DuplicateItem(BaseCoreException):
    default_message = "Item already exists"


class ItemDataConflict(BaseCoreException):
    default_message = "Conflict with data of this item"


class ReferencedItem(BaseCoreException):
    default_message = "Item is referenced by one or more items and cannot be operated"


class UnprocessableItem(BaseCoreException):
    default_message = "Item has wrong structure or type"


class ForbiddenResourceForUser(BaseCoreException):
    default_message = "The user does not have the required policy (role or user_id) for resource"
