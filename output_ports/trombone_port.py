from mido.ports import BaseOutput

class PrintPort(BaseOutput):
    def _send(self, message):
        if hasattr(message, 'note') and message.type == "note_on":
            print(int(message.note / 10))

