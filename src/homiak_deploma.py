#@bot.message_handler(commands=["self_photo"])
#def user_photo(message):
    #photo = bot.get_user_profile_photos(message.from_user.id)
    #bot.send_photo(message.chat.id, photo.photos[0][2].file_id)
#Где 0 - первая или же основная фотография в профиле, 2 - размер аватарки (постоянная нумерация 0..2, от меньшего к большему). Код не оптимизирован к её отсутствию.