# coding: utf-8
# -*- coding: utf-8 -*-
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler) 
import telegram
from maxsulot import *
from function import *
import json
import ast
import datetime

Token='1573065998:AAEp502bdMmXOnBboaZ8_PZcTz81cN8VcY0'
bot=telegram.Bot(Token)
Uzbutton=ReplyKeyboardMarkup([
    ["✏️ Buyurtma berish"],
    ["⚙️ Bizning hizmatlar","📞 Biz bilan bog'lanish"],
    ["🚩 Bizning manzil"]
], resize_keyboard=True)

global i, index, Zakzlar, add, S, User, Users
Zakazlar=[]
add={'Nomi':'', 'Rangi':'', 'Dona':'', 'Karobka':''}
i=0
index=-1
S=''
Users=''
Jami=JamiNarx=0
User={'Fio':'', 'Tel':'', 'Username':''}
messageH, unMessage="","Aniqlanmagan so'rov, bot faqat maxsus buyruqlarga javob qaytara oladi"
def start(update, context):
    message="Assalom alykum xurmatli mijozlar <b>Uchko'prik Lak Bo'yoqlar MCHJ</b> buyurtmalar botiga xush kelibsiz. Siz ushbu bot orqali bizning istalgan maxsulotlarimizga istalgancha buyurtma berishingiz mumkin."
    update.message.reply_photo( photo=open('img/img1.jpg', 'rb'), caption=message,  reply_markup=Uzbutton, parse_mode='HTML')
    f = open("files/users.txt", "r")
    S=f.read()
    arr=S.split(',')
    b=0
    print(arr)
    print(S)
    for a in arr:
        if(a==str(update.message.chat.id) and a!=''):
            b+=1
    if b==0:
        S=S+str(update.message.chat.id)+","
        f = open("files/users.txt", "w")
        f.write(S)
    return 2
