class Effect:
    def __init__(self, rate, block_len):
        self.rate = rate
        self.block_len = block_len

    def clip16(self, x):    
        # Clipping for 16 bits
        if x > 32767:
            x = 32767
        elif x < -32768:
            x = -32768
        else:
            x = x        
        return int(x)
    
    def apply(self, view, input_tuple):
        pass