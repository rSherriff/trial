from enum import Enum, auto
from sections.section import Section
from sections.section_layouts import Rect


class DialogState(Enum):
    PENDING = auto()
    DIALOG = auto()
    FINISHED = auto()

class TextEffects(Enum):
    PAUSE = auto()

class Dialog():
    def __init__(self, section: Section, rect: Rect) -> None:

        self.section = section
        
        self.rect = rect

        self.reset_talking()

        self.current_pause = 0
        self.current_dialog_index = 0

        self.state = DialogState.PENDING

    def start_character_talking(self, text):
        self.reset_talking()

        self.analyse_text(text)
        for i in range(0,len(self.text)):
            self.text[i] = self.align_justified(self.text[i])
        self.change_state(DialogState.DIALOG)

    def reset_talking(self):
        self.text = ""
        self.total_text_length = 0
        self.text_effects = list()
        self.current_dialog_index = 1

    def end_talking(self):
        self.current_dialog_index = len(self.text)
        self.change_state(DialogState.FINISHED) 

    def update(self):
        if self.state == DialogState.DIALOG:
            self.dialog_tick_loop()

    def render(self, console):
        drawn_lines = 0

        # Figure out what paragraph we are in
        paragraph_length_count = 0
        paragraph_index = 0
        for paragraph_tuple in self.text:
            paragraph_length_count += paragraph_tuple[0]
            if self.get_current_dialog_index() < paragraph_length_count:
                break
            paragraph_index += 1

        # print all completed paragraph
        line_y = self.rect.y
        for i in range(0, paragraph_index):
            for j in range(0, len(self.text[i][1])):
                console.print(self.rect.x, line_y, self.text[i][1][j], fg=(255,255,255), bg=(0,0,0))
                drawn_lines += 1
                line_y += 1
            line_y += 2

        current_line = int((self.get_current_dialog_index() ) / self.rect.width) - drawn_lines

        # Print up to the current line in the current paragraph
        for i in range(0,current_line):
            console.print(self.rect.x, line_y, self.text[paragraph_index][1][i], fg=(255,255,255), bg=(0,0,0))
            line_y += 1

        # Print up to the current character in the current line in the current paragraph
        if paragraph_index < len(self.text):
            if current_line < len(self.text[paragraph_index][1]):
                current_character = self.get_current_dialog_index() % self.rect.width
                console.print(self.rect.x, line_y, self.text[paragraph_index][1][current_line][:current_character], fg=(255,255,255), bg=(0,0,0))

    def dialog_tick_loop(self):
        self.current_pause += self.section.engine.get_delta_time()
        self.current_pause = min(self.current_pause, 0)
        if self.current_pause >= 0:
            diff =  self.section.engine.get_delta_time() * 50
            if len(self.text_effects) >0:
                if self.text_effects[0]["type"] == TextEffects.PAUSE:  
                    if self.current_dialog_index + diff >= self.text_effects[0]["index"]:  
                        self.current_pause -= self.text_effects[0]["length"]   
                        self.current_dialog_index  = self.text_effects[0]["index"]   
                        self.text_effects.pop(0)  
                    else:
                        self.current_dialog_index += diff  
            else:
                self.current_dialog_index += diff  

        if self.current_dialog_index > self.total_text_length:          
            self.change_state(DialogState.FINISHED)

    def get_current_dialog_index(self):
        return (int(self.current_dialog_index))

    def change_state(self, new_state):
        self.state = new_state

    def analyse_text(self, text):
        split_text = text.split('#')
        final_text = ""
        for t in split_text:
            if t.startswith("pause="):
                t = t[len("pause="):]
                self.text_effects.append({"type":TextEffects.PAUSE,"index":len(final_text), "length":float(t)})
            else:
                final_text += t

        self.text = final_text.split('\n')

    def align_justified(self, text: str) -> list[str]:
        # Create an empty list to store the lines of text
        lines = []

        # Split the text into words
        words = text.split()

        # Keep track of the current line and current width
        current_line = []
        current_width = 0
        paragraph_length = 0

        # Loop through the words in the text
        for word in words:
            # If the current line is empty, add the word to the line
            if current_line == []:
                current_line = [word]
                current_width = len(word)
            # If the current line is not empty and the word fits on the current line
            elif current_width + 1 + len(word) <= self.rect.width:
                # Add the word to the line, with a space between the words
                current_line.append(word)
                current_width += 1 + len(word)
            # If the word does not fit on the current line
            else:
                # Add the current line to the list of lines
                lines.append(current_line)

                # Start a new line with the current word
                current_line = [word]
                current_width = len(word)

        # Add the final line to the list of lines
        lines.append(current_line)

        # Justify the lines by adding spaces between the words
        justified_lines = []
        for line in lines:
            # Calculate the number of spaces to add between the words
            num_spaces = self.rect.width - sum(len(word) for word in line)
            num_intervals = len(line) - 1

            # Add the spaces between the words
            justified_line = ""
            for i, word in enumerate(line):
                justified_line += word
                if i < num_intervals:
                    # Add an extra space if there are more spaces to add than intervals
                    if num_spaces > num_intervals:
                        justified_line += " "
                        num_spaces -= 1
                    justified_line += " " * (num_spaces // num_intervals)
                    if num_spaces % num_intervals > 0:
                        justified_line += " "
                        num_spaces -= 1
            paragraph_length += len(justified_line)
            justified_lines.append(justified_line)

        #final_line = ""
        #for i, word in enumerate(lines[-1]):
            #final_line += word
            #if i < len(lines[-1]) -1:
                #final_line += " "
            
        #paragraph_length += len(final_line)
        self.total_text_length += paragraph_length
        #justified_lines.append(final_line)

        """
        # If the height of the box is less than the number of lines,
        # return only the last height lines
        if len(justified_lines) > self.rect.height:
            return justified_lines[-self.rect.height:]
        # If the height of the box is greater than or equal to the number of lines,
        # return all of the lines
        else:
            return justified_lines
        """

        return (paragraph_length, justified_lines)
    