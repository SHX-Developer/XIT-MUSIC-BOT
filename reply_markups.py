from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



#  ADMIN PANNEL

admin_reply = ReplyKeyboardMarkup(resize_keyboard = True)
admin_reply.row('Рассылка текста')
admin_reply.row('Рассылка трека')
admin_reply.row('🏠  Главное меню')



#  MENU

menu_reply = ReplyKeyboardMarkup(resize_keyboard = True)
menu_reply.row('🎙 Новинки', '🔍', '🔥 Ремиксы')
menu_reply.row('📝  Чат','📂  Плейлист')



#  REMIX LANGUAGES

remix_language_reply = ReplyKeyboardMarkup(resize_keyboard = True)
remix_language_reply.row('🇷🇺  Русские', '🇺🇸  Английские')
remix_language_reply.row('🏠  Главное меню')



#  CANCEL

cancel_reply = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_reply.row('Отменить')



#  BACK

back_reply = ReplyKeyboardMarkup(resize_keyboard = True)
back_reply.row("⬅  Назад")



#  MAIN MENU

main_menu_reply = ReplyKeyboardMarkup(resize_keyboard = True)
main_menu_reply.row('🏠  Главное меню')



#  RUSSIAN ARTISTS

#  FIRST PAGE
first_russian_artists_reply = ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
first_russian_artists_reply.row("⬅   Назад", "🏠  Главное меню")
FirstPageRussianArtistsButton1 = KeyboardButton("ADON MIX")
FirstPageRussianArtistsButton2 = KeyboardButton("AHMED SHAD")
FirstPageRussianArtistsButton134 = KeyboardButton("AKMAL'")
FirstPageRussianArtistsButton3 = KeyboardButton("AL FAKHER")
FirstPageRussianArtistsButton4 = KeyboardButton("ALEKS ATAMAN")
FirstPageRussianArtistsButton136 = KeyboardButton("AMIRCHIK")
FirstPageRussianArtistsButton5 = KeyboardButton("ANDRO")
FirstPageRussianArtistsButton6 = KeyboardButton("ANDY PANDA")
FirstPageRussianArtistsButton7 = KeyboardButton("ANNA ASTI")
FirstPageRussianArtistsButton8 = KeyboardButton("AQUANEON")
FirstPageRussianArtistsButton124 = KeyboardButton("AQUARIUMS")
FirstPageRussianArtistsButton9 = KeyboardButton("ARKUSHA")
FirstPageRussianArtistsButton10 = KeyboardButton("AVG")
FirstPageRussianArtistsButton11 = KeyboardButton("BAKR")
FirstPageRussianArtistsButton123 = KeyboardButton("BAGARDI")
FirstPageRussianArtistsButton12 = KeyboardButton("BITTUEV")
FirstPageRussianArtistsButton13 = KeyboardButton("BODIEV")
FirstPageRussianArtistsButton112 = KeyboardButton("BOLIN")
FirstPageRussianArtistsButton101 = KeyboardButton("BUDA")
FirstPageRussianArtistsButton14 = KeyboardButton("BY ИНДИЯ")
FirstPageRussianArtistsButton105 = KeyboardButton("BYLIK")
FirstPageRussianArtistsButton15 = KeyboardButton("CHRIS YANK")
FirstPageRussianArtistsButton16 = KeyboardButton("CVETOCEK7")
FirstPageRussianArtistsButton17 = KeyboardButton("CYGO")
FirstPageRussianArtistsButton18 = KeyboardButton("DANNY ABRO")
FirstPageRussianArtistsButton19 = KeyboardButton("DAREEM")
FirstPageRussianArtistsButton127 = KeyboardButton("DEESMI")
FirstPageRussianArtistsButton102 = KeyboardButton("DIOR")
FirstPageRussianArtistsButton103 = KeyboardButton("DJ SMASH")
FirstPageRussianArtistsButton20 = KeyboardButton("DMA ILLAN")
FirstPageRussianArtistsButton21 = KeyboardButton("DZHIVAN")
FirstPageRussianArtistsButton22 = KeyboardButton("ELEY")
FirstPageRussianArtistsButton23 = KeyboardButton("ELMAN")
FirstPageRussianArtistsButton24 = KeyboardButton("ENRASTA")
FirstPageRussianArtistsButton25 = KeyboardButton("ESCAPE")
FirstPageRussianArtistsButton26 = KeyboardButton("ESMI")
FirstPageRussianArtistsButton27 = KeyboardButton("ESTETIKA")
FirstPageRussianArtistsButton28 = KeyboardButton("ETOLUBOV")
FirstPageRussianArtistsButton29 = KeyboardButton("GALIBRI")
FirstPageRussianArtistsButton30 = KeyboardButton("GAODAGAMO")
FirstPageRussianArtistsButton109 = KeyboardButton("GAYAZOV$ BROTHER$")
FirstPageRussianArtistsButton111 = KeyboardButton("GENIMI")
FirstPageRussianArtistsButton114 = KeyboardButton("GIDAYYAT")
FirstPageRussianArtistsButton31 = KeyboardButton("GRENCHANIK")
FirstPageRussianArtistsButton32 = KeyboardButton("GROOVE")
FirstPageRussianArtistsButton33 = KeyboardButton("GUMA")
FirstPageRussianArtistsButton34 = KeyboardButton("HOMIE")
FirstPageRussianArtistsButton35 = KeyboardButton("IAMMIND")
FirstPageRussianArtistsButton128 = KeyboardButton("IDA SINGER")
FirstPageRussianArtistsButton36 = KeyboardButton("IDRIS")
FirstPageRussianArtistsButton37 = KeyboardButton("INTELLIGENT")
FirstPageRussianArtistsButton38 = KeyboardButton("IVAN VALEEV")
FirstPageRussianArtistsButton133 = KeyboardButton("JAKONE")
FirstPageRussianArtistsButton117 = KeyboardButton("JAH KHALIB")
FirstPageRussianArtistsButton129 = KeyboardButton("JAMIK")
FirstPageRussianArtistsButton39 = KeyboardButton("JANAGA")
FirstPageRussianArtistsButton40 = KeyboardButton("JONY")
FirstPageRussianArtistsButton41 = KeyboardButton("KALUSH")
FirstPageRussianArtistsButton42 = KeyboardButton("KALVADOS")
FirstPageRussianArtistsButton43 = KeyboardButton("KAMAZZ")
FirstPageRussianArtistsButton44 = KeyboardButton("KAMBULAT")
FirstPageRussianArtistsButton45 = KeyboardButton("KARAT")
FirstPageRussianArtistsButton46 = KeyboardButton("KAT-RIN")
FirstPageRussianArtistsButton47 = KeyboardButton("KAVABANGA")
FirstPageRussianArtistsButton48 = KeyboardButton("KDK")
FirstPageRussianArtistsButton130 = KeyboardButton("KRISTINA SI")
FirstPageRussianArtistsButton49 = KeyboardButton("KONFUZ")
FirstPageRussianArtistsButton100 = KeyboardButton("LENARKO")
FirstPageRussianArtistsButton50 = KeyboardButton("LERA LERA")
FirstPageRussianArtistsButton51 = KeyboardButton("LIAM HOWARD")
FirstPageRussianArtistsButton110 = KeyboardButton("LIL KRISTALLL")
FirstPageRussianArtistsButton52 = KeyboardButton("LIMBA")
FirstPageRussianArtistsButton53 = KeyboardButton("LIOVA")
FirstPageRussianArtistsButton54 = KeyboardButton("LKN")
FirstPageRussianArtistsButton55 = KeyboardButton("LOOKBUFFALO")
FirstPageRussianArtistsButton56 = KeyboardButton("LUCAVEROS")
FirstPageRussianArtistsButton57 = KeyboardButton("LXE")
FirstPageRussianArtistsButton58 = KeyboardButton("MACAN")
FirstPageRussianArtistsButton108 = KeyboardButton("MADURI")
FirstPageRussianArtistsButton59 = KeyboardButton("MARKUL")
FirstPageRussianArtistsButton60 = KeyboardButton("MATLY")
FirstPageRussianArtistsButton61 = KeyboardButton("MAYOT")
FirstPageRussianArtistsButton62 = KeyboardButton("MEALON")
FirstPageRussianArtistsButton104 = KeyboardButton("MEKHMAN")
FirstPageRussianArtistsButton63 = KeyboardButton("MIYAGI")
FirstPageRussianArtistsButton64 = KeyboardButton("MR LAMBO")
FirstPageRussianArtistsButton113 = KeyboardButton("NASTY BABE")
FirstPageRussianArtistsButton65 = KeyboardButton("NECHAEV")
FirstPageRussianArtistsButton66 = KeyboardButton("NEEL")
FirstPageRussianArtistsButton67 = KeyboardButton("NEKOGLAI")
FirstPageRussianArtistsButton119 = KeyboardButton("NICENIGHT")
FirstPageRussianArtistsButton135 = KeyboardButton("NIKITATA")
FirstPageRussianArtistsButton68 = KeyboardButton("NLO")
FirstPageRussianArtistsButton69 = KeyboardButton("NVRKN134")
FirstPageRussianArtistsButton70 = KeyboardButton("NЮ")
FirstPageRussianArtistsButton71 = KeyboardButton("ODGO")
FirstPageRussianArtistsButton116 = KeyboardButton("OXXXYMIRON")
FirstPageRussianArtistsButton137 = KeyboardButton("PUSSYKILLER")
FirstPageRussianArtistsButton115 = KeyboardButton("QYAL QYAL")
FirstPageRussianArtistsButton72 = KeyboardButton("R.RICCADO")
FirstPageRussianArtistsButton73 = KeyboardButton("RAIKAHO")
FirstPageRussianArtistsButton74 = KeyboardButton("RAKHIM")
FirstPageRussianArtistsButton75 = KeyboardButton("RAMIL")
FirstPageRussianArtistsButton76 = KeyboardButton("RASA")
FirstPageRussianArtistsButton77 = KeyboardButton("REAL GIRL")
FirstPageRussianArtistsButton78 = KeyboardButton("SAM WICK")
FirstPageRussianArtistsButton79 = KeyboardButton("SANTIZ")
FirstPageRussianArtistsButton121 = KeyboardButton("SANTY ONE")
FirstPageRussianArtistsButton80 = KeyboardButton("SASHA SANTA")
FirstPageRussianArtistsButton137 = KeyboardButton("SCIRENA")
FirstPageRussianArtistsButton120 = KeyboardButton("SHAMI")
FirstPageRussianArtistsButton81 = KeyboardButton("SHEIKH MANSUR")
FirstPageRussianArtistsButton82 = KeyboardButton("SLAVA MARLOW")
FirstPageRussianArtistsButton125 = KeyboardButton("SLAVIK POGOSOV")
FirstPageRussianArtistsButton83 = KeyboardButton("STRANGE")
FirstPageRussianArtistsButton84 = KeyboardButton("STRCTRE")
FirstPageRussianArtistsButton85 = KeyboardButton("T1ONE")
FirstPageRussianArtistsButton131 = KeyboardButton("TARAS")
FirstPageRussianArtistsButton86 = KeyboardButton("TANIR")
FirstPageRussianArtistsButton87 = KeyboardButton("TESLYA")
FirstPageRussianArtistsButton88 = KeyboardButton("TIMRAN")
FirstPageRussianArtistsButton89 = KeyboardButton("TINI LIN")
FirstPageRussianArtistsButton90 = KeyboardButton("TORI KVIT")
FirstPageRussianArtistsButton91 = KeyboardButton("V$XV PRINCE")
FirstPageRussianArtistsButton122 = KeyboardButton("VERBEE")
FirstPageRussianArtistsButton126 = KeyboardButton("VESNA305")
FirstPageRussianArtistsButton92 = KeyboardButton("WELLAY")
FirstPageRussianArtistsButton93 = KeyboardButton("WHITE GALLOWS")
FirstPageRussianArtistsButton94 = KeyboardButton("WHYBABY")
FirstPageRussianArtistsButton132 = KeyboardButton("X")
FirstPageRussianArtistsButton95 = KeyboardButton("XASSA")
FirstPageRussianArtistsButton96 = KeyboardButton("XCHO")
FirstPageRussianArtistsButton118 = KeyboardButton("XOLIDAYBOY")
FirstPageRussianArtistsButton97 = KeyboardButton("YACHEVSKIY")
FirstPageRussianArtistsButton98 = KeyboardButton("YUFOLL")
FirstPageRussianArtistsButton107 = KeyboardButton("ZIPPO")
FirstPageRussianArtistsButton99 = KeyboardButton("ZOMB")
first_russian_artists_reply.add(FirstPageRussianArtistsButton1, FirstPageRussianArtistsButton2, FirstPageRussianArtistsButton134, FirstPageRussianArtistsButton3, FirstPageRussianArtistsButton4, FirstPageRussianArtistsButton136, FirstPageRussianArtistsButton5,
                                  FirstPageRussianArtistsButton6, FirstPageRussianArtistsButton7, FirstPageRussianArtistsButton8, FirstPageRussianArtistsButton124, FirstPageRussianArtistsButton9, FirstPageRussianArtistsButton10,
                                  FirstPageRussianArtistsButton11, FirstPageRussianArtistsButton123, FirstPageRussianArtistsButton12, FirstPageRussianArtistsButton13, FirstPageRussianArtistsButton112, FirstPageRussianArtistsButton101, FirstPageRussianArtistsButton14, FirstPageRussianArtistsButton105, FirstPageRussianArtistsButton15,
                                  FirstPageRussianArtistsButton16, FirstPageRussianArtistsButton17, FirstPageRussianArtistsButton18, FirstPageRussianArtistsButton19, FirstPageRussianArtistsButton127, FirstPageRussianArtistsButton102, FirstPageRussianArtistsButton103, FirstPageRussianArtistsButton20,
                                  FirstPageRussianArtistsButton21, FirstPageRussianArtistsButton22, FirstPageRussianArtistsButton23, FirstPageRussianArtistsButton24, FirstPageRussianArtistsButton25,
                                  FirstPageRussianArtistsButton26, FirstPageRussianArtistsButton27, FirstPageRussianArtistsButton28, FirstPageRussianArtistsButton29, FirstPageRussianArtistsButton30, FirstPageRussianArtistsButton109, FirstPageRussianArtistsButton111, FirstPageRussianArtistsButton114,
                                  FirstPageRussianArtistsButton31, FirstPageRussianArtistsButton32, FirstPageRussianArtistsButton33, FirstPageRussianArtistsButton34, FirstPageRussianArtistsButton35, FirstPageRussianArtistsButton128,
                                  FirstPageRussianArtistsButton36, FirstPageRussianArtistsButton37, FirstPageRussianArtistsButton38, FirstPageRussianArtistsButton133, FirstPageRussianArtistsButton117, FirstPageRussianArtistsButton129, FirstPageRussianArtistsButton39, FirstPageRussianArtistsButton40,
                                  FirstPageRussianArtistsButton41, FirstPageRussianArtistsButton42, FirstPageRussianArtistsButton43, FirstPageRussianArtistsButton44, FirstPageRussianArtistsButton45,
                                  FirstPageRussianArtistsButton46, FirstPageRussianArtistsButton47, FirstPageRussianArtistsButton48, FirstPageRussianArtistsButton130, FirstPageRussianArtistsButton49, FirstPageRussianArtistsButton100, FirstPageRussianArtistsButton50,
                                  FirstPageRussianArtistsButton51, FirstPageRussianArtistsButton110, FirstPageRussianArtistsButton52, FirstPageRussianArtistsButton53, FirstPageRussianArtistsButton54, FirstPageRussianArtistsButton55,
                                  FirstPageRussianArtistsButton56, FirstPageRussianArtistsButton57, FirstPageRussianArtistsButton58, FirstPageRussianArtistsButton108, FirstPageRussianArtistsButton59, FirstPageRussianArtistsButton60,
                                  FirstPageRussianArtistsButton61, FirstPageRussianArtistsButton62, FirstPageRussianArtistsButton104, FirstPageRussianArtistsButton63, FirstPageRussianArtistsButton64, FirstPageRussianArtistsButton113, FirstPageRussianArtistsButton65,
                                  FirstPageRussianArtistsButton66, FirstPageRussianArtistsButton67, FirstPageRussianArtistsButton119, FirstPageRussianArtistsButton135, FirstPageRussianArtistsButton68, FirstPageRussianArtistsButton69, FirstPageRussianArtistsButton70,
                                  FirstPageRussianArtistsButton71, FirstPageRussianArtistsButton116, FirstPageRussianArtistsButton137, FirstPageRussianArtistsButton115, FirstPageRussianArtistsButton72, FirstPageRussianArtistsButton73, FirstPageRussianArtistsButton74, FirstPageRussianArtistsButton75,
                                  FirstPageRussianArtistsButton76, FirstPageRussianArtistsButton77, FirstPageRussianArtistsButton78, FirstPageRussianArtistsButton79, FirstPageRussianArtistsButton121, FirstPageRussianArtistsButton80, FirstPageRussianArtistsButton137, FirstPageRussianArtistsButton120,
                                  FirstPageRussianArtistsButton81, FirstPageRussianArtistsButton82, FirstPageRussianArtistsButton125, FirstPageRussianArtistsButton83, FirstPageRussianArtistsButton84, FirstPageRussianArtistsButton85, FirstPageRussianArtistsButton131,
                                  FirstPageRussianArtistsButton86, FirstPageRussianArtistsButton87, FirstPageRussianArtistsButton88, FirstPageRussianArtistsButton89, FirstPageRussianArtistsButton90,
                                  FirstPageRussianArtistsButton91, FirstPageRussianArtistsButton122, FirstPageRussianArtistsButton126, FirstPageRussianArtistsButton92, FirstPageRussianArtistsButton93, FirstPageRussianArtistsButton94, FirstPageRussianArtistsButton132, FirstPageRussianArtistsButton95,
                                  FirstPageRussianArtistsButton96, FirstPageRussianArtistsButton118, FirstPageRussianArtistsButton97, FirstPageRussianArtistsButton98, FirstPageRussianArtistsButton107, FirstPageRussianArtistsButton99)
