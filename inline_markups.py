from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#  SUBSCRIBE

subscribe_inline = InlineKeyboardMarkup()
subscribe_inline.row(InlineKeyboardButton(text = 'Канал 1', url = 'https://t.me/+EQMzXTCJj-w4ZGZi'))
subscribe_inline.row(InlineKeyboardButton(text = 'Канал 2', url = 'https://t.me/+K2uSQQ6ufyJlOTFi'))
subscribe_inline.row(InlineKeyboardButton(text = 'Проверить  ✅', callback_data = 'check'))



#  CHAT

chat_inline = InlineKeyboardMarkup()
chat_inline.row(InlineKeyboardButton(text = 'Перейти в чат', url = 'https://t.me/+uHPwQOJPeAowNTAy'))



#  NEW TRACKS

week_17 = InlineKeyboardMarkup()
week_17.row(InlineKeyboardButton(text = 'Aarne feat. Big Baby Tape - 4 ur girl', callback_data = 'track_171'))
week_17.row(InlineKeyboardButton(text = 'CHEBANOV feat. Асия - Огни Москвы', callback_data = 'track_172'))
week_17.row(InlineKeyboardButton(text = 'Guf feat. A.V.G - Спонсор Твоих Проблем', callback_data = 'track_173'))
week_17.row(InlineKeyboardButton(text = 'HENSY - Монолог', callback_data = 'track_174'))
week_17.row(InlineKeyboardButton(text = 'OBLADAET - Britney', callback_data = 'track_175'))
week_17.row(InlineKeyboardButton(text = 'Ramil\', MACAN - Не играй в любовь', callback_data = 'track_176'))
week_17.row(InlineKeyboardButton(text = 'Zivert - НАД КРЫШАМИ', callback_data = 'track_177'))
week_17.row(InlineKeyboardButton(text = 'Алёна Швец. - Обидно', callback_data = 'track_178'))
week_17.row(InlineKeyboardButton(text = 'Люся Чеботина - ПСЕВДОМОДЕЛИ', callback_data = 'track_179'))
week_17.row(InlineKeyboardButton(text = 'Тима Акимов - Космонавт', callback_data = 'track_180'))
week_17.row(InlineKeyboardButton(text = 'Вперёд >>', callback_data = 'next_week_16'))


week_16 = InlineKeyboardMarkup()
week_16.row(InlineKeyboardButton(text = 'ANNA ASTI - Дурак', callback_data = 'track_161'))
week_16.row(InlineKeyboardButton(text = 'AUGUST feat. MAYOT - Every Day', callback_data = 'track_162'))
week_16.row(InlineKeyboardButton(text = 'Aarne, uglystephan - Клянусь', callback_data = 'track_163'))
week_16.row(InlineKeyboardButton(text = 'DZHARO - Бесконечность', callback_data = 'track_164'))
week_16.row(InlineKeyboardButton(text = 'Heronwater - 2 часа ночи', callback_data = 'track_165'))
week_16.row(InlineKeyboardButton(text = 'Kamazz feat. NLO - Большие Города', callback_data = 'track_166'))
week_16.row(InlineKeyboardButton(text = 'Levandowskiy, Гио Пика - Вена-Париж', callback_data = 'track_167'))
week_16.row(InlineKeyboardButton(text = 'Niletto & Goshu - Ты чё такая смелая', callback_data = 'track_168'))
week_16.row(InlineKeyboardButton(text = 'ПАБЛО & Mr Lambo - Чилим', callback_data = 'track_169'))
week_16.row(InlineKeyboardButton(text = 'Тима Акимов - Точно да', callback_data = 'track_170'))
week_16.row(InlineKeyboardButton(text = '<< Назад', callback_data = 'back_week_17'),
            InlineKeyboardButton(text = 'Вперёд >>', callback_data = 'next_week_15'))


