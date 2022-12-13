from threading import Timer

class Animation():
    def __init__(self, engine, frames, timeline, tick_length) -> None:
        self.engine = engine
        self.frames = frames
        self.timeline = timeline
        self.tick_length = tick_length
        self.current_tick = 0
        self.timer = None

    def start(self):
        self.tick_loop()

    def stop(self):
        self.timer.cancel()

    def tick_loop(self):
        self.current_tick += 1
        if self.current_tick >= len(self.timeline):
            self.current_tick = 0
        self.timer = Timer(self.tick_length, self.tick_loop)
        self.timer.daemon = True
        self.timer.start()
 
    def get_animation_tick(self):
        return (self.animation_tick)

    def get_current_frame(self):
        return self.frames[self.timeline[self.current_tick]]

"""
        frames = {"1":"a","2":"b","3":"c"}
        timeline = "111222333"
        animation = Animation(self.engine, test_anim_dict, test_anim_timeline, 0.5)
        animation.start()
        animation.get_current_frame()
"""

    