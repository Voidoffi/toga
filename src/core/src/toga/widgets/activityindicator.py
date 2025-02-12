import warnings

from .base import Widget


class ActivityIndicator(Widget):

    def __init__(
        self,
        id=None,
        style=None,
        running=False,
        factory=None,  # DEPRECATED !
    ):
        """

        Args:
            id (str):  An identifier for this widget.
            style (:obj:`Style`): An optional style object. If no style is provided then a
                new one will be created for the widget.
            running (bool):  Set the initial running mode. Defaults to False
            hide_when_stopped (bool):  Hide the indicator when not running. Defaults to
                True.
        """
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################
        super().__init__(id=id, style=style)

        self._is_running = False

        self._impl = self.factory.ActivityIndicator(interface=self)

        if running:
            self.start()
        else:
            self.stop()

    @property
    def is_running(self):
        """
        Use ``start()`` and ``stop()`` to change the running state.

        Returns:
            True if this activity indicator is running
            False otherwise
        """
        return self._is_running

    def start(self):
        """
        Start this activity indicator.
        """
        if not self.is_running:
            self._impl.start()
        self._is_running = True

    def stop(self):
        """
        Stop this activity indicator (if not already stopped).
        """
        if self.is_running:
            self._impl.stop()
        self._is_running = False