week_15 = InlineKeyboardMarkup()
week_15.row(InlineKeyboardButton(text = "MACAN, Jakone - Поспешили", callback_data = "track_151"))
week_15.row(InlineKeyboardButton(text = "A.V.G - Я плачу", callback_data = "track_152"))
week_15.row(InlineKeyboardButton(text = "Винтаж, ТРАВМА, SKIDRI, DVRKLXGHT - Плохая Девочка", callback_data = "track_153"))
week_15.row(InlineKeyboardButton(text = "Konfuz, The Limba - Ты и Я", callback_data = "track_154"))
week_15.row(InlineKeyboardButton(text = "ANNA ASTI - Царица", callback_data = "track_155"))
week_15.row(InlineKeyboardButton(text = "NILETTO - Летний дождь", callback_data = "track_156"))
week_15.row(InlineKeyboardButton(text = "MONA - Верю в любовь", callback_data = "track_157"))
week_15.row(InlineKeyboardButton(text = "VERBEE - Обнимай", callback_data = "track_158"))
week_15.row(InlineKeyboardButton(text = "GORO - Во мне столько любви", callback_data = "track_159"))
week_15.row(InlineKeyboardButton(text = "A.V.G. Goro - Она близко", callback_data = "track_160"))
week_15.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_16"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_14"))


week_14 = InlineKeyboardMarkup()
week_14.row(InlineKeyboardButton(text = "ANNA ASTI - Царица", callback_data = "track_141"))
week_14.row(InlineKeyboardButton(text = "Miyagi & Эндшпиль - Bounty", callback_data = "track_142"))
week_14.row(InlineKeyboardButton(text = "Ислам Итляшев - Довела", callback_data = "track_143"))
week_14.row(InlineKeyboardButton(text = "MACAN - Самый пьяный округ в мире", callback_data = "track_144"))
week_14.row(InlineKeyboardButton(text = "MAYOT - Мотылёк", callback_data = "track_145"))
week_14.row(InlineKeyboardButton(text = "Баста - Девочка-самурай", callback_data = "track_146"))
week_14.row(InlineKeyboardButton(text = "NLO - Молодость для тус", callback_data = "track_147"))
week_14.row(InlineKeyboardButton(text = "XOLIDAYBOY - Малышка хочет движа", callback_data = "track_148"))
week_14.row(InlineKeyboardButton(text = "МУККА - Бурями", callback_data = "track_149"))
week_14.row(InlineKeyboardButton(text = "Xcho - Музыка в ночи", callback_data = "track_150"))
week_14.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_15"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_13"))


week_13 = InlineKeyboardMarkup()
week_13.row(InlineKeyboardButton(text = "Markul, FEDUK - Мятный", callback_data = "track_131"))
week_13.row(InlineKeyboardButton(text = "Wildways, Mary Gu - Я тебя тоже", callback_data = "track_132"))
week_13.row(InlineKeyboardButton(text = "Ваня Дмитренко, Моя Мишель - Рыбка", callback_data = "track_133"))
week_13.row(InlineKeyboardButton(text = "ЕГОР НАТС - ОЧЕНЬ СКУЧАЮ", callback_data = "track_134"))
week_13.row(InlineKeyboardButton(text = "Канги - Ой", callback_data = "track_135"))
week_13.row(InlineKeyboardButton(text = "NЮ - Улыбашка", callback_data = "track_136"))
week_13.row(InlineKeyboardButton(text = "Чина - Дерзкая", callback_data = "track_137"))
week_13.row(InlineKeyboardButton(text = "Kambulat - Марокканка", callback_data = "track_138"))
week_13.row(InlineKeyboardButton(text = "GUMA, Dyce - Бронежилет", callback_data = "track_139"))
week_13.row(InlineKeyboardButton(text = "Артур Пирожков - Позитив", callback_data = "track_140"))
week_13.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_14"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_12"))


