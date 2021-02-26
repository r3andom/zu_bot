import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='')
dispatcher = updater.dispatcher
job_queue = updater.job_queue

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Buongiorno, stronzo!')

def echo(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Che cazzo vuoi?')

def time(update, context):
    import time

    epoch_time = time.time()
    local_time = time.localtime(epoch_time)

    second = local_time.tm_sec
    minute = local_time.tm_min
    hour = local_time.tm_hour
    day = local_time.tm_mday
    month = local_time.tm_mon
    year = local_time.tm_year

    if second < 10:
        second = '0' + str(second)
    
    if minute < 10:
        minute = '0' + str(minute)

    text_time = ('Sono le {}:{}:{} del {}/{}/{}, coglione.'.format(hour, minute, second, day, month, year))
    
    context.bot.send_message(chat_id = update.effective_chat.id, text = text_time)

def alarm(update, context):
    import time
    
    text_alarm = context.args
    
    if len(text_alarm) == 2:
        try:
            hour_alarm = int(text_alarm[0])
            minute_alarm = int(text_alarm[1])
        
            if hour_alarm > -1 and hour_alarm < 24 and minute_alarm > -1 and minute_alarm < 60:
                
                if hour_alarm < 10:
                    hour_text = '0' + str(hour_alarm)
                else:
                    hour_text = str(hour_alarm)
                    
                if minute_alarm < 10:
                    minute_text = '0' + str(minute_alarm)
                else:
                    minute_text = str(minute_alarm)
                    
                message_alarm = 'Vuoi che ti svegli alle {}:{}?'.format(hour_text, minute_text)
                context.bot.send_message(chat_id = update.effective_chat.id, text = message_alarm)
                context.bot.send_message(chat_id = update.effective_chat.id, text = 'Col cazzo, non sono tua madre.')
                
            else:
                context.bot.send_message(chat_id = update.effective_chat.id, text = 'I numeri che mi hai dato non hanno senso.')
        
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text='Se vuoi che funzioni scrivi /alarm e la data nel formato HH MM, con lo spazio in mezzo, sennò attaccati a sto cazzo.')
        
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text='Se vuoi che funzioni scrivi /alarm e la data nel formato HH MM, con lo spazio in mezzo, sennò attaccati a sto cazzo')

def wisdom(update, context):
    context.bot.send_voice(chat_id = update.effective_chat.id, voice = open('media/grande_massima.ogg', 'rb'))


def wisdom_message(context: CallbackContext):
    context.bot.send_voice(chat_id = context.job.context, voice = open('media/grande_massima.ogg', 'rb'))

def wisdom_reminder(update: telegram.Update, context):
    import datetime

    try:
        hour = int(context.args[0])
        minute = int(context.args[1])

        if hour == 0:
            hour = 23
        else:
            hour = hour - 1
        
        date = datetime.time(hour, minute)
        context.job_queue.run_daily(wisdom_message, date, context=update.message.chat_id)
    
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Se vuoi che funzioni scrivi /enlight e l\'ora nel formato HH MM, con lo spazio in mezzo, sennò attaccati a sto cazzo.')

def timer_message(context: CallbackContext):
    context.bot.send_message(chat_id = context.job.context, text = ':..::..:\n   ::')

def set_timer(update: telegram.Update, context):
    
    try:
        second = int(context.args[0])
        
        if second >= 0:
            context.job_queue.run_once(timer_message, second, context = update.message.chat_id)

        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = 'Ma secondo te ha senso un timer negativo?')

    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Per il /timer devi darmi un numero intero per i secondi e niente altro.')

def god_reveal(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = open('media/god.jpg', 'rb'))
    
def satan_reveal(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = open('media/satan.jpg', 'rb'))

def unknown(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Non rompere, non so fare altro.')

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
time_handler = CommandHandler('time', time)
alarm_handler = CommandHandler('alarm', alarm)
wisdom_handler = CommandHandler('wisdom', wisdom)
enlight_handler = CommandHandler('enlight', wisdom_reminder)
timer_handler = CommandHandler('timer', set_timer)
god_handler = CommandHandler('god', god_reveal)
satan_handler = CommandHandler('satan', satan_reveal)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler) 
dispatcher.add_handler(time_handler)
dispatcher.add_handler(alarm_handler)
dispatcher.add_handler(wisdom_handler)
dispatcher.add_handler(enlight_handler)
dispatcher.add_handler(timer_handler)
dispatcher.add_handler(god_handler)
dispatcher.add_handler(satan_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
