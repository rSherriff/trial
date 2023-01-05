

from actions.actions import Action

class GenericAction(Action):
    def __init__(self, engine, func) -> None:
        super().__init__(engine)
        self.func = func

    def perform(self) -> None:
        self.func()

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

class JumpToMenuAction(Action):
    def __init__(self, engine) -> None:
        super().__init__(engine)

    def perform(self) -> None:
        self.engine.open_menu()

class EndCurrentChapterAction(Action):
    def __init__(self, engine) -> None:
        super().__init__(engine)

    def perform(self) -> None:
        self.engine.end_current_chapter()
