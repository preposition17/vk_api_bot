# vk_api bot
This is a bot built on a vk_api library with using sockets for interaction of vk_api with bot functions.
![Terminal preview](https://github.com/preposition17/vk_api_bot/blob/master/terminal_preview.jpg)
1. client_api.py connects to server_bot.py
2. client_api.py recives request (VK message from user) and sends it to server_bot.py
3. server_bot.py recives data (request) from client_api.py and performs the function, associated with data.
4. server_bot.py sends response to client_api.py
5. client_api.py sends response (VK message) to user.



