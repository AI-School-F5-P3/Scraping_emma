class Quote:
    def __init__(self, text, author, tags, author_about_link):
        self.text = text
        self.author = author
        self.tags = tags
        self.author_about_link = author_about_link

class Author:
    def __init__(self, name, about, about_link):
        self.name = name
        self.about = about
        self.about_link = about_link