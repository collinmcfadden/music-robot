from mido.ports import BaseOutput
from mido import open_output
from output_ports.trombone_port import PrintPort

class PortSplitter(BaseOutput):
    
    def __init__(self, trombone_channel_num):
        self.trombone_channel_num = trombone_channel_num
        super().__init__()

    def _open(self):
        self.accompaniment_port = open_output('Microsoft GS Wavetable Synth 0')
        self.trombone_port = PrintPort()

    def _send(self, message):
        # print(message)
        if hasattr(message, 'channel') and message.channel == self.trombone_channel_num:
            self.trombone_port.send(message)
        else:
            self.accompaniment_port.send(message)