first_russian_artists_reply.row("Следующая страница  ➡")
first_russian_artists_reply.row("⬅   Назад", "🏠  Главное меню")

#  SECOND PAGE
second_russian_artists_reply = ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
second_russian_artists_reply.row("⬅   Назад", "🏠  Главное меню")
SecondPageRussianArtistsButton1 = KeyboardButton("АБРИКОСА")
SecondPageRussianArtistsButton2 = KeyboardButton("АДВАЙТА")
SecondPageRussianArtistsButton3 = KeyboardButton("АНДРЕЙ ЛЕНИЦКИЙ")
SecondPageRussianArtistsButton4 = KeyboardButton("АРКАЙДА")
SecondPageRussianArtistsButton47 = KeyboardButton("АЛЁНА ШВЕЦ.")
SecondPageRussianArtistsButton49 = KeyboardButton("АМУРА")
SecondPageRussianArtistsButton43 = KeyboardButton("БОДЯ МИР642")
SecondPageRussianArtistsButton5 = KeyboardButton("ВАНЯ ДМИТРЕНКО")
SecondPageRussianArtistsButton6 = KeyboardButton("ВСЕГДАМЕЧТАЛ")
SecondPageRussianArtistsButton7 = KeyboardButton("ГАНВЕСТ")
SecondPageRussianArtistsButton8 = KeyboardButton("ДЕНИС RIDER")
SecondPageRussianArtistsButton41 = KeyboardButton("ДЖАЯММИ")
SecondPageRussianArtistsButton9 = KeyboardButton("ДЖИОС")
SecondPageRussianArtistsButton10 = KeyboardButton("ЕГОР КРИД")
SecondPageRussianArtistsButton11 = KeyboardButton("ИНТЕРНАЛ")
SecondPageRussianArtistsButton12 = KeyboardButton("ИСЛАМ ИТЛЯШЕВ")
SecondPageRussianArtistsButton40 = KeyboardButton("КАНГИ")
SecondPageRussianArtistsButton13 = KeyboardButton("КАСПИЙСКИЙ ГРУЗ")
SecondPageRussianArtistsButton14 = KeyboardButton("ЛЁША СВИК")
SecondPageRussianArtistsButton15 = KeyboardButton("ЛИВИ")
SecondPageRussianArtistsButton16 = KeyboardButton("ЛЫФАРЬ")
SecondPageRussianArtistsButton17 = KeyboardButton("МАКС КОРЖ")
SecondPageRussianArtistsButton18 = KeyboardButton("МАЛЬБЕК")
SecondPageRussianArtistsButton19 = KeyboardButton("МИЧЕЛЗ")
SecondPageRussianArtistsButton20 = KeyboardButton("МОТ")
SecondPageRussianArtistsButton21 = KeyboardButton("НИКУБА")
SecondPageRussianArtistsButton22 = KeyboardButton("ОСТАП ПАРФЁНОВ")
SecondPageRussianArtistsButton23 = KeyboardButton("ПАША PROOROK")
SecondPageRussianArtistsButton24 = KeyboardButton("ПЛАГА")
SecondPageRussianArtistsButton25 = KeyboardButton("ПОШЛЫЙ")
SecondPageRussianArtistsButton48 = KeyboardButton("СКРИПТОНИТ")
SecondPageRussianArtistsButton26 = KeyboardButton("СУЛТАН ЛАГУЧЕВ")
SecondPageRussianArtistsButton27 = KeyboardButton("ТИМА АКИМОВ")
SecondPageRussianArtistsButton28 = KeyboardButton("ТИМА БЕЛОРУССКИХ")
SecondPageRussianArtistsButton29 = KeyboardButton("ТРИ ДНЯ ДОЖДЯ")
SecondPageRussianArtistsButton30 = KeyboardButton("ФЛИТ")
SecondPageRussianArtistsButton31 = KeyboardButton("ФОГЕЛЬ")
SecondPageRussianArtistsButton32 = KeyboardButton("ШЕЙХ МАНСУР")
SecondPageRussianArtistsButton39 = KeyboardButton("ЭЛДЖЕЙ")
SecondPageRussianArtistsButton44 = KeyboardButton("ЭНДШПИЛЬ")
SecondPageRussianArtistsButton46 = KeyboardButton("ЭРИКА ЛУНДМОЕН")
SecondPageRussianArtistsButton33 = KeyboardButton("ЮЛИАНА КАРАУЛОВА")
SecondPageRussianArtistsButton34 = KeyboardButton("ЮРИЙ ШАТУНОВ")
SecondPageRussianArtistsButton35 = KeyboardButton("ЯД ДОБРА")
SecondPageRussianArtistsButton45 = KeyboardButton("ЯМЫЧ")
SecondPageRussianArtistsButton42 = KeyboardButton("84")
SecondPageRussianArtistsButton36 = KeyboardButton("3-ИЙ ЯНВАРЬ")
SecondPageRussianArtistsButton37 = KeyboardButton("5УТРА")
SecondPageRussianArtistsButton38 = KeyboardButton("100ЛИЦЯ")
second_russian_artists_reply.add(   SecondPageRussianArtistsButton1, SecondPageRussianArtistsButton2, SecondPageRussianArtistsButton3, SecondPageRussianArtistsButton4, SecondPageRussianArtistsButton47, SecondPageRussianArtistsButton49, SecondPageRussianArtistsButton43, SecondPageRussianArtistsButton5,
                                    SecondPageRussianArtistsButton6, SecondPageRussianArtistsButton7, SecondPageRussianArtistsButton8, SecondPageRussianArtistsButton41, SecondPageRussianArtistsButton9, SecondPageRussianArtistsButton10,
                                    SecondPageRussianArtistsButton11, SecondPageRussianArtistsButton12, SecondPageRussianArtistsButton40, SecondPageRussianArtistsButton13, SecondPageRussianArtistsButton14, SecondPageRussianArtistsButton15,
                                    SecondPageRussianArtistsButton16, SecondPageRussianArtistsButton17, SecondPageRussianArtistsButton18, SecondPageRussianArtistsButton19, SecondPageRussianArtistsButton20,
                                    SecondPageRussianArtistsButton21, SecondPageRussianArtistsButton22, SecondPageRussianArtistsButton23, SecondPageRussianArtistsButton24, SecondPageRussianArtistsButton25, SecondPageRussianArtistsButton48,
                                    SecondPageRussianArtistsButton26, SecondPageRussianArtistsButton27, SecondPageRussianArtistsButton28, SecondPageRussianArtistsButton29, SecondPageRussianArtistsButton30,
                                    SecondPageRussianArtistsButton31, SecondPageRussianArtistsButton32, SecondPageRussianArtistsButton39, SecondPageRussianArtistsButton44, SecondPageRussianArtistsButton46,
                                    SecondPageRussianArtistsButton33, SecondPageRussianArtistsButton34, SecondPageRussianArtistsButton35, SecondPageRussianArtistsButton45, SecondPageRussianArtistsButton42,
                                    SecondPageRussianArtistsButton36, SecondPageRussianArtistsButton37, SecondPageRussianArtistsButton38)