week_12 = InlineKeyboardMarkup()
week_12.row(InlineKeyboardButton(text = "Кравц, Гио Пика - Где прошла ты", callback_data = "track_121"))
week_12.row(InlineKeyboardButton(text = "kizaru - Зеркало", callback_data = "track_122"))
week_12.row(InlineKeyboardButton(text = "Jakone, SCIRENA - По весне", callback_data = "track_123"))
week_12.row(InlineKeyboardButton(text = "MACAN, SCIRENA - IVL", callback_data = "track_124"))
week_12.row(InlineKeyboardButton(text = "MACAN - ASPHALT 8", callback_data = "track_125"))
week_12.row(InlineKeyboardButton(text = "Pepel Nahudi - Заново завоевать", callback_data = "track_126"))
week_12.row(InlineKeyboardButton(text = "A.V.G, Goro - Она близко", callback_data = "track_127"))
week_12.row(InlineKeyboardButton(text = "NLO - Танцы", callback_data = "track_128"))
week_12.row(InlineKeyboardButton(text = "SOSKA 69 - Чёрная машина", callback_data = "track_129"))
week_12.row(InlineKeyboardButton(text = "ANNA ASTI - Верю в тебя", callback_data = "track_130"))
week_12.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_13"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_11"))


week_11 = InlineKeyboardMarkup()
week_11.row(InlineKeyboardButton(text = "Miyagi & Эншпиль - По полям", callback_data = "track_111"))
week_11.row(InlineKeyboardButton(text = "Konfuz - Тише", callback_data = "track_112"))
week_11.row(InlineKeyboardButton(text = "HammAli & Navai - Ноты", callback_data = "track_113"))
week_11.row(InlineKeyboardButton(text = "MONA, Баста - Ты так мне необходим", callback_data = "track_114"))
week_11.row(InlineKeyboardButton(text = "Armich - Смесь", callback_data = "track_115"))
week_11.row(InlineKeyboardButton(text = "blago white, LOVV66 - Выше", callback_data = "track_116"))
week_11.row(InlineKeyboardButton(text = "KARA KROSS, MANIL - Чёртово колесо", callback_data = "track_117"))
week_11.row(InlineKeyboardButton(text = "Sqwore - Детство", callback_data = "track_118"))
week_11.row(InlineKeyboardButton(text = "Три Дня Дождя - За Край", callback_data = "track_119"))
week_11.row(InlineKeyboardButton(text = "луни ана - DO U CALL ME", callback_data = "track_120"))
week_11.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_12"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_10"))


week_10 = InlineKeyboardMarkup()
week_10.row(InlineKeyboardButton(text = "GUMA, КУОК - Притяжение", callback_data = "track_101"))
week_10.row(InlineKeyboardButton(text = "Элджей - Изиранеры", callback_data = "track_102"))
week_10.row(InlineKeyboardButton(text = "HammAli & Navai - Засыпай, Красавица", callback_data = "track_103"))
week_10.row(InlineKeyboardButton(text = "Mr Lambo, Xcho - Roles", callback_data = "track_104"))
week_10.row(InlineKeyboardButton(text = "ЕГОР НАТС, М - ВЫДОХНИ", callback_data = "track_105"))
week_10.row(InlineKeyboardButton(text = "Basiaga - Валим", callback_data = "track_106"))
week_10.row(InlineKeyboardButton(text = "Dabro - Надо повторить", callback_data = "track_107"))
week_10.row(InlineKeyboardButton(text = "Andro - Дай мне только шанс", callback_data = "track_108"))
week_10.row(InlineKeyboardButton(text = "Boilevard Depo - ДА", callback_data = "track_109"))
week_10.row(InlineKeyboardButton(text = "Люся Чеботина - ProОзеро", callback_data = "track_110"))
week_10.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_11"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_9"))


