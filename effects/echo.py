from effects.effect import Effect

class EchoEffect(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)
        self.change_delay(0.1)

    def apply(self, view, input_tuple):

        gain = view.echo_feedback.get() / 100
        delay = view.echo_delay.get()

        if self.delay_sec != delay:
            self.change_delay(delay)
        
        diff_block = [0] * self.block_len

        for n in range(0, self.block_len):

            x0 = input_tuple[n]
            
            # Compute output value
            # y(n) = x(n) + G x(n-N)
            y0 = x0 + gain * self.buffer[self.pointer]

            diff_block[n] = self.clip16(y0) - x0

            # Update buffer
            self.buffer[self.pointer] = x0

            # Increment buffer index
            self.pointer = self.pointer + 1
            if self.pointer >= self.buffer_len:
                # The index has reached the end of the buffer. Circle the index back to the front.
                self.pointer = 0
        
        return diff_block
    
    def change_delay(self, delay):
        # delay in seconds, 50 milliseconds
        self.delay_sec = delay

        # Buffer to store past signal values. Initialize to zero.
        self.buffer_len = int(self.rate * self.delay_sec)              # length of buffer
        self.buffer = self.buffer_len * [0]   # list of zeros
        self.pointer = 0