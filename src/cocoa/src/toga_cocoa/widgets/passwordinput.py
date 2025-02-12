from ..libs import (
    NSSecureTextField,
    NSTextFieldSquareBezel,
    objc_method,
    objc_property,
)
from .textinput import TextInput


class TogaSecureTextField(NSSecureTextField):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    @objc_method
    def textShouldEndEditing_(self, textObject) -> bool:
        return self.interface.validate()


class PasswordInput(TextInput):
    def create(self):
        self.native = TogaSecureTextField.new()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add the layout constraints
        self.add_constraints()
