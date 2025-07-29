import phpserialize
from typing import Dict, Any

class PHPSessionDeserializationError(Exception):
    """Custom exception for PHP session deserialization errors."""
    pass


class PHPSessionDeserializer:
    """Parses PHP session-encoded strings into native Python dictionaries."""

    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def deserialize(self, session_string: str) -> Dict[str, Any]:
        """
        Deserializes a PHP session string into a Python dictionary.

        Args:
            session_string (str): Session-encoded string from PHP.

        Returns:
            Dict[str, Any]: Parsed key-value mapping.

        Raises:
            PHPSessionDeserializationError: If decoding fails.
        """
        result = {}
        i = 0
        length = len(session_string)

        try:
            while i < length:
                # Find the key separator
                sep = session_string.find('|', i)
                if sep == -1:
                    raise ValueError("Missing '|' separator")

                key = session_string[i:sep]
                i = sep + 1

                # Now find where the serialized value ends
                # We will increase the slice until phpserialize.loads doesn't raise
                for j in range(i + 1, length + 1):
                    sub = session_string[i:j]
                    try:
                        value = phpserialize.loads(sub.encode(self.encoding), decode_strings=True)
                        result[key] = value
                        i = j  # Move to the next key
                        break
                    except Exception:
                        continue
                else:
                    raise PHPSessionDeserializationError(f"Could not parse value for key '{key}'")

        except Exception as e:
            raise PHPSessionDeserializationError(str(e)) from e

        return result
