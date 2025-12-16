from datetime import datetime

class Transaction:
    def __init__(self,user_id:str,book_title:str,action:str)->None:
        self.user_id = user_id
        self.book_title = book_title
        self.action = action # borrow or return#
        self.timestamp:datetime=datetime.now()

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] | {self.action.upper()} | {self.book_title} | User: {self.user_id}"
