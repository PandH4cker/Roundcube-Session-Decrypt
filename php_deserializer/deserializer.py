import phpserialize
from typing import Any


class PHPDeserializationError(Exception):
    """Custom exception for PHP deserialization errors."""
    pass


class PHPDeserializer:
    """Handles conversion from PHP serialized strings to native Python objects."""

    def __init__(self, encoding: str = "utf-8") -> None:
        """
        Initialize the deserializer.

        Args:
            encoding (str): Character encoding used for PHP serialized strings.
        """
        self.encoding = encoding

    def deserialize(self, php_string: str) -> Any:
        """
        Deserialize a PHP serialized string into a Python object.

        Args:
            php_string (str): The PHP serialized string.

        Returns:
            Any: Native Python object representing the deserialized data.

        Raises:
            PHPDeserializationError: If the input cannot be deserialized.
        """
        try:
            bytes_input = php_string.encode(self.encoding)
            result = phpserialize.loads(bytes_input, decode_strings=True)
            return result
        except Exception as ex:
            raise PHPDeserializationError("Invalid PHP serialized input") from ex
