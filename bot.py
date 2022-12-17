import discord, colorama
from discord.ext import commands
from dotenv import load_dotenv

# class Bot(discord.Client): 
class Bot(commands.Bot): 
    def __init__(self, command_prefix, token, channel_id):
        """ Initialize the bot. """

        # Initialize the inherited class
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=False)

        # Set internal arguments
        self.token = token
        self.channel_id = channel_id

        # Define all commands
        self.add_command()

    ## Utility Methods ##
    def print_result(self, output, color=colorama.Fore.GREEN):
        """ Base method. Pretty print out results to terminal as well as log. """
        print(f"{color} {output} {colorama.Fore.RESET}")
        logging.info(output) 

    ## Command Method ##
    def add_commands(self):
        """ Add commands to the bot. """
        @self.command(name="ping", pass_context=True)
        async def ping(message):
            await message.channel.send(f"Pong to you, {message.author}!")
    
    ## Overridden Methods ##
    async def on_ready(self):
        """ When the bot is ready, print a message to the console. """
        self.print_result(f"[+] Ready. Logged in as {self.user}")
        
    async def on_message(self, message):
        """ Do something when a message is received. """ 
        if message.author == self.user:
            return # don't run commands on thyself 

        # Log all mesages
        self.result(f"[*] Received message: {message.content} from {message.author} in {message.channel}", colorama.Fore.YELLOW)

    async def on_error(event, *args, **kwargs):
        """ Handle bot errors. """
        if event == 'on_message':
            self.result(f"Unhandled message: {args[0]}", colorama.Fore.RED)
        else:
            raise

if __name__ == "__main__":
    # Automatically load the .env file in the current working directory
    try:
        load_dotenv()
        token      = os.environ["DISCORD_BOT_TOKEN"]
        channel_id = os.environ["DISCORD_CHANNEL_ID"]
    except KeyError:
        print("[-] Error: Could not read .env properly. Exiting.")
        exit(1)

    # Create a new instance of the bot and run it
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(intents=intents, token=token, channel_id=channel_id)
    bot.run(token)