def inline_callback(update, context):
    global i, index,S, User, Users, add, Zakazlar
    query=update.callback_query
    fun=json.loads(query.data)

    if fun['fun']=='zakazQ':
        query.message.reply_photo(photo=open('img/img2.jpg', 'rb'), caption='Online')
        return 2
    # Zakaz maxsulot
    if fun['fun']=="ZakazM":
        index+=1
        query.message.delete()
        Zakazlar.append(add)
        Kraskalar(query)
    if fun['fun']=='Rangi':
        query.message.delete()
        Zakazlar[index]['Nomi']=Kraska[int(fun['index'])]['Nomi']
        Ranglar(int(fun['index']), query)
    if fun['fun']=='Soni':
        query.message.delete()
        Zakazlar[index]['Rangi']=Rang[int(fun['rang'])]
        Sonlar(int(fun['index']), query)
    if fun['fun']=='Count':
        query.message.delete()
        if fun['soni']=='🛢 Dona':
            query.message.reply_html('📍\n🛢 Ilsimos maxsulotning dona sonini kiriting\n<b>☝️ Masalan:</b> <i>(<b>Dona soni:</b>20)</i>\n<b>Dona soni:</b>')
            i=1
        if fun['soni']=='📦 Karobka':
            query.message.reply_html('📍\n📦 Iltimos maxsulotning qadoqlangan sonini kiriting\n<b>☝️ Masalan:</b> <i>(<b>Karobka soni:</b>20)</i>\n<b>Karobka soni:</b>')
            i=2
    if fun['fun']=='Junatish':
        query.message.delete()
        butH=[
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'Tasdiqlash', 'Id':query.message.chat.id}))],
            [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'Rad', 'Id':query.message.chat.id}))]
        ]
        query.message.reply_html(Users+S)
        query.message.reply_html("📌 |  ✅\nSizning buyurtmangiz <b>Uchko'prik Lak Bo'yoqlar MCHJ</b>  xodimlariga yuborildi. Iltimos biroz kuting korxona xodimlari qisqa vaqtlar ichida siz bilan bog'lanishadi.", reply_markup=Uzbutton)
        f = open("files/admins.txt", "r")
        Q=f.read()
        arr=Q.split(',')
        for b in arr:
            if b!='':
                bot.send_message(chat_id=int(b), text=Users+S,  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(butH))
        S=''
        index=-1
        Zakazlar=[]
    if fun['fun']=="Tasdiqlash":
        text="📌 |  ✅\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz tasdiqlandi iltimos biroz kuting, <b>Mustang</b> kompaniyasi xodimlari qisqa vaqatlar ichida siz bilan bg'lanishadi."
        Message=query.message.text+"\n\n<b>✅ Tasdiqlangan</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        query.message.reply_html(Message)
    if fun['fun']=="TasdiqlashR":
        text="📌 |  ✅\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz tasdiqlandi iltimos biroz kuting, <b>Mustang</b> kompaniyasi xodimlari qisqa vaqatlar ichida siz bilan bg'lanishadi."
        Message=query.message.caption+"\n\n<b>✅ Tasdiqlangan</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        x="img/"+fun['img']+".jpg"
        query.message.reply_photo(photo=open(x, 'rb'), caption=Message, parse_mode="HTML")
    if fun['fun']=="Rad":
        text="❌\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz bazi sabablarga ko'ra tasdiqlanmadi, Bunday sabablar uchun  <b>Mustang</b> kompaniyasi sizdan uzur so'raydi."
        Message=query.message.text+"\n\n<b>❌ Rad etildi</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        query.message.reply_html(Message)
    if fun['fun']=="RadR":
        text="❌\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz bazi sabablarga ko'ra tasdiqlanmadi, Bunday sabablar uchun  <b>Mustang</b> kompaniyasi sizdan uzur so'raydi."
        Message=query.message.caption+"\n\n<b>❌ Rad etildi</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        x="img/"+fun['img']+".jpg"
        query.message.reply_photo(photo=open(x, 'rb'), caption=Message, parse_mode="HTML")
    if fun['fun']=='Delete':
        query.message.delete()
        query.message.reply_html("📌 | ❌ \nSizning buyurtmangiz muvofaqiyatli o'chirildi.☝️ Istasangiz <b>Buyurtma berish</b> tugmasi orqali qayta buyurtma berishindiz mumkin.", reply_markup=Uzbutton)
        i=0
    if fun['fun']=='Qaytarish':
        query.message.delete()
        S=''
        index=0
        Zakazlar=[]
        User['Fio']=''
        Zakazlar.append(add)
        query.message.reply_html("📌 | ♻️ \nSizning eski buyurtmangizni bekor qildingiz.<b>☝️ Yangi maxsulotni tanlashingiz mumkin.</b>", reply_markup=Uzbutton)
        Kraskalar(query)
        i=0
    if fun['fun']=='YozmaZ':
        query.message.delete()
        S=''
        index=0
        Zakazlar=[]
        User['Fio']=''
        query.message.reply_html("📌 |  ✍️\nIltimos buyurtma berish jarayonida imlo xatolariga etibor bering va namunaga binonan yozishingizni so'raymiz.\n<b>Namuna:</b>\n<i>Mustang 3kg soni.. \nMustang 1kg soni...\nFIO...\nTelefon raqam...</i>")
        i=5
    if fun['fun']=='Rasim':
        query.message.delete()
        S=''
        index=0
        Zakazlar=[]
        User['Fio']=''
        query.message.reply_html("📌 |  ✍️\nIltimos buyurtma rasimini yuboring.")
        i=6
          
