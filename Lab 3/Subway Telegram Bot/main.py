import os
import random
import sys
import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyswip import Prolog

from telegram_api_key import TOKEN
from prolog_interface import PrologInterface

# Show Keyboard with options
def showKeyboard(options, add_skip=False):
  new_list = []
  
  for item in options:
    new_list.append(item.capitalize().replace("_", " "))
  
  if add_skip:
    new_list += ["🚫 Skip"]

  n = 2
  new_segmented_list = [new_list[i * n:(i + 1) * n] for i in range((len(new_list) + n - 1) // n )]

  keyboard_list = []
  for inner_list in new_segmented_list:
    temp_list = []
    for item in inner_list:
      temp_list.append(KeyboardButton(text=item))
    keyboard_list.append(temp_list)
    
  return ReplyKeyboardMarkup(keyboard=keyboard_list, resize_keyboard=True, one_time_keyboard=True)

# Parse User Responses
def __convertListToNumberedString(list_input):
    string = ""
    for item in list_input:
        string += "• {item}\n".format(item=item.capitalize().replace("_", " "))
    return string
    

def __formatNoSelection(string_input):
    return "(No Selection)\n" if not string_input else string_input

def chooseBreads(bread_list):
    return (
        "🥖 (1/7) BREADS\n"
        "\n"
        "Sure, next please pick a bread?\n"
        "{}".format(__convertListToNumberedString(bread_list))
    )

def chooseMains(main_list):
    return (
        "🍗 (2/7) MAINS\n"
        "\n"
        "Okay awesome, now which main?\n"
        "{}".format(__convertListToNumberedString(main_list))
    )

def chooseVeggies(veggie_list):
    return (
        "🥗 (3/7) VEGGIES\n"
        "\n"
        "Great, now please select all veggies you want!\n"
        "{}".format(__convertListToNumberedString(veggie_list))
    )

def chooseSauces(sauce_list):
    return (
        "💬 (4/7) SAUCES\n"
        "\n"
        "Do you want any sauces with that? \n"
        "{}".format(__convertListToNumberedString(sauce_list))
    )

def chooseAddOn(addon_list):
    return (
        "🥑 (5/7) ADD-ONS\n"
        "\n"
        "We're almost done! Do you want any add ons?\n"
        "{}".format(__convertListToNumberedString(addon_list))
    )

def chooseSides(side_list):
    return (
        "🍪 (6/7) SIDES\n"
        "\n"
        "Okay, how about some sides?\n"
        "{}".format(__convertListToNumberedString(side_list))
    )

def chooseDrinks(drink_list):
    return (
        "🥤 (7/7) DRINKS\n"
        "\n"
        "Final question 🎉 Do you want a drink with that?\n"
        "{}".format(__convertListToNumberedString(drink_list))
    )

def showWelcomeMsg(meal_list, restart=False):
    meal_list_string = __convertListToNumberedString(meal_list)

    if (restart):
        return (
            "Hi again! Looks like someone's extra hungry today 😊\n\n"
            "Let's get started, what can we get you?\n"
            "{}".format(meal_list_string)
        )
    else:
        return (
            "Hi there, Welcome to Subway! 😊\n\n"
            "What can we get you today?\n"
            "{}".format(meal_list_string)
        )

def showOrderSummary(meals, breads, mains, veggies, sauces, topups, sides, drinks):
    return (
        "🍽️ Okay awesome! Let me repeat your order for you:\n\n"
        "<b>Subway Meal</b>\n"
        "{meals}\n"
        "<b>Selected Bread</b>\n"
        "{breads}\n"
        "<b>Main</b>\n"
        "{mains}\n"
        "<b>Veggies</b>\n"
        "{veggies}\n"
        "<b>Sauces</b>\n"
        "{sauces}\n"
        "<b>Add Ons</b>\n"
        "{topups}\n"
        "<b>Sides</b>\n"
        "{sides}\n"
        "<b>Drinks</b>\n"
        "{drinks}\n"
        
    ).format(
        meals=__formatNoSelection(__convertListToNumberedString(meals)), 
        breads=__formatNoSelection(__convertListToNumberedString(breads)), 
        mains=__formatNoSelection(__convertListToNumberedString(mains)), 
        veggies=__formatNoSelection(__convertListToNumberedString(veggies)), 
        sauces=__formatNoSelection(__convertListToNumberedString(sauces)), 
        topups=__formatNoSelection(__convertListToNumberedString(topups)), 
        sides=__formatNoSelection(__convertListToNumberedString(sides)),
        drinks=__formatNoSelection(__convertListToNumberedString(drinks))
    )

# Instantiate Telegram Bot  
class TelegramBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__(*args, **kwargs)
        self.prolog = PrologInterface()
        self.question_lists = ['meals', 'breads', 'mains', 'veggies', 'sauces', 'topups', 'sides', 'drinks']
        self.counter = 0


    def __restart(self):
      self.prolog = PrologInterface()
      self.counter = 0


    async def __updateCounter(self):
        next_question = self.question_lists[self.counter + 1]
        if self.prolog.available_options(next_question):
            self.counter += 1
        else:
            self.counter += 2


    async def __ask(self, id, bot, question):
        if question == 'meals':
            meals = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
                id, 
                 showWelcomeMsg(
                    meal_list=meals, 
                    restart=False
                ),
                reply_markup=showKeyboard(meals)
            )

        elif question == 'breads':
            breads = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseBreads(bread_list=breads),
              reply_markup=showKeyboard(breads)
            )

        elif question == 'mains':
            mains = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseMains(main_list=mains),
              reply_markup=showKeyboard(mains)
            )

        elif question == 'veggies':
            veggies = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseVeggies(veggie_list=veggies),
              reply_markup=showKeyboard(veggies, add_skip=True)
            )

        elif question == 'sauces':
            sauces = self.prolog.selectable_input_options(question)
            
            await bot.sendMessage(
              id, 
               chooseSauces(sauce_list=sauces),
              reply_markup=showKeyboard(sauces, add_skip=True)
            )

        elif question == 'topups':
            topups = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseAddOn(addon_list=topups),
              reply_markup=showKeyboard(topups, add_skip=True)
            )

        elif question == 'sides':
            sides = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseSides(side_list=sides),
              reply_markup=showKeyboard(sides, add_skip=True)
            )

        elif question == 'drinks':
            drinks = self.prolog.selectable_input_options(question)

            await bot.sendMessage(
              id, 
               chooseDrinks(drink_list=drinks),
              reply_markup=showKeyboard(drinks)
            )

        else:
            await bot.sendMessage(
              id, 
               showOrderSummary(
                meals=self.prolog.selected_options("meals"),
                breads=self.prolog.selected_options("breads"), 
                mains=self.prolog.selected_options("mains"), 
                veggies=self.prolog.selected_options("veggies"), 
                sauces=self.prolog.selected_options("sauces"), 
                topups=self.prolog.selected_options("topups"), 
                sides=self.prolog.selected_options("sides"),
                drinks=self.prolog.selected_options("drinks")
              ),
              reply_markup=ReplyKeyboardRemove(),
              parse_mode='HTML'
            )
            await bot.sendMessage(
              id, "Preparing your order now!"
            )
            await bot.sendDocument(
              id, document=open('assets/thank_you.gif', 'rb')
            )
            await bot.sendMessage(
              id, "Enjoy your meal! Hope to see you back soon"
            )
            await bot.sendMessage(
              id, "Want to start a new order? Click /restart"
            )


    async def on_chat_message(self, msg):
        _, _, id = telepot.glance(msg)

        if msg['text'] == '/start':
            self.__restart()
            await self.__ask(id, bot, self.question_lists[self.counter])

        elif msg['text'] == '/restart':
            self.__restart()
            meals = self.prolog.available_options("meals")
            
            await bot.sendMessage(
                id, 
                 showWelcomeMsg(
                    meal_list=meals, 
                    restart=True
                ),
                reply_markup=showKeyboard(meals)
            )

        else:
            user_input = msg['text'].lower().replace(" ", "_")

            if user_input not in self.prolog.all_options("drinks"):
                if "skip" in user_input:
                    await self.__updateCounter()
                
                elif user_input in self.prolog.all_options("meals"):
                    self.prolog.add_meal(user_input)

                    await self.__updateCounter()

                elif user_input in self.prolog.all_options("breads"):
                    self.prolog.add_bread(user_input)

                    await self.__updateCounter()

                elif user_input in self.prolog.all_options("mains"):
                    self.prolog.add_main(user_input)

                    await self.__updateCounter()

                elif user_input in self.prolog.all_options("veggies"):
                    self.prolog.add_veggie(user_input)
                    
                    if not self.prolog.selectable_input_options("veggies"):
                        await self.__updateCounter()
                    
                elif user_input in self.prolog.all_options("sauces"):
                    self.prolog.add_sauce(user_input)

                    if not self.prolog.selectable_input_options("sauces"):
                        await self.__updateCounter()
                        
                elif user_input in self.prolog.all_options("topups"):
                    self.prolog.add_topup(user_input)

                    if not self.prolog.selectable_input_options("topups"):
                        await self.__updateCounter()
                        
                elif user_input in self.prolog.all_options("sides"):
                    self.prolog.add_side(user_input)

                    if not self.prolog.selectable_input_options("sides"):
                        await self.__updateCounter()
                        
                await self.__ask(id, bot, self.question_lists[self.counter])

            else:
                self.prolog.add_drink(user_input)
                await self.__ask(id, bot, None)
          

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, TelegramBot, timeout=500),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Starting Telegram Bot ...')

loop.run_forever()

