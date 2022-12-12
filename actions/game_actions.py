

from actions.actions import Action

class JumpToChapterAction(Action):
    def __init__(self, engine, chapter) -> None:
        super().__init__(engine)
        self.chapter = chapter

    def perform(self) -> None:
        self.engine.start_chapter(self.chapter)

class JumpToStageAction(Action):
    def __init__(self, engine, stage) -> None:
        super().__init__(engine)
        self.stage = stage

    def perform(self) -> None:
        self.engine.start_stage(self.stage)