second_russian_artists_reply.row("⬅  Предыдущая страница")
second_russian_artists_reply.row("⬅   Назад", "🏠  Главное меню")



#  ENGLISH ARTISTS

english_artists_reply = ReplyKeyboardMarkup(row_width = 3, resize_keyboard = True)
english_artists_reply.row("⬅   Назад", "🏠  Главное меню")
english_artist_1 = KeyboardButton("BLACKBEAR")
english_artist_2 = KeyboardButton("CASSETTE")
english_artist_3 = KeyboardButton("DAFT PUNK")
english_artist_4 = KeyboardButton("DUA LIPA")
english_artist_5 = KeyboardButton("FOUSHEE")
english_artist_6 = KeyboardButton("G-EASY")
english_artist_7 = KeyboardButton("GHOSTLY KISSES")
english_artist_8 = KeyboardButton("IAN STORM")
english_artist_9 = KeyboardButton("INNA")
english_artist_10 = KeyboardButton("JVLA")
english_artist_11 = KeyboardButton("KINA")
english_artist_22 = KeyboardButton("LADY GAGA")
english_artist_12 = KeyboardButton("LISA")
english_artist_13 = KeyboardButton("MINELLI")
english_artist_14 = KeyboardButton("MISHLAWI")
english_artist_15 = KeyboardButton("OLIVER TREE")
english_artist_16 = KeyboardButton("PHARELL WILLIAMS")
english_artist_17 = KeyboardButton("SEAN PAUL")
english_artist_18 = KeyboardButton("SQUID GAME")
english_artist_23 = KeyboardButton("SZA")
english_artist_19 = KeyboardButton("TIESTO")
english_artist_20 = KeyboardButton("TREVOR DANIEL")
english_artist_21 = KeyboardButton("XXXTENTACION")
english_artists_reply.add(  english_artist_1, english_artist_2, english_artist_3, english_artist_4, english_artist_5,
                            english_artist_6, english_artist_7, english_artist_8, english_artist_9, english_artist_10,
                            english_artist_11, english_artist_22, english_artist_12, english_artist_13, english_artist_14, english_artist_15,
                            english_artist_16, english_artist_17, english_artist_18, english_artist_23, english_artist_19, english_artist_20,
                            english_artist_21)
english_artists_reply.row("⬅   Назад", "🏠  Главное меню")












