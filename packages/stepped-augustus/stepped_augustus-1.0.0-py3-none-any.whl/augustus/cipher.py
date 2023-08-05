class SteppedAugustus:
    """
    Represents a message to be encoded/decoded.

    Parameters
    ----------
    message : str
        The message to be encoded/decoded.
    multiplier : int
        A multiplier to be applied during encoding/decoding.

    Raises
    ------
    TypeError
        If called with incorrect argument types.
    """

    def __init__(self, message: str, multiplier: int = 1) -> None:

        if not isinstance(message, str):
            raise TypeError("Cannot use {type(message)} as message.")

        if not isinstance(multiplier, int):
            raise TypeError("Cannot use {type(multiplier)} as multiplier.")

        self.message = message
        self.multiplier = multiplier

    def _cipher(self, direction: int) -> str:
        """
        Ciphers the message attribute given the direction.

        Parameters
        ----------
            direction : int
                An integer modifier used to change the direction
                of the cipher. Either 1 or -1.

        Returns
        -------
        str
            The ciphered message.
        """

        new_message = []

        for word in self.message.split(" "):
            new_word = []

            for pos, char in enumerate(word, start=1):

                if char.isalpha():
                    lower_bound = 65 if char.isupper() else 97
                    alpha_idx_mod = pos * self.multiplier * direction

                    old_alpha_idx = ord(char) - lower_bound
                    new_alpha_idx = old_alpha_idx + alpha_idx_mod

                    new_word.append(chr(new_alpha_idx % 26 + lower_bound))

                else:
                    new_word.append(char)

            new_message.append("".join(new_word))

        return " ".join(new_message)

    @property
    def right_cipher(self) -> str:
        """The message attribute ciphered to the right."""
        return self._cipher(1)

    @property
    def left_cipher(self) -> str:
        """The message attribute ciphered to the left."""
        return self._cipher(-1)
