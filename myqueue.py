from twilio.rest import Client

class MyQueue:

    def __init__(self):
        self.account_sid = 'ACc5d75f40a69e6846130c587baa3607c9'
        self.auth_token = '3027e609089cd833248a4c24547edaba'
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = [
            {
                'name':'Daniela',
                'phone':'+56949514914'
            },
            {
                'name':'Sebastian',
                'phone':'+56949514914'
            }
        ]
        self._mode = 'FIFO'
        

    def enqueue(self, user):
        msg = ""
        if self.size() > 0:
            msg = "there are " + str(self.size()) + " people ahead of you"
        else:
            msg = "you are next in line"

        message = self.client.messages.create(
            body= "Hello " + user['name'] + " , " + msg,
            from_= "+18646060750",
            to= user['phone']
        )

        self._queue.append(user)

        result = {
            "user" : user,
            "message": {
                "status": message.status
            }
        }
        return result

    def dequeue(self):

        if self.size() > 0:
            if self._mode == 'FIFO':
                deleted_user = self._queue.pop(0)
            else:
                deleted_user = self._queue.pop(0)

            message = self.client.messages.create(
                body = "Thanks for coming " + deleted_user["name"] + ", come back soon",
                to = deleted_user["phone"],
                from_ = "+18646060750" 
            )

            result = {
                "user": deleted_user,
                "message": {
                    "status": message.status
                }
            }

            return result
        
        else:
            return "There are no users to delete"

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)
