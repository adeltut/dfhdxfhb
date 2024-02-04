import asyncio
from aiogram import Bot, Dispatcher, types, F
from dotenv import load_dotenv
from utilis.command import set_commands
from handlers.start import get_start
from state.registor import RegistorState
from handlers.register import start_register, registor_name, report, registor_gen, registor_work, registor_phone, registor_otch
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.Registor_kb import admin_keyboard, Defult_keyboard, oles_keyboard
import os
from utilis.database import Database, Databaseackt, Databascmena
from queue import Queue
from state.coferm import done, cmenadd, cmenad38, ackt
import datetime
from datetime import date
import requests
from datetime import datetime as dt
from fastapi import FastAPI
from pydantic import BaseModel
import json

q = Queue()
load_dotenv()
token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')
admin_id38 = os.getenv('ADMIN_ID38')

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher()


async def time(messege: Message):

    url = f"https://spar36.serverkazan.keenetic.link/iclock/api/transactions/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkZWx0dXQ1IiwiZXhwIjoxNzA3MTUwMzMyLCJlbWFpbCI6ImFkZWx0dXR1bmluNUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTcwNjU0NTUzMn0.ekE24-jfu4gIps6vuL3ThwBprxANI7qlDxW54L4BzjE"
    }
    current_date = date.today()
    json1 = {
        "start_time": current_date
    }
    response = requests.get(url, params=json1, headers=headers)
    print(response.json())
    str = int(response.json()["count"])

    for i in range(str):
        name = response.json()["data"][i]["first_name"]
        punch_state = response.json()["data"][i]["punch_state"]
        punch_time = response.json()["data"][i]["punch_time"]
        print(name, ",", punch_state, ",", punch_time)
        db = Databaseackt(os.getenv("DATABASE_NAMEactk"))
        ackt = db.select_ackt_name(name)
        print(f"{ackt} dfh")
        date1 = dt.strptime(punch_time, '%Y-%m-%d %H:%M:%S')
        h1 = date1.strftime("%H:%M")
        dateq = date1.strftime("%d.%m")
        print(h1)
        print(dateq)
        try:
            print("gdfibjidfjn")
            if ((dateq) == ackt[8]):
                if (punch_state == "1"):
                    if (ackt[7] != h1):
                        db = Databaseackt(os.getenv("DATABASE_NAMEactk"))
                        db.editackyxod(h1, name)
                        ackt = db.select_ackt_name(name)
                        str = f"Уход отмечен в {h1}"
                        await bot.send_message(admin_id, str)
                        print("gdfibjidfjn")
                        s3 = ackt[6].split(":")
                        s2 = ackt[7].split(":")
                        h = int(s2[0]) - int(s3[0])
                        m = int(s2[1]) - int(s3[1])
                        md = m / 60
                        ch = h + md
                        print("gdfibjidfjn")
                        if (ch > 8):
                            ch1 = ch - 1
                            ch2 = round(ch1)
                        else:
                            ch2 = round(ch)

                        str1 = f"{ackt[6]}-{ackt[7]} = {ch2}"

                        print(str1)
                        str = (f"#отчёт\n"
                               f"{name}\n"
                               f"{ackt[2]}\n"
                               f"{str1}")
                        print("gdfibjidfjn")
                        db.editackh(ch2, name)
                        print("gdfibjidfjn")
                        await bot.send_message(admin_id, str)
                        sendsms(user[6])
        except:
            print("gdfibjidfj")

        if (ackt == None or ackt[8] != dateq):
            if (punch_state == "0"):
                db = Database(os.getenv("DATABASE_NAME"))
                print(name)
                user = db.select_user_name(name)
                print(user[2])
                db = Databaseackt(os.getenv("DATABASE_NAMEactk"))
                db.add_userackt(name, user[2], user[3], h1, dateq)
                str = f"Приход отмечен в {h1}"
                await bot.send_message(admin_id, str)
                print("gdfibjidfjn")
                await sendsms(user[6])


