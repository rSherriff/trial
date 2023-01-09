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
    def __init__(self, section: Section, rect: Rect, fg=(255,255,255), bg=(0,0,0)) -> None:

        self.section = section
        
        self.rect = rect

        self.reset_talking()

        self.current_pause = 0
        self.current_dialog_index = 0
        self.longest_line = 0
        self.current_line = 0

        self.fg_color = fg
        self.bg_color = bg

        self.state = DialogState.PENDING

    def start_talking(self, text):
        self.reset_talking()

        self.text = list()
        self.align_justified(text)
        self.change_state(DialogState.DIALOG)

    def reset_talking(self):
        self.text = ""
        self.total_text_length = 0
        self.text_effects = list()
        self.current_dialog_index = 1
        self.longest_line = 0
        self.current_line = 0
        self.change_state(DialogState.PENDING)

    def end_talking(self):
        self.current_dialog_index = self.total_text_length
        self.change_state(DialogState.FINISHED)
        
    def is_pending(self):
        return self.state == DialogState.PENDING

    def is_talking(self):
        return self.state == DialogState.DIALOG

    def is_finished(self):
        return self.state == DialogState.FINISHED

    def update(self):
        if self.state == DialogState.DIALOG:
            self.dialog_tick_loop()

    def get_current_height(self):
        if self.is_finished():
            return int((self.total_text_length ) / self.rect.width)
        return min( int((self.total_text_length ) / self.rect.width), self.current_line + 1)
        
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

        # Print all completed paragraphs
        line_y = self.rect.y
        for i in range(0, paragraph_index):
            for j in range(0, len(self.text[i][1])):
                console.print(self.rect.x, line_y, self.text[i][1][j], fg=self.fg_color, bg=self.bg_color)
                drawn_lines += 1
                line_y += 1
            line_y += 2

        self.current_line = int((self.get_current_dialog_index() ) / self.rect.width) - drawn_lines 

        # Print up to the current line in the current paragraph
        for i in range(0,self.current_line):
            console.print(self.rect.x, line_y, self.text[paragraph_index][1][i], fg=self.fg_color, bg=self.bg_color)
            line_y += 1

        # Print up to the current character in the current line in the current paragraph
        if paragraph_index < len(self.text):
            if self.current_line < len(self.text[paragraph_index][1]):
                current_character = self.get_current_dialog_index() % self.rect.width
                console.print(self.rect.x, line_y, self.text[paragraph_index][1][self.current_line][:current_character], fg=self.fg_color, bg=self.bg_color)

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
            self.end_talking()

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

    def align_justified(self, text: str) -> list[str]:
        
        # Split the text into paragraphs
        text = text.split('\n')


        for i in range(0,len(text)):

            paragraph = text[i]

            # Create an empty list to store the lines of text
            lines = []

            # Split the text into words
            words = paragraph.split()

            # Keep track of some things
            current_line = []
            current_width = 0
            paragraph_length = 0
            equivalent_index = self.total_text_length

            effects = list()

            # Loop through the words in the text
            for word in words:

                if word.startswith("#pause="):
                    value = word[len("#pause="):]
                    self.text_effects.append({"type":TextEffects.PAUSE,"index":equivalent_index-1, "length":float(value)})
                    print(self.text_effects[-1])
                    effects.append((len(lines) + 1, equivalent_index%self.rect.width))
                    continue

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
                    equivalent_index += sum(len(s) for s in current_line)

                    # Start a new line with the current word
                    current_line = [word]
                    current_width = len(word)

            # Add the final line to the list of lines
            lines.append(current_line)
            equivalent_index += sum(len(s) for s in current_line)

            # Justify the lines by adding spaces between the words
            justified_lines = []
            spaces_added = 0
            for j, line in enumerate(lines):
                # Calculate the number of spaces to add between the words
                num_spaces = self.rect.width - sum(len(word) for word in line)
                num_intervals = len(line) - 1

                # Add the spaces between the words
                justified_line = ""
                index_into_line = 0
                for i, word in enumerate(line):
                    justified_line += word

                    if i < num_intervals:
                        # Add an extra space if there are more spaces to add than intervals
                        if num_spaces > num_intervals:
                            justified_line += " "
                            num_spaces -= 1
                            spaces_added += 1
                        justified_line += " " * (num_spaces // num_intervals)
                        spaces_added += (num_spaces // num_intervals)
                        if num_spaces % num_intervals > 0:
                            justified_line += " "
                            num_spaces -= 1
                            spaces_added += 1

                    
                    index_into_line = len(justified_line)
                    if len(effects) > 0:
                        if j == effects[0][0]:
                            if index_into_line >= effects[0][1]:
                                print(spaces_added)
                                #self.text_effects[-1]["index"] += spaces_added
                                effects.pop(0)

                if len(justified_line) < self.rect.width:
                    justified_line += " " * (self.rect.width - len(justified_line))

                if len(justified_line) > self.longest_line:
                    self.longest_line = len(justified_line)

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
                
            self.text.append((paragraph_length, justified_lines))

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