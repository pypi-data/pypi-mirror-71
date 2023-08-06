from enum import Enum


class Sign(Enum):
    """Enum class for synaptic sign types.

    """
    EXCITATORY = 1
    INHIBITORY = 2
    UNSPECIFIED = 3

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def color(sign):
        """Convert synaptic sign to color.

        Parameters
        ----------
        sign : Sign

        Returns
        -------

        """
        if sign == EXCITATORY:
            return 'green'
        if sign == INHIBITORY:
            return 'red'
        return 'black'


EXCITATORY = Sign.EXCITATORY
INHIBITORY = Sign.INHIBITORY
UNSPECIFIED = Sign.UNSPECIFIED
