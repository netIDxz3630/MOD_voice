from effects.effect import Effect
import math

class Modulation_fequencyEffect(Effect):
    def __init__(self, rate, block_len):
        super().__init__(rate, block_len)

        # Buffer to store past signal values. Initialize to zero.
        self.buffer_len =  1024          # Set buffer length.
        self.buffer = self.buffer_len * [0]   # list of zeros
        
        # Buffer (delay line) indices
        self.kr = 0  # read index
        self.kw = int(0.5 * self.buffer_len)  # w

    def apply(self, view, input_tuple):

        self.gain = view.modulation_feedback.get() / 100
        self.f0 = view.modulation_frequency.get()

        diff_block = [0] * self.block_len

        # Initialize phase
        self.om = 2 * math.pi * self.f0 / self.rate
        self.theta = 0

        for n in range(0, self.block_len):

            x0 = input_tuple[n]
            
            # Get previous and next buffer values (since kr is fractional)
            kr_prev = int(math.floor(self.kr))
            frac = self.kr - kr_prev    # 0 <= frac < 1
            kr_next = kr_prev + 1
            if kr_next == self.buffer_len:
                kr_next = 0           

            # Compute output value using interpolation
            diff_block[n] = int((1-frac) * self.buffer[kr_prev] + frac * self.buffer[kr_next]) - x0

            # Update buffer
            self.buffer[self.kw] = x0  

            # Amplitude modulation:
            self.theta = self.theta + self.om
            diff_block[n] = int( input_tuple[n] * math.cos(self.theta) )
               
            # keep theta betwen -pi and pi
            while self.theta > math.pi:
                self.theta = self.theta - 2*math.pi

            # Ensure that 0 <= kr < BUFFER_LEN
            if self.kr >= self.buffer_len:
                # End of buffer. Circle back to front.
                self.kr = self.kr - self.buffer_len

            # Increment write index    
            self.kw = self.kw + 1
            if self.kw == self.buffer_len:
                # End of buffer. Circle back to front.
                self.kw = 0

        return diff_block