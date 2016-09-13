class SlackMessage:
    def __init__(self, fallback, color, text, title, title_link, fields=None):
        self.attachments = []
        self.attachments.append({})
        self.attachments[0]['fallback'] = fallback
        self.attachments[0]['color'] = color
        self.attachments[0]['text'] = text
        self.attachments[0]['title'] = title
        self.attachments[0]['title_link'] = title_link
        if fields is None:
            self.attachments[0]['fields'] = []
        else:
            self.attachments[0]['fields'] = fields