def ZakazlarFun(update, context):
    global i, narx, index,S,  User,Users, add, Zakazlar, idAdmin, x
    if i==9:
        f = open("files/users.txt", "r")
        S=f.read()
        arr=S.split(',')
        if len(update.message.photo)>0:
            file_id = update.message.photo[-1]
            newFile = bot.getFile(file_id)
            x = datetime.datetime.now()
            x=x.strftime("%d")+x.strftime("%b")+x.strftime("%y")+x.strftime("%H")+x.strftime("%M")+x.strftime("%S")
            a="img/"+x+".jpg"
            newFile.download(a)
            text=str(update.message.caption)
            x=x+".jpg"
            for b in arr:
                if b!='':
                    bot.sendPhoto(chat_id=int(b), photo=open(a, 'rb'), caption=text, parse_mode="HTML")  
            i=-1
        else:
            text=update.message.text
            for b in arr:
                if b!='':
                    bot.send_message(chat_id=int(b), text=text,  parse_mode='HTML')
    if i==8:
        f = open("files/password.txt", "r")
        password=f.read()
        if password==str(update.message.text):
            f = open("files/admins.txt", "r")
            S=f.read()
            arr=S.split(',')
            b=0
            for a in arr:
                if a==str(idAdmin) and a!='':
                    b+=1
            if(b==0):
                S=S+','+str(idAdmin)
                f = open("files/admins.txt", "w")
                f.write(S)
                update.message.reply_html("📌 |  ✅\nSiz kiritgan ID raqam Adminlar qatoriga kiritildi va barcha buyurtmalarni ko'rish imkoniyatiga ega bo'ldi.", reply_markup=Uzbutton)
            else:
                update.message.reply_html("📌 |  ✅\nSiz kiritgan ID raqam Adminlar qatorida mavjut.", reply_markup=Uzbutton)

    if i==7:
        i=8
        idAdmin=update.message.text
        update.message.reply_html("📌 \n<b>Parolni kiriting:</b>", reply_markup=Uzbutton)

        
    if i==6:
        if len(update.message.photo)>0:
            file_id = update.message.photo[-1]
            newFile = bot.getFile(file_id)
            x = datetime.datetime.now()
            x=x.strftime("%d")+x.strftime("%b")+x.strftime("%y")+x.strftime("%H")+x.strftime("%M")+x.strftime("%S")
            a="img/"+x+".jpg"
            newFile.download(a)
            butH=[
                [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'TasdiqlashR', 'Id':update.message.chat.id, 'img':x}))],
                [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'RadR', 'Id':update.message.chat.id, 'img':x}))]
            ]
            update.message.reply_html("📌 |  ✅\nSizning buyurtmangiz <b>Uchko'prik Lak Bo'yoqlar MCHJ</b>  xodimlariga yuborildi. Iltimos biroz kuting korxona xodimlari qisqa vaqtlar ichida siz bilan bog'lanishadi.", reply_markup=Uzbutton)
            text="\n\n<b>Ismi: </b>"+str(update.message.chat.first_name)+"\n<b>Familya: </b>"+str(update.message.chat.last_name)+"\n<b>Username:</b> @"+str(update.message.chat.username)+"\n<b>Text:</b> "+str(update.message.caption)
            x=x+".jpg"
            f = open("files/admins.txt", "r")
            S=f.read()
            arr=S.split(',')
            for b in arr:
                if b!='':
                    bot.sendPhoto(chat_id=int(b), photo=open(a, 'rb'), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(butH))  
            i=-1
        else:
            update.message.reply_html("📌 |  ❌\nIltimos buyurtma qo'lyozma rasmini yuboring!!!", reply_markup=Uzbutton)



    if i==5:
        butH=[
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'Tasdiqlash', 'Id':update.message.chat.id}))],
            [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'Rad', 'Id':update.message.chat.id}))]
        ]
        text=update.message.text
        update.message.reply_html("📌 |  ✅\nSizning buyurtmangiz <b>Uchko'prik Lak Bo'yoqlar MCHJ</b>  xodimlariga yuborildi. Iltimos biroz kuting korxona xodimlari qisqa vaqtlar ichida siz bilan bog'lanishadi.", reply_markup=Uzbutton)
        f = open("files/admins.txt", "r")
        S=f.read()
        arr=S.split(',')
        for b in arr:
            if b!='':
                bot.send_message(chat_id=int(b), text=text,  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(butH))
    if i==4:
        if update.message.contact:
            User['Tel']=update.message.contact.phone_number
        else:
            User['Tel']=update.message.text
        Tekshir(update)
        i=-1

    if i==3:
        User['Fio']=update.message.text
        phoneB=telegram.KeyboardButton(text="📱 Telefon raqamni", request_contact=True)
        update.message.reply_html("<b>Telefon raqam:</b>", reply_markup=ReplyKeyboardMarkup([[phoneB]], resize_keyboard=True, one_time_keyboard=True))
        i=4
    if i==2:
        Zakazlar[index]['Karobka']=update.message.text
        Zakazlar[index]['Dona']=str(int(update.message.text)*6)+" bonka"
        if User['Fio']!='':
            Tekshir(update)
            i=-1
        else: 
            update.message.reply_html("<b>Iltimos O'zingiz haqingizdagi ma'lumotlarni to'ldiring!!!</b>" )
            update.message.reply_html("<b>Ism Familya:</b> \n<i>(Mazalan: Alisher Parpiev)</i>")           
            i=3  
         
    if i==1:
        Zakazlar[index]['Dona']=update.message.text+' bonka'
        Zakazlar[index]['Karobka']=str(int(int(update.message.text)/6))
        if User['Fio']!='':
            Tekshir(update)
            i=-1
        else: 
            update.message.reply_html("<b>Iltimos O'zingiz haqingizdagi ma'lumotlarni to'ldiring!!!</b>" )
            update.message.reply_html("<b>Ism Familya:</b> \n<i>(Mazalan: Alisher Parpiev)</i>")           
            i=3  
    if i==0:
        update.message.reply_html("<b>📌 | ⁉️\nAniqlanmagan so'rov bot faqat maxsus so'rovlarga javob qaytara oladi.</b>")
    if i==-1:
        i=0
    return 2
    

