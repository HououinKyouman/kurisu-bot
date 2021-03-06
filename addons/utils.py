import sqlite3


# These methods are static since they're used in different addons
async def db_check(bot, msg, cursor, table: str):
    """
    This function is coroutine.

    Checks if table exists.

    :param bot: Bot instance
    :param msg: Message
    :param cursor: Database cursor
    :param table: Table name
    :return: Bool
    """

    try:
        cursor.execute('SELECT 1 FROM {}'.format(table))
        return True
    except sqlite3.Error:
        await bot.send_message(msg.channel, "Table {} is not initialized.\n\n"
                                            "Hint: Use `Kurisu, db init` to perform database initialization.".format(table))
        cursor.close()
        return False


async def get_members(bot, msg, name: str):
    """
    This function is coroutine.

    Gets server member/members.
    Returns array of members in "Username#Discriminator" format/
    First member of this array (members[0]) should be passed to server.get_member_named() method.
    Members array can be used for similar results outputting.

    :param bot: Bot instance
    :param msg: Message
    :param name: Member name
    :return: Array
    """

    members = []

    # Search for a member by mention
    # First check if it's mention
    if name.startswith('<@'):
        print("Mention has been passed. Looking for the member...")
        name = name.strip('<@?!#$%^&*>')
        mem = msg.server.get_member(name)
        print("Member {} found!".format(mem.name))
        members.append(mem.name + '#' + mem.discriminator)
        return members
    else:
        # Search for a member with specific discriminator
        # Since username cannot contain hash we can safely split it
        if '#' in name:
            print("Name with discriminator has been passed. Looking for the member...")
            name_parts = name.split('#')
            for mem in msg.server.members:
                if name_parts[0].lower() in mem.name.lower() and name_parts[1] in mem.discriminator:
                    print("Member {} found!".format(mem.name))
                    members.append(mem.name + '#' + mem.discriminator)
                    # Since there can be only one specific member with this discriminator
                    # we can return members right after we found him
                    return members
            # If we didn't find any members with this discriminator then there's no point to continue.
            if not members:
                print("No members with this discriminator were found...")
                await bot.send_message(msg.channel, "No members were found and I don't have any clue who that is.")
                return None

        # Search for a member by username
        for mem in msg.server.members:
            # Limit number of results
            if name.lower() in mem.name.lower() and len(members) < 6:
                members.append(mem.name + '#' + mem.discriminator)

        # Search for a member by nickname
        # If we didn't find any members, then there is possibility that it's a nickname
        if not members:
            print("Members weren't found. Checking if it's a nickname...")
            for mem in msg.server.members:
                # Limit number of results & check if member has a nick and compare with input
                if mem.nick and name.lower() in mem.nick.lower() and len(members) < 6:
                    members.append(mem.name + '#' + mem.discriminator)

        # If no members this time, then return None and error message, else - return members
        if not members:
            print("No members were found")
            await bot.send_message(msg.channel, "No members were found and I don't have any clue who that is.")
            return None
        else:
            if len(members) > 4:
                await bot.say("There are too many results. Please be more specific.\n\n"
                              "Here is a list with suggestions:\n"
                              "{}".format("\n".join(members)))
                return None
            else:
                return members


# Dummy cog
class Utils:

    # Construct
    def __init__(self):
        print('Addon "{}" loaded'.format(self.__class__.__name__))


def setup(bot):
    bot.add_cog(Utils())
