class SteppedAugustus:
    """Represents a message to be encoded/decoded.

    Usage:
    >>> from augustus import SteppedAugustus
    >>>
    >>> SteppedAugustus("Hello, World", 1).right_cipher
    'Igopt, Xqupi'
    >>>
    >>> SteppedAugustus("Igopt, Xqupi", 1).left_cipher
    'Hello, World'
    >>>
    >>> # Alternatively the _cipher method can be used for lazy
    >>> # evaluation and customizing the direction.
    >>> for char in SteppedAugustus("Hello", 1)._cipher(1):
    ...     print(char)
    """

    def __init__(self, message: str, multiplier: int = 1) -> None:

        if not isinstance(message, str):
            raise TypeError("Cannot use {type(message)} as message.")

        if not isinstance(multiplier, int):
            raise TypeError("Cannot use {type(multiplier)} as multiplier.")

        self.message = message
        self.multiplier = multiplier

    def _cipher(self, direction: int) -> str:
        """Ciphers the message attribute given the direction
        and yields each character in a lazy manner."""

        position = 1

        for char in self.message:
            if char.isspace():
                position = 1

            if not char.isalpha():
                yield char
                continue

            lower_bound = 65 if char.isupper() else 97

            ord_mod = position * self.multiplier * direction
            new_ord = (ord(char) - lower_bound + ord_mod) % 26 + lower_bound

            yield chr(new_ord)

            position += 1

    @property
    def right_cipher(self) -> str:
        """The message attribute ciphered to the right."""
        return "".join(self._cipher(1))

    @property
    def left_cipher(self) -> str:
        """The message attribute ciphered to the left."""
        return "".join(self._cipher(-1))
