class Post:
    def __init__(self, post_id, create_user_id):
        self.post_id = post_id
        self.create_user_id = create_user_id
        self.list_reading_user_id = []