async def registor_mag(messege: Message, state: FSMContext):
    if (messege.text == "sparonline36" or messege.text == "sparonline38"):
        await messege.answer(f"Вы выбрали {messege.text}\n")

        await state.update_data(regmag=messege.text)
        await state.set_state(RegistorState.regWork)
        reg_data = await state.get_data()
        reg_name = reg_data.get("regname")
        reg_Work = reg_data.get("regWork")
        reg_gen = reg_data.get("reggen")
        reg_phone = reg_data.get("regphone")
        reg_mag = reg_data.get("regmag")
        reg_otch = reg_data.get("regotch")
        msg = f"Прятно познакомится {reg_name} \n\n Пол - {reg_gen}\n Магазин - {reg_mag}\n Должность - {reg_Work}\n Телефон - {reg_phone}\n Telegram id - {messege.from_user.id}"
        await messege.answer(msg, reply_markup=Defult_keyboard)
        db = Database(os.getenv("DATABASE_NAME"))
        db.add_user(reg_name, reg_Work, messege.from_user.id, reg_gen, reg_mag, reg_phone, reg_otch)
        await state.set_state(RegistorState.work)
        if reg_mag == "sparonline36" and reg_Work == "Сборщик":
            await messege.answer("Регистрация в терминале учета рабочего времени")
            url = f"https://spar36.serverkazan.keenetic.link/personnel/api/employees/"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkZWx0dXQ1IiwiZXhwIjoxNzA3MTUwMzMyLCJlbWFpbCI6ImFkZWx0dXR1bmluNUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTcwNjU0NTUzMn0.ekE24-jfu4gIps6vuL3ThwBprxANI7qlDxW54L4BzjE"
            }
            response = requests.get(url, headers=headers)
            print(response.json())
            col = int(response.json()["count"])
            url = f"https://spar36.serverkazan.keenetic.link/personnel/api/employees/"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkZWx0dXQ1IiwiZXhwIjoxNzA3MTUwMzMyLCJlbWFpbCI6ImFkZWx0dXR1bmluNUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTcwNjU0NTUzMn0.ekE24-jfu4gIps6vuL3ThwBprxANI7qlDxW54L4BzjE"
            }
            json1 = {
                "emp_code": col + 1,
                'department': 1,
                "area": [2, 2],
                "first_name": reg_name
            }
            response = requests.post(url, headers=headers, json=json1)
            print(response.json())
            await messege.answer("Данный этап регистрации завершен, для учета рабочего времени надо привезать биометрию к ФИ в терминале(пример есть в группе), и подождать потверждения регистрации в боте.")
        await messege.answer("По вопросу работы бота обращаться к @TutAd5")
        await bot.send_message(admin_id,
                               text=f"#новый_пользователь\n ✅Зарегистрирован новый пользователь\n {reg_name} \n\n Пол - {reg_gen}\n Магазин - {reg_mag}\n Должность - {reg_Work}\n Телефон - {reg_phone}\n Telegram id - {messege.chat_id}")
        await bot.send_message(admin_id38,
                               text=f"#новый_пользователь\n ✅Зарегистрирован новый пользователь\n {reg_name} \n\n Пол - {reg_gen}\n Магазин - {reg_mag}\n Должность - {reg_Work}\n Телефон - {reg_phone}\n Telegram id - {messege.chat_id}")

    else:
        await messege.answer("Выберете информацию через кнопки ниже")


async def state_Work(messege: Message, state: FSMContext):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(messege.from_user.id)
    if (user[2] == "Курьер"):
        str1 = f"{messege.text} заказов"
    else:

        s = messege.text
        s1 = s.split("-")
        s3 = s1[0].split(":")
        s2 = s1[1].split(":")
        h = int(s2[0]) - int(s3[0])
        m = int(s2[1]) - int(s3[1])
        md = m / 60
        ch = h + md
        if (ch > 8):
            ch1 = ch - 1
            ch2 = round(ch1)
        else:
            ch2 = round(ch)
        str1 = f"{messege.text} = {ch2}"

    str = (f"#отчёт\n"
           f"{user[1]}\n"
           f"{user[2]}\n"
           f"{str1}")
    await messege.answer(str)

    if (user[5] == 'sparonline36'):
        await bot.send_message("-1001974191481", str)
        dbackt = Databaseackt(os.getenv("DATABASE_NAMEackt"))
        dbackt.add_userackt(user[1], user[2], messege.from_user.id, ch2)
    elif (user[5] == 'sparonline38'):
        await bot.send_message("-1002058853145", str)