def Tekshir(update):
    global i, index,S,  User,Users, add,  Zakazlarss
    Users='📌\n<b>👤 Zakaz Beruvchi</b>\n\n<b>👨‍💻 FIO:</b> '+User['Fio']+"\n<b>📱 Telefon raqami:</b> "+User['Tel']+"\n\n<b>🧾 Buyurtmalar</b>"
    S=S+"\n\n<b>"+str(index+1)+"-Maxsulot</b>\n<b>📍 Nomi:</b>"+Zakazlar[index]['Nomi']+"\n<b>📍 Rangi:</b>"+Zakazlar[index]['Rangi']+"\n<b>📍Soni:</b>"+Zakazlar[index]['Dona']+"\n<b>📍 Karobka soni:</b>"+Zakazlar[index]['Karobka']
    butH=[
            [InlineKeyboardButton("✅ Zakazni yuborish", callback_data=json.dumps({'fun':'Junatish'}))],
            [InlineKeyboardButton("➕ Zakaz qo'shish", callback_data=json.dumps({'fun':'ZakazM'}))],
            [InlineKeyboardButton("♻️ Qayta zakaz berish", callback_data=json.dumps({'fun':'Qaytarish'}))],
            [InlineKeyboardButton("❌ O'chirish", callback_data=json.dumps({'fun':'Delete'}))]
        ]
    update.message.reply_html(Users+S, reply_markup=InlineKeyboardMarkup(butH))
    return 2

def Buyurtma(update, contect):
    global i,  index,S, Jami, User,Users, add, Zakazlar
    S=''
    Zakazlar=[]
    index=-1
    butH=[
            [InlineKeyboardButton("🗂 Avtomatik Buyurtma", callback_data=json.dumps({'fun':'ZakazM'}))],
            [InlineKeyboardButton("📝 Qo'lyozma buyurtma", callback_data=json.dumps({'fun':'YozmaZ'}))],
            [InlineKeyboardButton("📸 Rasim yuborish", callback_data=json.dumps({'fun':'Rasim'}))],
        ]
    update.message.reply_photo( photo=open('img/img3.jpg', 'rb'), caption="Assalom alaykum hurmatli mijoz. Siz quyidagi uch usulda buyurtma berish imkoniyatiga egasiz.\n\n🛒 Maxsulotlarni tanlash.\n📋 Maxsulotlar nomini yozish.\n🖼 Qo'lyozmani suratga olib yuborish.",   reply_markup=InlineKeyboardMarkup(butH))
    return 2