week_9 = InlineKeyboardMarkup()
week_9.row(InlineKeyboardButton(text = "Джиган feat. VACÍO, MAYOT - Танцуй со мной", callback_data = "track_91"))
week_9.row(InlineKeyboardButton(text = "алёна швец. - Спи", callback_data = "track_92"))
week_9.row(InlineKeyboardButton(text = "DZHARO - Cлед", callback_data = "track_93"))
week_9.row(InlineKeyboardButton(text = "JABO feat. Konfuz - МНОГО РАЗ", callback_data = "track_94"))
week_9.row(InlineKeyboardButton(text = "17 SEVENTEEN - Для тебя и для меня", callback_data = "track_95"))
week_9.row(InlineKeyboardButton(text = "Гуф - Про пуделя", callback_data = "track_96"))
week_9.row(InlineKeyboardButton(text = "Rakhim - Look At Me Habibi", callback_data = "track_97"))
week_9.row(InlineKeyboardButton(text = "Эллаи - Набери", callback_data = "track_98"))
week_9.row(InlineKeyboardButton(text = "UBEL - Никогда-нибудь", callback_data = "track_99"))
week_9.row(InlineKeyboardButton(text = "Idris & Leos - Первой не пиши", callback_data = "track_100"))
week_9.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_10"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_8"))


week_8 = InlineKeyboardMarkup()
week_8.row(InlineKeyboardButton(text = "104, Скриптонит - BITCH", callback_data = "track_81"))
week_8.row(InlineKeyboardButton(text = "10AGE, Шура - Зима", callback_data = "track_82"))
week_8.row(InlineKeyboardButton(text = "ANNA ASTI - Звенит январская вьюга", callback_data = "track_83"))
week_8.row(InlineKeyboardButton(text = "Konfuz - Скучаю", callback_data = "track_84"))
week_8.row(InlineKeyboardButton(text = "Kristina Si - Твой мир", callback_data = "track_85"))
week_8.row(InlineKeyboardButton(text = "MAYOT - 4", callback_data = "track_86"))
week_8.row(InlineKeyboardButton(text = "OBLADAET - MONSTER TRAKK", callback_data = "track_87"))
week_8.row(InlineKeyboardButton(text = "The Limba, JONY, ЕГОР КРИД, А4 - Новогодняя песня", callback_data = "track_88"))
week_8.row(InlineKeyboardButton(text = "i61 - SUBMOSCOW SWAG", callback_data = "track_89"))
week_8.row(InlineKeyboardButton(text = "Милана Хаметова, DAVA - НОВОГОДНЯЯ", callback_data = "track_90"))
week_8.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_9"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_7"))


week_7 = InlineKeyboardMarkup()
week_7.row(InlineKeyboardButton(text = "PHARAOH - Соната Ей", callback_data = "track_71"))
week_7.row(InlineKeyboardButton(text = "JONY, ANNA ASTi - Как любовь твою понять?", callback_data = "track_72"))
week_7.row(InlineKeyboardButton(text = "kizaru - Тебя любят там где меня нет", callback_data = "track_73"))
week_7.row(InlineKeyboardButton(text = "Баста, FEDUK - Времени нет", callback_data = "track_74"))
week_7.row(InlineKeyboardButton(text = "Элджей - Форрест Гамп", callback_data = "track_75"))
week_7.row(InlineKeyboardButton(text = "SODA LUV - DTF", callback_data = "track_76"))
week_7.row(InlineKeyboardButton(text = "Ольга Серябкина - Эта зима", callback_data = "track_77"))
week_7.row(InlineKeyboardButton(text = "104 feat. Hey Monro - Куртка", callback_data = "track_78"))
week_7.row(InlineKeyboardButton(text = "Mary Gu, MAYOT - Два выстрела", callback_data = "track_79"))
week_7.row(InlineKeyboardButton(text = "ST - Воспоминания", callback_data = "track_80"))
week_7.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_8"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_6"))