async def start_bot(bot: bot):
    await bot.send_message(admin_id, text="#запуск\n Бот запустился", reply_markup=admin_keyboard)


#    await bot.send_message(admin_id38, text="#запуск\n Бот запустился", reply_markup=oles_keyboard)
async def dataget(messege: Message, state: FSMContext):
    dbackt = Databaseackt(os.getenv("DATABASE_NAMEackt"))
    userackt = dbackt.get_record()
    for row in userackt:
        str = (f"ID:, {row[0]}\n"
               f"Имя:, {row[1]}\n"
               f"Должность:, {row[2]}\n"
               f"Количество:, {row[4]}\n"
               f"Статус:, {row[5]}")
        await messege.answer(str)
    await state.set_state(RegistorState.editacktid)
    await messege.answer("Введите номер которого вы хотите изменить")


async def editacktid(messege: Message, state: FSMContext):
    await messege.answer(f"Вы выбрали id:{messege.text}\n"
                         f"Введите изменёное количество")
    await state.update_data(acktid=messege.text)
    await state.set_state(RegistorState.editackt)


async def editackt(messege: Message, state: FSMContext):
    await messege.answer("Происходит процес изменения БД")
    col = messege.text
    ackt_data = await state.get_data()
    acktid = ackt_data.get("acktid")
    dbackt = Databaseackt(os.getenv("DATABASE_NAMEackt"))
    dbackt.editacktid(col, acktid)
    userackt = dbackt.select_ackt_id(acktid)
    str = (f"ID:, {userackt[0]}\n"
           f"Имя:, {userackt[1]}\n"
           f"Должность:, {userackt[2]}\n"
           f"Количество:, {userackt[4]}\n"
           f"Статус:, {userackt[5]}")
    await messege.answer(str)


