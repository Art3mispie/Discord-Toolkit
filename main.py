import discordtoolkit


tlk = discordtoolkit.DiscordToolkit()
#tlk.token = ""
tlk.token = input("Enter your discord token to authorize with the API!")
print("Logged in as " + tlk.check_token() + "!")

tlk.server_id = input("Enter your target server (server ID) ")

print("""
  _____  _                       _ _______          _ _    _ _   
 |  __ \(_)                     | |__   __|        | | |  (_) | 
 | |  | |_ ___  ___ ___  _ __ __| |  | | ___   ___ | | | ___| |_ 
 | |  | | / __|/ __/ _ \| '__/ _` |  | |/ _ \ / _ \| | |/ / | __|
 | |__| | \__ \ (_| (_) | | | (_| |  | | (_) | (_) | |   <| | |_ 
 |_____/|_|___/\___\___/|_|  \__,_|  |_|\___/ \___/|_|_|\_\_|\__|
                                                                 
  developed by Jane Alderson                                             
"""
)

print("Welcome to the DiscordToolkit console! This console allows you to interact with the discord API easily and directly.")
print("""
Commands:
# tactical OSINT
-   get_roles() # Get a list of roles and permissions on the server.
-   permissions_decoder(int permission_intiger) # Decode a permission intiger and see all individual permissions.
-   get_channels_name() # Get a list of all channel names inside their categorites.
-   read_messages(string channel_id int amount) # reads $(amount) messages in the channel with ID $(channel_id)
-   user(string id) # displays information about the user given ID.

# Hijacking compatibility commands
-   ban(string user_id string reason) # bans $(userID) user from the server with $(reason) as reason
-   message(string channel_id string message) # messages in channel $(channelD) saying $(message)
-   status(string status) # updates status to $(status)
-   armageddon(string message) # attempts to delete all channels and demote every other member, then make a channel and send $(message).
""")

while True:
    command = input("DiscordToolkit> ")
    try:
        print(eval("tlk." + command))
    except Exception as e:
        print("invalid command! " + str(e))