week_6 = InlineKeyboardMarkup()
week_6.row(InlineKeyboardButton(text = "Big Baby Tape faet. Young Moscow - Мой Белый", callback_data = "track_61"))
week_6.row(InlineKeyboardButton(text = "Смоки Мо, Murovei, Guf, Ноггано - OZZY", callback_data = "track_62"))
week_6.row(InlineKeyboardButton(text = "10AGE - Б.О.М.Ж", callback_data = "track_63"))
week_6.row(InlineKeyboardButton(text = "DenDerty, ЛСП - Мрак", callback_data = "track_64"))
week_6.row(InlineKeyboardButton(text = "NILETTO - Летуаль", callback_data = "track_65"))
week_6.row(InlineKeyboardButton(text = "VESNA305 - Ты не мечтай даже", callback_data = "track_66"))
week_6.row(InlineKeyboardButton(text = "МОТ - Снова МОТ Стелет", callback_data = "track_67"))
week_6.row(InlineKeyboardButton(text = "Артем Качер - Пока ты с ним", callback_data = "track_68"))
week_6.row(InlineKeyboardButton(text = "Luverance - Океаны", callback_data = "track_69"))
week_6.row(InlineKeyboardButton(text = "Bahh Tee, Turken - Фантазия", callback_data = "track_70"))
week_6.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_7"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_5"))


week_5 = InlineKeyboardMarkup()
week_5.row(InlineKeyboardButton(text = "ANNA ASTI - Ночью на кухне", callback_data = "track_51"))
week_5.row(InlineKeyboardButton(text = "Три дня дождя - Подозрительно", callback_data = "track_52"))
week_5.row(InlineKeyboardButton(text = "MACAN - Плачь, но не звони", callback_data = "track_53"))
week_5.row(InlineKeyboardButton(text = "Белый шум, Баста - Белый шум", callback_data = "track_54"))
week_5.row(InlineKeyboardButton(text = "Kambulat - Тынгла", callback_data = "track_55"))
week_5.row(InlineKeyboardButton(text = "Джизус - На удачу", callback_data = "track_56"))
week_5.row(InlineKeyboardButton(text = "DZHARO - ROCKSTAR", callback_data = "track_57"))
week_5.row(InlineKeyboardButton(text = "Rakhim, Andro - Разожги во мне огонь", callback_data = "track_58"))
week_5.row(InlineKeyboardButton(text = "VACIO - Фотик", callback_data = "track_59"))
week_5.row(InlineKeyboardButton(text = "Mr Lambo, Пабло - Авансы", callback_data = "track_60"))
week_5.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_6"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_4"))


week_4 = InlineKeyboardMarkup()
week_4.row(InlineKeyboardButton(text = "Ёлка - Снова", callback_data = "track_41"))
week_4.row(InlineKeyboardButton(text = "FEDUK - Ябеда", callback_data = "track_42"))
week_4.row(InlineKeyboardButton(text = "zoloto - непроизошло", callback_data = "track_43"))
week_4.row(InlineKeyboardButton(text = "Kambulat - Это Любовь", callback_data = "track_44"))
week_4.row(InlineKeyboardButton(text = "Rydm City, Скриптонит - Solo Tu", callback_data = "track_45"))
week_4.row(InlineKeyboardButton(text = "HOLLYFLAME - За твоим домом", callback_data = "track_46"))
week_4.row(InlineKeyboardButton(text = "Лали, МУККА - Будильник", callback_data = "track_47"))
week_4.row(InlineKeyboardButton(text = "LIZER - Дерзко", callback_data = "track_48"))
week_4.row(InlineKeyboardButton(text = "XOLIDAYBOY - Моя Хулиганка", callback_data = "track_49"))
week_4.row(InlineKeyboardButton(text = "Джизус - Твои Глаза", callback_data = "track_50"))
week_4.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_5"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_3"))


