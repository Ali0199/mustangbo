from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import telegram
from maxsulot import *
import json
import ast

# Kraskasss
def Kraskalar(query):
    buttons=[]
    count=0
    for i in Kraska:
        a={'fun':'Rangi', 'index':count}
        a=json.dumps(a)
        button=[InlineKeyboardButton(i['Nomi'], callback_data=a)]
        buttons.append(button)
        count+=1
    buttons=InlineKeyboardMarkup(buttons)
    query.message.reply_html('📌 \nBizning maxsulotlardan istaganingizni tanlang va buyurtma bering. \n <b>Barch maxsulotlar:</b>', reply_markup=buttons)
# Rangi
def Ranglar(a, query):
    buttons=[]
    count=0
    print(Kraska[int(a)]['img'])
    for i in Kraska[a]['Rangi']:
        fun={'fun':'Soni', 'index':a, 'rang':i}
        fun=json.dumps(fun)
        button=[InlineKeyboardButton(Rang[i], callback_data=fun)]
        buttons.append(button)
        count+=1
    buttons=InlineKeyboardMarkup(buttons)
    query.message.reply_photo(photo=open(Kraska[int(a)]['img'], 'rb'), caption='📌 \nIltimos tanlagan maxsulotingiz rangini kiriting. \n <b>Maxsulotning bizda mavjut ranglari:</b>', parse_mode='HTML', reply_markup=buttons)


def Sonlar(a, query):
    buttons=[]
    count=0
    for i in Kraska[a]['Soni']:
        fun={'fun':'Count', 'soni':Soni[count]}
        fun=json.dumps(fun)
        button=[InlineKeyboardButton(Soni[i], callback_data=fun)]
        buttons.append(button)
        count+=1
    buttons=InlineKeyboardMarkup(buttons)
    query.message.reply_html('📌 \nBizda siz tanlagan maxsulotning sifativa kilogramiga qarab quyidagi narxlari mavjut. \n <b>Maxsulotning bizda mavjut ranglari:</b>', reply_markup=buttons)






