import discord
from datetime import datetime, date
import calendar


table = dict()


def date2id(date_string):

    now = datetime.now()
    now = now.date()

    if len(date_string) < 2 or len(date_string) > 3 or min([len(i) for i in date_string]) < 1:
        return None, "date syntax is d/m[/y] cyka :)"
    elif len(date_string) == 2:
        date_string.append(str(now.year))
    else:
        if len(date_string[2]) == 2:
            date_string[2] = "20" + date_string[2]

    try:
        date_int = [int(i) for i in reversed(date_string)]
    except ValueError:
        return None, "try numbers..."

    try:
        day = date(*date_int)
    except ValueError as error:
        return None, error

    if (day - now).days <= 0:
        return None, "sorry you can't change the past my friend :/"

    return day, None


def date2str(day):

    text = "{} {}/{}/{}".format(calendar.day_name[day.weekday()], day.day, day.month, day.year)

    return text


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('rombot'):

            global table

            if message.content.startswith('rombot help'):

                help_message = "List of commands:\n" + \
                               "rombot help: display the list of commands\n" + \
                               "rombot add d/m[/y]: mark you available at this date\n" + \
                               "rombot remove d/m[/y]: unmark you (unavailable) at this date\n" + \
                               "rombot display d/m[/y]: display all the available cykas from now to this date\n"
                await message.channel.send(help_message)

            if message.content.startswith('rombot remove'):

                day, text = date2id(message.content[14:].split('/'))
                if day is None:
                    await message.channel.send(text)
                    return

                if day not in table.keys():
                    table[day] = []
                if message.author in table[day]:
                    table[day].remove(message.author)
                    await message.channel.send("you are marked unavailable the " + date2str(day))
                else:
                    await message.channel.send("you are already marked unavailable the " + date2str(day))

            if message.content.startswith('rombot add'):

                day, text = date2id(message.content[11:].split('/'))
                if day is None:
                    await message.channel.send(text)
                    return

                if day not in table.keys():
                    table[day] = []
                if message.author in table[day]:
                    await message.channel.send("you are already marked available the " + date2str(day))
                else:
                    table[day].append(message.author)
                    await message.channel.send("you are marked available the " + date2str(day))

            if message.content.startswith('rombot display'):

                now = datetime.now()
                now = now.date()

                last_day, text = date2id(message.content[15:].split('/'))
                if last_day is None:
                    await message.channel.send(text)
                    return

                text = "Available:\n"
                for day in sorted(table.keys()):
                    if (len(table[day]) > 0) and (day > now) and (day <= last_day):
                        text += date2str(day) + ": " + ", ".join([member.name for member in table[day]]) + "\n"

                await message.channel.send(text)


client = MyClient()


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client.run(token)
