#用户视角选择，用于生成文章的视角，第一人称还是第二人称
class perspective:
    def __init__(self):
        self.instruction = ""
        self.example = ""
    def set_perspective(self, perspective_input):
        if perspective_input == "1":
            self.instruction = '* **Narrative Perspective:** First person ("I", "we", "my", "our") - Write from the author\'s personal perspective, sharing experiences, insights, and recommendations as if you are personally involved or have direct experience with the topic.'
            self.example = 'Examples: "I believe that...", "In my experience with...", "We have found that...", "My research shows...", "I recommend..."'
        else:
            self.instruction = '* **Narrative Perspective:** Second person ("you", "your") - Write directly addressing the reader, providing guidance and actionable advice as if speaking directly to them.'
            self.example = 'Examples: "You should consider...", "Your business needs...", "You can achieve...", "You will find that...", "Your next step should be..."'
