
class ModmailThread:
  def __init__(self, message):
    self.id = message.id
    self.author_id = message.author.id
    self.author_name = message.author.name
    self.content = message.content
    self.attachments = message.attachments
    self.created_at = str(message.created_at)
    self.jump_url = message.jump_url