async def cmena(messege: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(messege.from_user.id)
    await messege.answer(f"Запрос отправлен")
    if (user[4] == 'М'):
        str = f"#смена\n {user[1]}\n Взял смену"
    elif (user[4] == "Ж"):
        str = f"#смена\n {user[1]}\n Взяла смену"
    if (user[5] == 'sparonline36'):
        await bot.send_message(admin_id, str)
        await bot.send_message("-1001974191481", str)
    elif (user[5] == 'sparonline38'):
        await bot.send_message(admin_id38, str)
        await bot.send_message("-1002058853145", str)
    str2 = f"Смена,{messege.from_user.id},0"
    q.put(str2)
    await accept_all()


async def cmenaad(messege: Message, state: FSMContext):
    await messege.answer(f"Введите количество заказов")
    await state.set_state(RegistorState.cmena)


async def cmenaun(messege: Message):
    a = messege.text
    str = f"Заказ,{messege.from_user.id},{a}"
    q.put(str)
    await accept_all()


async def mes(messege: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(messege.from_user.id)
    await messege.answer(f"✅Запрос отправлен")
    if (user[5] == 'sparonline36'):
        await bot.send_message(admin_id, f"Нету смены\n"
                                         f"{user[1]}")
    elif (user[5] == 'sparonline38'):
        await bot.send_message(admin_id38, f"Нету смены\n"
                                           f"{user[1]}")


async def accept(messege: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(messege.from_user.id)
    await messege.answer(f"✅Запрос отправлен")

    if (user[4] == 'М'):
        str = f"#смена_в_работе\n {user[1]}\n Потвердил смену"
    elif (user[4] == "Ж"):
        str = f"#смена_в_работе\n {user[1]}\n Потвердила смену"

    if (user[5] == 'sparonline36'):
        await bot.send_message(admin_id, str)
    elif (user[5] == 'sparonline38'):
        await bot.send_message(admin_id38, str)


async def ack(messege: Message):
    str = f"Акты,{messege.from_user.id},0"
    q.put(str)
    await accept_all()


async def accept_all():
    for i in range(q.qsize()):
        print(q.qsize())
        str = q.get()
        name = str.split(",")
        if (name[0] == 'Смена'):
            db = Database(os.getenv("DATABASE_NAME"))
            user = db.select_user_id(name[1])
            try:
                str, id = done(name[1])
            except:
                try:
                    str, id = done(name[1])
                except:

                    str = "❌Возникла ошибка, повторите попытку позже.При возникновении ошибки еще раз, напишите в группу"

            if (user[5] == 'sparonline36'):
                await bot.send_message(admin_id, f"{user[1]}\n"
                                                 f"{str}")
            elif (user[5] == 'sparonline38'):
                await bot.send_message(admin_id38, f"{user[1]}\n"
                                                   f"{str}")
                await bot.send_message(admin_id, f"{user[1]}\n"
                                                 f"{str}")
            await bot.send_message(id, str)
        elif (name[0] == 'Заказ'):
            x1 = name[2]
            x, y = (int(x) for x in x1.split())
            db = Database(os.getenv("DATABASE_NAME"))
            user = db.select_user_id(name[1])
            if (user[5] == 'sparonline36'):
                await bot.send_message(admin_id, cmenadd(x, y))
            elif (user[5] == 'sparonline38'):
                str = cmenad38(x, y)
                await bot.send_message(admin_id38, str)
                await bot.send_message(admin_id, str)
        elif (name[0] == 'Акты'):
            print("Эворвово")
            await bot.send_message(admin_id, ackt())
    return


async def echo(message: types.Message):
    print(message.text)


dp.message.register(cmena, F.text == "Смена")
dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands="start"))
dp.message.register(start_register, F.text == "Pегистрация")
dp.message.register(mes, F.text == "Нету смены")
dp.message.register(report, F.text == "Отчёт")
dp.message.register(ack, F.text == "Aкты")
dp.message.register(cmenaad, F.text == "Заказы")
dp.message.register(time, F.text == "Время")
dp.message.register(accept, F.text == "Потвердил(а) смену")
dp.message.register(dataget, F.text == "Изменить БД")
dp.message.register(registor_name, RegistorState.regName)
dp.message.register(registor_gen, RegistorState.reggen)
dp.message.register(registor_mag, RegistorState.regmag)
dp.message.register(registor_otch, RegistorState.regotch)
dp.message.register(registor_work, RegistorState.regWork)
dp.message.register(registor_phone, RegistorState.regphone)
dp.message.register(editacktid, RegistorState.editacktid)
dp.message.register(editackt, RegistorState.editackt)
dp.message.register(cmenaun, RegistorState.cmena)
dp.message.register(state_Work, RegistorState.work)

async def sendsms(phone):
    if phone == "+79872882377":
        proxies = {
            'http': 'http://192.168.150.19:8080',
            'https': 'http://192.168.150.19:8080'
        }
        print("dhf")
        print(phone)
        json = {"phone": f"{phone}"}
        print(json)
        r = requests.post("https://job.myspar.ru/auth/self-employed/login", json=json)
        print(r.status_code)
        print(r.text)
        linksms = r.text
        db = Databascmena(os.getenv("DATABASE_NAMEcmena"))
        db.add_usercmena(linksms, phone)
    return("OK")
async def getsmena(smc):
    proxies = {
        'http': 'http://192.168.150.19:8080',
        'https': 'http://192.168.150.19:8080'
    }
    print(smc)
    str1 = smc.split(":")
    print(str1)
    str2 = str1[1].split(" ")
    print(str2)
    phone = str2[2]
    smss = str2[1]
    current_date = date.today()
    print(current_date)
    data = current_date.strftime("%d.%m.%Y")
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_phone(phone)

    executorId = user[7]
    if (user[5] == 'sparonline36'):
        phoneadm ="+79375273558"
    elif (user[5] == 'sparonline38'):
        phoneadm ="+79302607421"

    for attempt in range(3):
        try:
            json1 = {"phone": f"{phoneadm}"}
            r0 = requests.post("https://job.myspar.ru/auth/employee/login", json=json1, proxies=proxies)
            print(r0.status_code)
            print(r0.text)
            str0 = eval(r0.text)
            str01 = str0['accessToken']
            print(str01)
            headersad = {'Authorization': f'Bearer {str01}'}
            json1 = {"serviceId": "2b5bf5a8-406f-407c-af5a-93d902ba732c", "planAssignmentsCount": "1",
                     "dateTime": f"{data}, 08:00", "shopId": "23b5e381-a42f-4ab3-963a-ab4e9c993c16"}
            r = requests.post("https://job.myspar.ru/api/order/create", json=json1, headers=headersad, proxies=proxies)
            print(r.status_code)
            print(r.text)
            str23 = json.loads(r.text)
            print(str23['id'])
            orderId = str23['id']
        except:
            print("Something went")
        else:
            break
    else:
        return("Ошибка при создание смены",phone)

    for attempt in range(3):
        try:
            db = Databascmena(os.getenv("DATABASE_NAMEcmena"))
            cmena = db.select_cmena_phone(phone)
            str = {"phone": f"{phone}", "code": f"{smss}"}
            print(str)
            print(cmena[1])
            str.update(eval(cmena[1]))
            print(str)
            s2 = str
            print(s2)
            r2 = requests.post("https://job.myspar.ru/auth/self-employed/login/sms-code", json=str, proxies=proxies)
            print(r2.status_code)
            print(r2.text)
            str2 = eval(r2.text)
            print(str2)
            str21 = str2['accessToken']
            print(str21)
        except:
            print("ошибка при входе")
        else:
            break
    else:
        return("Серьезная ошибка при входе",phone)

    for attempt in range(3):
        try:
            headers = {'Authorization': f'Bearer {str21}'}
            json1 = {"orderId": f"{orderId}", "comment": ""}
            r3 = requests.post("https://job.myspar.ru/api/order/response/make", json=json1, headers=headers, proxies=proxies)
            print(r3.status_code)
            print(r3.text)

        except:
         print("Ошибка при взятии смены")
        else:
            break
    else:
        return("Серьезная ошибка при взятие смены",phone)

    db = Databascmena(os.getenv("DATABASE_NAMEcmena"))
    db.delete_recordcmena(phone)

    for attempt in range(10):
        try:
            json1 = {"id": f"{orderId}", "executorId": f"{executorId}"}
            r4 = requests.post("https://job.myspar.ru/api/order/set-executor", json=json1, headers=headersad,
                               proxies=proxies)
            print(r4.status_code)
            print(r4.text)
        except:
            print("ошибка при одобрение смены")
        else:
            break
    else:
        return("ошибка при одобрение смены",phone)

    for attempt in range(3):
        try:
            json1 = {"id": f"{orderId}"}
            r4 = requests.post("https://job.myspar.ru/api/order/confirm", json=json1, headers=headers, proxies=proxies)
            print(r4.status_code)
            print(r4.text)
        except:
            print("ошибка при потверждении смены")
        else:
            break
    else:
        return("ошибка при потверждении смены",phone)

    return ("Смена была взята и потверждена.Пожалуста проверьте что в актуальных заказах есть смена", phone)

async def start():
    await set_commands(bot)

    try:
        await time("gdfg")
        await dp.start_polling(bot, skip_updates=True)

    finally:
        await bot.session.close()


class Item(BaseModel):
    text: str

app = FastAPI()

@app.post("/")
async def create_item(item: Item):
    print(item.text)
    str, phone = await getsmena(item.text)
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_phone(phone)
    await bot.send_message(user[3], str)
    return item




if __name__ == "__main__":
    asyncio.run(start())


