import toga
from toga_dummy.utils import TestCase


class NumberInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.nr_input = toga.NumberInput()
        self.non_int_value = 'a'

    def test_widget_created(self):
        self.assertEqual(self.nr_input._impl.interface, self.nr_input)
        self.assertActionPerformed(self.nr_input, 'create NumberInput')
        self.assertEqual(self.nr_input.readonly, False)

    def test_step(self):
        new_step = 5
        self.nr_input.step = new_step
        self.assertEqual(self.nr_input.step, new_step)

        with self.assertRaises(ValueError):
            self.nr_input.step = self.non_int_value

    def test_min_max_values(self):
        self.assertEqual(self.nr_input.min_value, None)
        self.assertEqual(self.nr_input.max_value, None)

        new_value = 1
        self.nr_input.min_value = new_value
        self.nr_input.max_value = new_value
        self.assertEqual(self.nr_input.min_value, new_value)
        self.assertEqual(self.nr_input.max_value, new_value)

        with self.assertRaises(ValueError):
            self.nr_input.min_value = self.non_int_value
        with self.assertRaises(ValueError):
            self.nr_input.max_value = self.non_int_value

    def test_set_value(self):
        self.nr_input.min_value = 0
        self.nr_input.max_value = 5

        new_value = None
        self.nr_input.value = new_value
        self.assertEqual(self.nr_input.value, new_value)

        new_value = []
        with self.assertRaises(ValueError):
            self.nr_input.value = new_value

        new_value = 3
        self.nr_input.value = new_value
        self.assertEqual(self.nr_input.value, new_value)

        new_value = 6
        self.nr_input.value = new_value
        self.assertEqual(self.nr_input.value, self.nr_input.max_value)

        new_value = -1
        self.nr_input.value = new_value
        self.assertEqual(self.nr_input.value, self.nr_input.min_value)

        with self.assertRaises(ValueError):
            self.nr_input.value = self.non_int_value

    def test_on_change(self):
        def dummy_function():
            pass

        self.nr_input.on_change = dummy_function
        self.nr_input.value = 2
        self.assertValueSet(self.nr_input, 'on_change', self.nr_input.on_change)

    def test_value_init(self):
        value = 5
        nr_input = toga.NumberInput(value=value)
        self.assertEqual(nr_input.value, value)

    def test_focus(self):
        self.nr_input.focus()
        self.assertActionPerformed(self.nr_input, "focus")

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        # default is a deprecated argument
        value = 5
        with self.assertWarns(DeprecationWarning):
            my_nr_input = toga.NumberInput(
                default=value,
            )
        self.assertValueSet(my_nr_input, 'value', value)
        self.assertEqual(my_nr_input.value, value)

        # can't specify both default *and* value
        with self.assertRaises(ValueError):
            toga.NumberInput(
                default=value,
                value=value,
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
