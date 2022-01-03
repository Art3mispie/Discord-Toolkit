import requests
import json
  
class DiscordToolkit:
    token = ""
    server_id = ""

    CREATE_INSTANT_INVITE = 0x1
    KICK_MEMBERS = 0x2
    BAN_MEMBERS = 0x4
    ADMINISTRATOR = 0x8
    MANAGE_CHANNELS = 0x10
    MANAGE_GUILD = 0x20
    ADD_REACTIONS = 0x40
    VIEW_AUDIT_LOG = 0x80
    PRIORITY_SPEAKER = 0x100
    STREAM = 0x200
    VIEW_CHANNEL = 0x400
    SEND_MESSAGES = 0x800
    SEND_TTS_MESSAGES = 0x1000
    MANAGE_MESSAGES = 0x2000
    EMBED_LINKS = 0x4000
    ATTACH_FILES = 0x8000
    READ_MESSAGE_HISTORY = 0x10000
    MENTION_EVERYONE = 0x20000
    USE_EXTERNAL_EMOJIS = 0x40000
    VIEW_GUILD_INSIGHTS = 0x80000
    CONNECT = 0x100000
    SPEAK = 0x200000
    MUTE_MEMBERS = 0x400000
    DEAFEN_MEMBERS = 0x800000
    MOVE_MEMBERS = 0x1000000
    USE_VAD = 0x2000000
    CHANGE_NICKNAME = 0x4000000
    MANAGE_NICKNAMES = 0x8000000
    MANAGE_ROLES = 0x10000000
    MANAGE_WEBHOOKS = 0x20000000
    MANAGE_EMOJIS = 0x40000000
    USE_SLASH_COMMANDS = 0x80000000
    REQUEST_TO_SPEAK = 0x100000000

    permissions_list = ['CREATE_INSTANT_INVITE', 'KICK_MEMBERS', 'BAN_MEMBERS', 'ADMINISTRATOR', 'MANAGE_CHANNELS', 
    'MANAGE_GUILD', 'ADD_REACTIONS', 'VIEW_AUDIT_LOG', 'PRIORITY_SPEAKER', 'STREAM', 'VIEW_CHANNEL', 'SEND_MESSAGES',
    'SEND_TTS_MESSAGES', 'MANAGE_MESSAGES', 'EMBED_LINKS', 'ATTACH_FILES', 'READ_MESSAGE_HISTORY', 'MENTION_EVERYONE', 'USE_EXTERNAL_EMOJIS', 
    'VIEW_GUILD_INSIGHTS', 'CONNECT', 'SPEAK', 'MUTE_MEMBERS', 'DEAFEN_MEMBERS', 'MOVE_MEMBERS', 'USE_VAD', 'CHANGE_NICKNAME', 
    'MANAGE_NICKNAMES', 'MANAGE_ROLES', 'MANAGE_WEBHOOKS', 'MANAGE_EMOJIS', 'USE_SLASH_COMMANDS', 'REQUEST_TO_SPEAK']

    def check_token(self):
        request = requests.get(f"https://discord.com/api/v9/users/@me", headers={"Authorization": self.token})
        return json.loads(request.text)["username"] + "#" + json.loads(request.text)["discriminator"]

    def get_roles_raw(self):
        request = requests.get(f"https://discord.com/api/v9/guilds/{self.server_id}/roles", headers={"Authorization": self.token})
        return request
    
    def get_roles(self):
        roles = self.get_roles_raw()
        roles = json.loads(roles.text)
        roles_string = ""
        for role in roles:
            role = str(role)
            role = role.replace("\'", "")
            role = role.replace("{", "")
            role = role.replace("}", "")
            roles_string += role + "\n"
        return roles_string
    
    def permissions_decoder_raw(self, permission_int):
        decoded_permissions = []
        for x in range(len(self.permissions_list)):
            decoded_permissions.append((int(permission_int) & eval("self." + self.permissions_list[x])) == eval("self." + self.permissions_list[x]))
        return decoded_permissions
    
    def permissions_decoder(self, permission_int):
        raw = self.permissions_decoder_raw(permission_int)
        result = ""
        for x in range(len(raw)):
            result += f"{self.permissions_list[x]}: {raw[x]},\n"
        return result
    
    def get_channels_raw(self):
        request = requests.get(f"https://discord.com/api/v9/guilds/{self.server_id}/channels", headers={"Authorization": self.token})
        return request
    
    def get_channels_info_raw(self):
        raw = json.loads(self.get_channels_raw().text)
        categories = []
        categories_raw = []
        channels_raw = []
        voice_channels_raw = []
        for entity in raw:
            if(entity["type"] == 4):
                categories_raw.append(entity)
                continue
            elif(entity["type"] == 0):
                channels_raw.append(entity)
    
        for category in categories_raw:
            categories.append({
                "name": category["name"],
                "id": category["id"],
                "permission_overwrites": category["permission_overwrites"],
                "channels": []
            })
        
        category_ids = []
        for category in categories:
            category_ids.append(category["id"])

        for x in range(len(channels_raw)):
            categories[category_ids.index(channels_raw[x]["parent_id"])]["channels"].append(channels_raw[x])
        
        return categories
            
    def get_channels_name(self):
        names = ""
        raw = self.get_channels_info_raw()
        for category in raw:
            names += category["name"] + "\n"
            for channel in category["channels"]:
                names += "\t" + channel["name"] + "\n"
        return names

    def get_channels_info(self):
        names = ""
        raw = self.get_channels_info_raw()
        for category in raw:
            names += category["name"] + "\n"
            for channel in category["channels"]:
                overwrites = channel["permission_overwrites"]
                names += "\t" + channel["name"] + "\n\t" +" || PERMISSIONS: " + str(channel["permission_overwrites"]) + " ||" + "\n"
        return names
    
    def read_messages_raw(self, channel_id, amount):
        request = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={amount}", headers={"Authorization": self.token})
        return request
    
    def read_messages(self, channel_id, amount):
        raw = json.loads(self.read_messages_raw(channel_id, amount).text)
        message_log = ""
        for message in raw:
            print(type(message))
            username = message["author"]["username"]
            content = message["content"]
            message_log += f"{username}: {content}\n"
        return message_log