week_3 = InlineKeyboardMarkup()
week_3.row(InlineKeyboardButton(text = "Коста Лакоста, Элджей - Бронежилет", callback_data = "track_31"))
week_3.row(InlineKeyboardButton(text = "Ramil' - Просто Лети", callback_data = "track_32"))
week_3.row(InlineKeyboardButton(text = "LIZER - Не Герой", callback_data = "track_33"))
week_3.row(InlineKeyboardButton(text = "Мари Краймбрери - Не Буди Меня", callback_data = "track_34"))
week_3.row(InlineKeyboardButton(text = "BATO, Boulevard Depo - Улицы", callback_data = "track_35"))
week_3.row(InlineKeyboardButton(text = "Padillion, Thomas Mraz - Серебрянный Сёрфер", callback_data = "track_36"))
week_3.row(InlineKeyboardButton(text = "MAYOT, GUF - SUMMERTIME", callback_data = "track_37"))
week_3.row(InlineKeyboardButton(text = "МОТ - Любовь как спецэффект", callback_data = "track_38"))
week_3.row(InlineKeyboardButton(text = "TONI, Andro - Соври", callback_data = "track_39"))
week_3.row(InlineKeyboardButton(text = "Yanix, SODA LUV - Badass", callback_data = "track_40"))
week_3.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_4"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_2"))


week_2 = InlineKeyboardMarkup()
week_2.row(InlineKeyboardButton(text = "Ваня Дмитренко, Григорий Лепс - Бейби", callback_data = "track_21"))
week_2.row(InlineKeyboardButton(text = "Ислам Итляшев - Ресторан", callback_data = "track_22"))
week_2.row(InlineKeyboardButton(text = "ELMAN, Andro - Круз", callback_data = "track_23"))
week_2.row(InlineKeyboardButton(text = "Люся Чеботина - ПЛАКАЛ ГОЛЛИВУД", callback_data = "track_24"))
week_2.row(InlineKeyboardButton(text = "Dabro - Мне не страшно", callback_data = "track_25"))
week_2.row(InlineKeyboardButton(text = "Kambulat - Пасмурно", callback_data = "track_26"))
week_2.row(InlineKeyboardButton(text = "Oxxxymiron - ОЙДА", callback_data = "track_27"))
week_2.row(InlineKeyboardButton(text = "JONY - Никак", callback_data = "track_28"))
week_2.row(InlineKeyboardButton(text = "Akmal' - Приснись", callback_data = "track_29"))
week_2.row(InlineKeyboardButton(text = "MUJEVA - Чёрный мерседес", callback_data = "track_30"))
week_2.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_3"),
            InlineKeyboardButton(text = "Вперёд >>", callback_data = "next_week_1"))


week_1 = InlineKeyboardMarkup()
week_1.row(InlineKeyboardButton(text = "ЕГОР КРИД feat. Михаил Шуфутинский - 3-е Сентября", callback_data = "track_11"))
week_1.row(InlineKeyboardButton(text = "VACÍO, MORGENSHTERN - Притон", callback_data = "track_12"))
week_1.row(InlineKeyboardButton(text = "КОСМОНАВТОВ НЕТ - холодная осень", callback_data = "track_13"))
week_1.row(InlineKeyboardButton(text = "GAYAZOV$ BROTHER$ - Спасай мою пятницу", callback_data = "track_14"))
week_1.row(InlineKeyboardButton(text = "blago white - VNATURI", callback_data = "track_15"))
week_1.row(InlineKeyboardButton(text = "Тима Акимов - Пролетело лето", callback_data = "track_16"))
week_1.row(InlineKeyboardButton(text = "The Limba - Не больно", callback_data = "track_17"))
week_1.row(InlineKeyboardButton(text = "PINQ, MAYOT, YUNGWAY, LOVV66, Scally Milano, uglystephan - Эстакада", callback_data = "track_18"))
week_1.row(InlineKeyboardButton(text = "ЛСП - Сектор Приз", callback_data = "track_19"))
week_1.row(InlineKeyboardButton(text = "Rakhim - Golden Chain", callback_data = "track_20"))
week_1.row(InlineKeyboardButton(text = "<< Назад", callback_data = "back_week_2"))



#  FORWARD LINK

link_inline = InlineKeyboardMarkup()
link_inline.row(InlineKeyboardButton(text = 'Бустить 🚀', url = 'http://t.me/hittt_music?boost'))



#  AD BUTTONS

shx_inline = InlineKeyboardMarkup()
shx_inline.row(InlineKeyboardButton('✅  Записаться на пробный урок', url = 'https://t.me/ShaHriXMusic'))












