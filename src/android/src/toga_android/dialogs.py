import asyncio

# from com.chaquo.python import Python
from java import Override, jint, jvoid, static_proxy

from android.app import Activity
from android.content import Intent  # Context
from android.net import Uri

from .libs.android import R__drawable
from .libs.android.app import AlertDialog__Builder
from .libs.android.content import DialogInterface__OnClickListener


class FileDialogsActivity(static_proxy(Activity)):
    def __init__(self):
        super().__init__()

    @Override(jvoid, [jint, Intent])
    def onActivityResult(self, requestCode, resultCode, returnIntent):
        selected_uri = None
        if resultCode == Activity.RESULT_OK:
            if returnIntent is not None:
                selected_uri = returnIntent.getData()
                if selected_uri is None:
                    selected_uri = []
                    clip_data = returnIntent.getClipData()
                    if clip_data is not None:
                        for i in range(0, clip_data.getItemCount()):
                            selected_uri.append(str(clip_data.getItemAt(i).getUri()))
                else:
                    selected_uri = [str(selected_uri)]
        if selected_uri is None:
            raise ValueError("No filename provided in the open file dialog")


class OnClickListener(DialogInterface__OnClickListener):
    def __init__(self, fn=None, value=None):
        super().__init__()
        self._fn = fn
        self._value = value

    def onClick(self, _dialog, _which):
        if self._fn:
            self._fn(self._value)


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __bool__(self):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __await__(self):
        return self.future.__await__()


class TextDialog(BaseDialog):
    def __init__(
            self,
            window,
            title,
            message,
            positive_text,
            negative_text=None,
            icon=None,
            on_result=None,
    ):
        """Create Android textual dialog.

        - window: Toga Window
        - title: Title of dialog
        - message: Message of dialog
        - positive_text: Button text where clicking it returns True (or None to skip)
        - negative_text: Button text where clicking it returns False (or None to skip)
        - icon: Integer used as an Android resource ID number for dialog icon (or None to skip)
        """
        super().__init__()
        self.on_result = on_result

        builder = AlertDialog__Builder(window._impl.app.native)
        builder.setCancelable(False)
        builder.setTitle(title)
        builder.setMessage(message)
        if icon is not None:
            builder.setIcon(icon)

        if positive_text is not None:
            builder.setPositiveButton(positive_text, OnClickListener(self.completion_handler, True))
        if negative_text is not None:
            builder.setNegativeButton(negative_text, OnClickListener(self.completion_handler, False))
        builder.show()

    def completion_handler(self, return_value: bool) -> None:
        if self.on_result:
            self.on_result(self, return_value)

        self.future.set_result(return_value)


class InfoDialog(TextDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            positive_text="OK",
            on_result=on_result,
        )


class QuestionDialog(TextDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            positive_text="Yes",
            negative_text="No",
            on_result=on_result,
        )


class ConfirmDialog(TextDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            positive_text="OK",
            negative_text="Cancel",
            on_result=on_result,
        )


class ErrorDialog(TextDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            positive_text="OK",
            icon=R__drawable.ic_dialog_alert,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None, **kwargs):
        super().__init__()
        window.factory.not_implemented("Window.stack_trace_dialog()")


class SaveFileDialog(BaseDialog):
    def __init__(self, window, title, filename, initial_directory, file_types=None, on_result=None):
        super().__init__()
        window.factory.not_implemented("Window.save_file_dialog()")


class OpenFileDialog(BaseDialog):
    def __init__(self, window, title, initial_directory, file_types, multiselect, on_result=None):
        super().__init__()
        self.on_result = on_result
        self.multiselect = multiselect

        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("*/*")
        if initial_directory is not None and str(initial_directory) != '':
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(str(initial_directory)))
        if file_types is not None and file_types != ['']:
            # Commented out because rubicon currently does not support arrays and nothing else works with this Intent
            # see https://github.com/beeware/rubicon-java/pull/53
            # intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types)
            window.factory.not_implemented(
                'Window.open_file_dialog() on Android currently does not support the file_type parameter')
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiselect)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        # context = Python.getPlatform().getApplication()
        context = FileDialogsActivity()
        context.startActivityForResult(intent, jint(1))

    def completion_handler(self, return_value: bool) -> None:
        if self.on_result:
            self.on_result(self, return_value)

        self.future.set_result(return_value)


class SelectFolderDialog(BaseDialog):
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        super().__init__()
        window.factory.not_implemented("Window.select_folder_dialog()")
