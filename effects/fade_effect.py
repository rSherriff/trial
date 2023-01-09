from effects.effect import Effect


class FadeEffect(Effect):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine,x,y,width,height)
        self.current_wipe_length = 0
        
    def start(self, parameters):
        super().start()
        self.lifespan_out = parameters[0]
        self.lifespan_in = parameters[1]
        
    def render(self, console):
        if self.time_alive> (self.lifespan_in + self.lifespan_out):
            self.stop()

        if self.time_alive <= self.lifespan_out:
            t = self.time_alive / self.lifespan_out

            for w in range(0, console.width):
                for h in range(0, self.height):
                    console.tiles_rgb[w,h] = self.tiles[w,h]
                    console.tiles_rgb[w,h][1] = self.blend_colour((0,0,0), self.tiles[w,h][1], t)
                    console.tiles_rgb[w,h][2] = self.blend_colour((0,0,0), self.tiles[w,h][2], t)
        else:
            t = (self.time_alive - self.lifespan_out) / self.lifespan_in

            for w in range(0, console.width):
                for h in range(0, self.height):
                    console.tiles_rgb[w,h][1] = self.blend_colour(console.tiles_rgb[w,h][1], (0,0,0), t)
                    console.tiles_rgb[w,h][2] = self.blend_colour(console.tiles_rgb[w,h][2], (0,0,0), t)

        self.time_alive += self.engine.get_delta_time()

        #temp_console.blit(console, src_x=int(self.current_wipe_length), src_y=0, dest_x=self.x + int(self.current_wipe_length), dest_y=self.y, width=self.width, height=self.height)

    def blend_colour(self, lc, rc, t):
        r = lc[0] * t + rc[0] * (1 - t) 
        g = lc[1] * t + rc[1] * (1 - t) 
        b = lc[2] * t + rc[2] * (1 - t)

        return (int(r),int(g),int(b))