def Boglanish(update, contect):
    global i
    text="<b>📌 | 📱 \nUchko'prik Lak Bo'yoq MCHJ</b> ishonch raqamlari siz uchun xizmatda.\n📞 <b>Admin:     </b>+998905086006\n📞 <b>Hisobchi: </b>+998911413344\n📞 <b>Texnolog: </b>+998911470778"
    update.message.reply_html( text)
    i=0
    return 2


def Hizmatlar(update, contect):
    global i
    text="<b>📌 | 📊\nUchko'prik Lak Bo'yoq MCHJ</b> quyidagi xizmatlarni o'z ichiga oladi.\n\n<b>Bizning Xizmatlar:</b>\n\n✅ Yuqori sifatli <b>Lak Bo'yoq</b> maxsulotlari ishlab chiqarish.\n✅ Suvli bo'yoqlar ishlab chiqarish.\n🚚 O'zbekiston bo'ylab yetkazib berish xizmati."
    update.message.reply_html( text)
    i=0
    return 2

def sendLocation(update, contect):
    update.message.reply_location(longitude=40.478057, latitude=71.0320803)
def Admin(update, context):
    global i
    update.message.reply_html("Iltimos Admin bo'lish uchun <b>ID</b> raqamni yuboring.\n\nSizning Id raqamindiz:<b>"+str(update.message.chat.id)+"</b>")
    i=7
    return 2
def SendAll(update, context):
    global i
    update.message.reply_html("Siz kiritgan ma'lumotlar botning barcha foydalanuvchilariga yuboriladi iltimos ma'lumotni yuborishdan oldin uning xatosiz va to'g'ri ekanligiga etibor bering.\n\n<b>Malumot:</b>")
    i=9
    return 2

def main():
    updater=Updater('1573065998:AAEp502bdMmXOnBboaZ8_PZcTz81cN8VcY0', use_context=True)
    dispatcher=updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    conv_handler=ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('admincreate', Admin),
            CommandHandler('allkuser', SendAll),
            MessageHandler(Filters.regex('^('+"✏️ Buyurtma berish"+')$'), Buyurtma),
            MessageHandler(Filters.regex('^('+"📞 Biz bilan bog'lanish"+')$'), Boglanish),
            MessageHandler(Filters.regex('^('+"⚙️ Bizning hizmatlar"+')$'), Hizmatlar),
            MessageHandler(Filters.regex('^('+"🚩 Bizning manzil"+')$'), sendLocation),
        ],
        states={
                1:[CallbackQueryHandler(inline_callback)],
                2:[
                    MessageHandler(Filters.regex('^('+"/start"+')$'), start),

                    MessageHandler(Filters.regex('^('+"✏️ Buyurtma berish"+')$'), Buyurtma),
                    MessageHandler(Filters.regex('^('+"📞 Biz bilan bog'lanish"+')$'), Boglanish),
                    MessageHandler(Filters.regex('^('+"⚙️ Bizning hizmatlar"+')$'), Hizmatlar),
                    MessageHandler(Filters.regex('^('+"🚩 Bizning manzil"+')$'), sendLocation),
                    MessageHandler(Filters.regex('^('+"/admincreate"+')$'), Admin),
                    MessageHandler(Filters.regex('^('+"/allkuser"+')$'), SendAll),
                ]
                },
        fallbacks=[MessageHandler(Filters.all, ZakazlarFun)]
        )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle() 


main()