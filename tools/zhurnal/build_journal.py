#!/usr/bin/env python3
"""Фирменный журнал пест-контроля ПЕСТКОНТРОЛЬ Центр: образец заполнения и пустой бланк (HTML -> PDF через Chromium).

python3 build_journal.py <fonts_dir> <out_dir>
Создаёт out_dir/sample.html и out_dir/blank.html.
"""
import html
import pathlib
import sys

FONTS = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

E = html.escape

# ---------------------------------------------------------------- реквизиты
CO = {
    'brand': 'ПЕСТКОНТРОЛЬ Центр',
    'legal': 'ООО «Центр дезинфекционных услуг»',
    'inn': '7714462211', 'kpp': '771401001', 'ogrn': '1207700257775',
    'addr': '123007, г.\u00a0Москва, 2-й Хорошёвский проезд, д.\u00a07, к.\u00a01, помещ.\u00a01',
    'lic': '№\u00a0Л064-00111-77/01942445',
    'phone': '+7 (495) 104-35-70', 'mail': 'b2b@pestcontrol-center.ru', 'site': 'пестконтроль-центр.рф',
}

LOGO = ('<svg class="lg" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#09090b"/>'
        '<g transform="translate(12 12)" fill="none" stroke-width="1.6" stroke-linejoin="round">'
        '<path d="M12 2.5l7.5 3v6c0 5-3.2 8.6-7.5 10-4.3-1.4-7.5-5-7.5-10v-6z" stroke="#fff"/>'
        '<circle cx="12" cy="11.5" r="2.6" stroke="#7c86ff"/>'
        '<path d="M12 6.2v2.7M12 14.1v2.7M6.8 11.5h2.6M14.6 11.5h2.6" stroke="#7c86ff"/></g></svg>')

SIGS = {
    'smirnov': 'M2 14c3-9 6-11 7-6s-2 9 1 6 4-10 6-8-1 9 2 7 3-5 5-4 1 4 4 3 5-2 9-3',
    'orlov': 'M3 12c2-6 7-8 8-3s-5 7-3 6 6-9 8-7-2 6 1 6 4-4 6-4 2 3 5 2 6-3 8-3',
    'ivanova': 'M2 9c4 0 4 7 6 5s2-9 4-8 0 9 3 8 3-7 5-6 0 6 3 5 4-5 6-4 1 3 6 1',
    'kozlov': 'M2 13c3-7 5-9 6-5s-3 6 0 5 5-8 7-6-2 7 2 5 4-3 7-3 4 2 8 0',
    'petrova': 'M2 10c3-4 6-5 6-1s-4 5-1 4 4-6 7-5-1 6 2 4 5-4 7-3 2 3 7 1',
}


def sig(who, w=46):
    return (f'<svg class="sig" viewBox="0 0 54 18" width="{w}" height="{w*18/54:.1f}" aria-hidden="true">'
            f'<path d="{SIGS[who]}" fill="none" stroke="#1f3fae" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------------------------------------------------------- данные образца
J_NO = 'ПК-0917/26'
OBJ = {
    'name': 'Производство хлебобулочных изделий ООО «Пекарня Пример»',
    'addr': 'Московская обл., г.\u00a0о. Химки, ул.\u00a0Примерная, д.\u00a01, стр.\u00a02',
    'cust': 'ООО «Пекарня Пример», ИНН 50••••••••',
    'contract': '№\u00a00917-ПК/26 от 28.08.2026',
    'resp_c': 'Иванова Е.\u00a0В., менеджер по качеству (приказ №\u00a041-П от 01.09.2026)',
    'resp_e': 'Смирнов А.\u00a0Н., инженер пест-менеджер',
    'start': '02.09.2026',
}

POINTS = [
    # code, type, contour, place, threshold
    ('КИК-01', 'Станция с приманкой, запираемая', '1', 'Территория, северный забор у КПП', 'до 25 %'),
    ('КИК-02', 'Станция с приманкой, запираемая', '1', 'Территория, северо-восточный угол забора', 'до 25 %'),
    ('КИК-03', 'Станция с приманкой, запираемая', '1', 'Контейнерная площадка ТКО', 'до 25 %'),
    ('КИК-04', 'Станция с приманкой, запираемая', '1', 'Рампа экспедиции, слева от дока №\u00a01', 'до 25 %'),
    ('КИК-05', 'Станция с приманкой, запираемая', '1', 'Отмостка восточной стены здания', 'до 25 %'),
    ('КИК-06', 'Станция с приманкой, запираемая', '1', 'Ворота приёмки склада сырья, снаружи', 'до 25 %'),
    ('КИК-07', 'Станция с приманкой, запираемая', '1', 'Южная стена, у вентшахты', 'до 25 %'),
    ('КИК-08', 'Станция с приманкой, запираемая', '1', 'Вход в АБК, справа', 'до 25 %'),
    ('МЛ-01', 'Ловушка механич. / клеевая, без яда', '2', 'Экспедиция, док №\u00a01, справа от ворот', '0'),
    ('МЛ-02', 'Ловушка механич. / клеевая, без яда', '2', 'Экспедиция, док №\u00a01, слева от ворот', '0'),
    ('МЛ-03', 'Ловушка механич. / клеевая, без яда', '2', 'Экспедиция, вдоль северной стены', '0'),
    ('МЛ-04', 'Ловушка механич. / клеевая, без яда', '2', 'Экспедиция, у ворот №\u00a02', '0'),
    ('МЛ-05', 'Ловушка механич. / клеевая, без яда', '2', 'Склад сырья, ворота приёмки, справа', '0'),
    ('МЛ-06', 'Ловушка механич. / клеевая, без яда', '2', 'Склад сырья, ворота приёмки, слева', '0'),
    ('МЛ-07', 'Ловушка механич. / клеевая, без яда', '2', 'Коридор АБК у входа в цех', '0'),
    ('МЛ-08', 'Ловушка механич. / клеевая, без яда', '2', 'Электрощитовая', '0'),
    ('МЛ-09', 'Ловушка механич. / клеевая, без яда', '3', 'Склад сырья, стеллаж А-1', '0'),
    ('МЛ-10', 'Ловушка механич. / клеевая, без яда', '3', 'Склад сырья, стеллаж А-2', '0'),
    ('ИМ-01', 'Клеевой монитор насекомых', '3', 'Склад сырья, у просеивателя муки', '0'),
    ('ИМ-02', 'Клеевой монитор насекомых', '3', 'Цех, тестомесильное отделение', '0'),
    ('ИМ-03', 'Клеевой монитор насекомых', '3', 'Цех, моечное отделение, за ванной', '0'),
    ('ИМ-04', 'Клеевой монитор насекомых', '3', 'Цех, зона печей', '0'),
    ('ИМ-05', 'Клеевой монитор насекомых', '3', 'Упаковка, у стола фасовки', '0'),
    ('ИМ-06', 'Клеевой монитор насекомых', '3', 'Комната приёма пищи персонала', '0'),
    ('ИЛ-01', 'Световая УФ-ловушка', '3', 'Экспедиция, над входом из цеха', 'до 20 за 14 сут'),
    ('ИЛ-02', 'Световая УФ-ловушка', '3', 'Цех, у входа из коридора', 'до 10 за 14 сут'),
    ('ИЛ-03', 'Световая УФ-ловушка', '3', 'Упаковка', 'до 5 за 14 сут'),
    ('ИЛ-04', 'Световая УФ-ловушка', '3', 'Склад сырья', 'до 10 за 14 сут'),
    ('ФЛ-01', 'Феромонная (пищевые огнёвки)', '3', 'Склад муки, стеллаж Б-1', 'до 2 за 14 сут'),
    ('ФЛ-02', 'Феромонная (пищевые огнёвки)', '3', 'Склад сухих ингредиентов', 'до 2 за 14 сут'),
]
CONTOUR = {'1': 'К1 · территория', '2': 'К2 · периметр здания', '3': 'К3 · внутренние помещения'}
CSHORT = {'1': 'К1 · территория', '2': 'К2 · периметр', '3': 'К3 · помещения'}

VISITS = ['02.09', '16.09', '30.09', '14.10', '21.10', '28.10', '11.11', '']
VKIND = ['план', 'план', 'план', 'план', 'внепл.', 'план', 'план', '']
V5_SCOPE = {'КИК-06', 'МЛ-05', 'МЛ-06', 'МЛ-09', 'МЛ-10', 'ИМ-01', 'ИЛ-04', 'ФЛ-01', 'ФЛ-02'}
OVR = {
    1: {'КИК-03': 'П25/З', 'ИЛ-01': 'Н14', 'ИЛ-02': 'Н6', 'ИЛ-03': 'Н3', 'ИЛ-04': 'Н5', 'ФЛ-01': 'Н2'},
    2: {'КИК-03': 'П10', 'КИК-05': 'П50/З', 'МЛ-04': 'Д', 'ИЛ-01': 'Н11/З', 'ИЛ-02': 'Н4/З', 'ИЛ-03': 'Н2/З', 'ИЛ-04': 'Н3/З', 'ФЛ-01': 'Н1',
        **{f'ИМ-0{i}': '0/З' for i in range(1, 7)}},
    3: {'КИК-05': 'П20/З', 'ИМ-03': 'Н2', 'ИЛ-01': 'Н7', 'ИЛ-02': 'Н3', 'ИЛ-03': 'Н1', 'ИЛ-04': 'Н2'},
    4: {'МЛ-10': 'М1/З', 'ИЛ-04': 'Н1'},
    5: {'КИК-05': 'П5', 'ИЛ-01': 'Н4/З', 'ИЛ-02': 'Н2/З', 'ИЛ-03': '0/З', 'ИЛ-04': 'Н1/З',
        **{f'ИМ-0{i}': '0/З' for i in range(1, 7)}},
}


def cell(vi, code):
    if vi == 0:
        return 'У'
    if vi >= 6:
        return ''
    if vi == 4 and code not in V5_SCOPE:
        return '—'
    v = OVR.get(vi, {}).get(code)
    if v:
        return v
    return '0'


AGENTS = [
    ('Родентицидная приманка, парафинированный брикет 20\u00a0г, с горьким веществом', 'бродифакум 0,005\u00a0%', 'Только станции К1 (территория), запираемые, закреплённые. В помещениях с пищевой продукцией не применяется'),
    ('Клеевые пластины для грызунов (без действующего вещества)', '—', 'Механические ловушки МЛ контуров 2–3'),
    ('Инсектицидный гель от тараканов', 'имидаклоприд 2,15\u00a0%', 'Точечно, в щели и полости по показаниям; не на поверхности, контактирующие с продукцией'),
    ('Клеевые мониторы для ползающих насекомых', '—', 'ИМ-01…06, замена не реже 1\u00a0раза в месяц и при загрязнении'),
    ('Сменные клеевые экраны световых ловушек', '—', 'ИЛ-01…04, замена 1\u00a0раз в месяц; лампы — 1\u00a0раз в год'),
    ('Феромонные диспенсеры для пищевых огнёвок', 'феромон (аттрактант)', 'ФЛ-01…02, замена капсулы 1\u00a0раз в 6–8\u00a0недель'),
    ('Дезинфицирующее средство для обработки корпусов станций', 'ЧАС + амины', 'Мойка корпусов КИК и МЛ, рабочий раствор по инструкции'),
]
SGR_MASK = 'RU.77.99.••.•••.Е.••••••.••.••'

LOG = [
    ('02.09.2026', '09:30–12:40', 'Плановый, первичный', 'Обследование объекта. Установка и маркировка 30 ТПК по план-схеме (прил.\u00a01). Заправка КИК-01…08. Инструктаж персонала.',
     '№1 — 320 г (8×40 г); №2 — 10 шт.; №4 — 6 шт.; №5 — 4 шт.; №6 — 2 шт.', '0917-01', 'smirnov'),
    ('16.09.2026', '10:00–11:35', 'Плановый', 'Осмотр 30 ТПК. КИК-03 — поедаемость 25 %, приманка заменена. ФЛ-01 — 2 огнёвки (предписание №\u00a03).',
     '№1 — 40 г', '0917-02', 'smirnov'),
    ('30.09.2026', '10:10–12:05', 'Плановый', 'Осмотр 30 ТПК. КИК-05 — 50 %, норы у отмостки (пр.\u00a0№\u00a04). МЛ-04 — нет доступа (пр.\u00a0№\u00a05). Замена экранов ИЛ и мониторов ИМ, мойка станций.',
     '№1 — 40 г; №4 — 6 шт.; №5 — 4 шт.; №7 — 0,5 л р-ра', '0917-03', 'smirnov'),
    ('14.10.2026', '09:40–12:20', 'Плановый + дезинсекция по показаниям', 'Осмотр 30 ТПК. ИМ-03 — рыжий таракан, 2 особи (сигнал №\u00a01). Точечная обработка моечного отделения гелем: шов за ванной, кабель-канал, 12 м².',
     '№3 — 6 г; №1 — 40 г', '0917-04', 'smirnov'),
    ('21.10.2026', '08:50–10:10', 'Внеплановый (сигнал №\u00a02)', 'Осмотр склада сырья и ворот приёмки, 9 ТПК. МЛ-10 — мышь домовая, 1 особь. Найден негерметичный ввод кабеля в стене (пр.\u00a0№\u00a07).',
     '№2 — 1 шт.', '0917-05', 'orlov'),
    ('28.10.2026', '10:00–11:50', 'Плановый, контроль эффективности', 'Осмотр 30 ТПК. ИМ-03 — 0: дезинсекция эффективна. МЛ-10 — 0. Замена экранов ИЛ и мониторов ИМ.',
     '№4 — 6 шт.; №5 — 4 шт.; №7 — 0,5 л р-ра', '0917-06', 'smirnov'),
]

INSECTS = [
    ('16.09', 'ИЛ-01…04', 'Мухи комнатные — 22; плодовые мушки — 6', '28', 'норма', 'Плановая замена экранов 30.09'),
    ('16.09', 'ФЛ-01', 'Огнёвка южная амбарная, имаго — 2', '2', 'на пороге', 'Предписание №\u00a03: уборка просыпей, проверка партий'),
    ('30.09', 'ИЛ-01…04', 'Мухи комнатные — 16; плодовые мушки — 4', '20', 'норма', 'Экраны заменены'),
    ('30.09', 'ФЛ-01', 'Огнёвка южная амбарная, имаго — 1', '1', 'норма', 'Контроль на следующем визите'),
    ('14.10', 'ИМ-03', 'Рыжий таракан (Blattella germanica), имаго — 2', '2', 'превышение', 'Дезинсекция гелем, акт 0917-04; предписание №\u00a06'),
    ('14.10', 'ИЛ-01…04', 'Мухи комнатные — 10; плодовые мушки — 3', '13', 'норма', '—'),
    ('28.10', 'ИЛ-01…04', 'Мухи комнатные — 6; плодовые мушки — 1', '7', 'норма', 'Экраны заменены'),
    ('28.10', 'ИМ-03', 'Не обнаружено (контроль через 14 сут)', '0', 'норма', 'Эффективность подтверждена'),
]

ACTIONS = [
    ('1', '02.09', 'МЛ-01', 'Док №\u00a01: износ нижнего уплотнителя ворот, зазор около 10\u00a0мм', 'Заменить уплотнитель, до ремонта держать ПВХ-завесу закрытой', 'Гл. инженер, до 16.09', 'Выполнено 15.09', '16.09', 'ivanova'),
    ('2', '02.09', 'ИЛ-04', 'Склад сырья: разрыв защитной сетки приточной решётки', 'Заменить сетку на приточной решётке', 'Гл. инженер, до 30.09', 'Выполнено 25.09', '30.09', 'ivanova'),
    ('3', '16.09', 'ФЛ-01', 'Склад муки: просыпи под стеллажом Б-1, огнёвка в ловушке', 'Уборка просыпей, осмотр партий муки, соблюдение FIFO', 'Нач. склада, до 18.09', 'Выполнено 17.09', '30.09', 'petrova'),
    ('4', '30.09', 'КИК-05', 'Территория: 2 норы у отмостки, строительный мусор', 'Засыпать и утрамбовать норы, вывезти мусор', 'АХО, до 07.10', 'Выполнено 06.10', '14.10', 'ivanova'),
    ('5', '30.09', 'МЛ-04', 'Экспедиция: ловушка заставлена паллетами', 'Освободить доступ, сохранять проход вдоль стены', 'Нач. экспедиции, сразу', 'Выполнено 30.09', '14.10', 'kozlov'),
    ('6', '14.10', 'ИМ-03', 'Моечная: отслоение герметика за ванной, влага, остатки теста', 'Санобработка за ванной, герметизация шва', 'Нач. цеха, до 21.10', 'Выполнено 20.10', '28.10', 'kozlov'),
    ('7', '21.10', 'МЛ-10', 'Склад сырья: ввод кабеля в стене не загерметизирован, отверстие ~15\u00a0мм', 'Заделать металлической сеткой и герметиком', 'Гл. инженер, до 28.10', 'Выполнено 27.10', '28.10', 'ivanova'),
    ('8', '28.10', 'КИК-03', 'Площадка ТКО: крышки контейнеров не закрываются', 'Заменить контейнеры или крышки, держать закрытыми', 'АХО, до 11.11', 'В работе', '', None),
]

SIGNALS = [
    ('1', '13.10.2026 19:40', 'Цех, моечное отделение', 'Таракан у моечной ванны', 'Козлов И.\u00a0А., мастер смены', 'Ивановой Е.\u00a0В. 14.10, 08:15', '14.10, визит №\u00a04: подтверждено (ИМ-03 — Н2), обработка, пр.\u00a0№\u00a06', 'kozlov', 'smirnov'),
    ('2', '20.10.2026 14:30', 'Склад сырья, стеллаж А-2', 'Помёт мыши на полу у поддона', 'Петрова О.\u00a0С., кладовщик', 'Ивановой Е.\u00a0В. 14:45; заявка Исполнителю 15:05', '21.10, визит №\u00a05: МЛ-10 — М1, пр.\u00a0№\u00a07', 'petrova', 'orlov'),
]

BRIEF = [
    ('02.09.2026', 'Персонал склада, экспедиции и цеха — 14 чел. (лист регистрации прил.\u00a05)', 'Назначение ТПК, запрет перемещать ловушки; как заполнять сигнальный лист', 'Смирнов А.\u00a0Н.', 'smirnov'),
]

MONTHS = [
    ('Сентябрь 2026', '3 / 0', '90', 'К1: поедаемость в 2 осмотрах (КИК-03, КИК-05). К2–К3: 0', 'ИЛ — 48; ФЛ — 3 огнёвки; ИМ — 0', '5 / 5', 'Умеренный: норы у КИК-05'),
    ('Октябрь 2026', '2 / 1', '69', 'К1: КИК-05 20 % → 5 %. К3: мышь в МЛ-10 (21.10), вход закрыт', 'ИЛ — 20; ИМ-03 — 2 таракана → 0; ФЛ — 0', '3 / 2', 'Снижается. Открыто пр.\u00a0№\u00a08'),
]


# ---------------------------------------------------------------- CSS
def css():
    f = FONTS.as_uri()
    return f"""
@font-face{{font-family:Inter;font-style:normal;font-weight:100 900;src:url({f}/inter-ru-wght-normal.woff2) format("woff2");unicode-range:U+0020-007E,U+00A0,U+00A9,U+00AB,U+00AD,U+00B0,U+00B7,U+00BB,U+00D7,U+0401,U+0410-044F,U+0451,U+2009,U+2010-2015,U+2018-201E,U+2022,U+2026,U+202F,U+2116,U+20BD,U+2192,U+2212}}
@font-face{{font-family:Inter;font-style:normal;font-weight:100 900;src:url({f}/inter-latin-wght-normal.woff2) format("woff2");unicode-range:U+0000-001F,U+007F-009F,U+00A1-00A8,U+00AA,U+00AC,U+00AE-00AF,U+00B1-00B6,U+00B8-00BA,U+00BC-00D6,U+00D8-00FF,U+2000-2008,U+200A-200F,U+2016-2017,U+201F-2021,U+2023-2025,U+2027-202E,U+2030-206F,U+2122,U+2191,U+2193}}
@font-face{{font-family:Inter;font-style:normal;font-weight:100 900;src:url({f}/inter-cyrillic-wght-normal.woff2) format("woff2");unicode-range:U+0400,U+0402-040F,U+0450,U+0452-045F}}
@font-face{{font-family:Inter;font-style:italic;font-weight:100 900;src:url({f}/inter-ru-wght-italic.woff2) format("woff2");unicode-range:U+0020-007E,U+00A0,U+00A9,U+00AB,U+00AD,U+00B0,U+00B7,U+00BB,U+00D7,U+0401,U+0410-044F,U+0451,U+2009,U+2010-2015,U+2018-201E,U+2022,U+2026,U+202F,U+2116,U+20BD,U+2192,U+2212}}
@font-face{{font-family:Inter;font-style:italic;font-weight:100 900;src:url({f}/inter-latin-wght-italic.woff2) format("woff2");unicode-range:U+0000-001F,U+007F-009F,U+00A1-00A8,U+00AA,U+00AC,U+00AE-00AF,U+00B1-00B6,U+00B8-00BA,U+00BC-00D6,U+00D8-00FF,U+2000-206F}}
@page{{size:A4 portrait;margin:0}}
@page land{{size:A4 landscape;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#fff}}
body{{font-family:Inter,Arial,sans-serif;color:#18181b;font-size:8.6pt;line-height:1.35;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;padding:11mm 12mm 9mm 20mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;display:flex;flex-direction:column}}
.pg.land{{page:land;width:297mm;height:210mm;padding:10mm 12mm 8mm 16mm}}
.pg:last-child{{page-break-after:auto;break-after:auto}}
.wm{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-32deg);font-size:76pt;font-weight:800;letter-spacing:.08em;color:rgba(97,95,255,.055);white-space:nowrap;pointer-events:none;z-index:0}}
.pg>*{{position:relative;z-index:1}}
.pg>.wm{{position:absolute;z-index:0}}
/* шапка */
.hd{{display:flex;align-items:center;justify-content:space-between;gap:10mm;padding-bottom:3mm;border-bottom:.6mm solid #615fff}}
.brand{{display:flex;align-items:center;gap:3mm}}
.lg{{width:10mm;height:10mm;flex:none}}
.bn{{font-weight:700;font-size:12.5pt;letter-spacing:-.015em;line-height:1;white-space:nowrap}}
.bn small{{font-weight:600;font-size:6.6pt;color:#615fff;letter-spacing:.16em;margin-left:1.6mm;vertical-align:.18em}}
.bt{{font-size:6.6pt;color:#71717a;margin-top:1.1mm;white-space:nowrap}}
.hr{{text-align:right;font-size:6.8pt;color:#52525b;line-height:1.45;white-space:nowrap}}
.badge{{display:inline-block;font-size:6.4pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:.9mm 2.4mm;border-radius:1mm;margin-bottom:1mm}}
.b-s{{background:#fdc700;color:#09090b}}
.b-b{{background:#eceeff;color:#3f3dcc}}
.hd.sm .lg{{width:7.5mm;height:7.5mm}}
.hd.sm .bn{{font-size:10pt}}
.hd.sm{{padding-bottom:2.2mm}}
.jmeta{{font-size:6.8pt;color:#52525b}}
.jmeta b{{color:#18181b;font-weight:600}}
/* подвал */
.ft{{margin-top:auto;padding-top:2.2mm;border-top:.25mm solid #d4d4d8;display:flex;justify-content:space-between;gap:6mm;font-size:6pt;color:#71717a;line-height:1.4}}
.ft b{{color:#18181b;font-weight:600}}
.ft .pn{{white-space:nowrap;font-weight:600;color:#18181b}}
/* разделы */
.sec{{display:flex;align-items:baseline;gap:2.6mm;margin:4.2mm 0 1.6mm}}
.sec .n{{flex:none;font-size:7pt;font-weight:700;color:#fff;background:#615fff;border-radius:1mm;padding:.6mm 1.8mm;letter-spacing:.04em;position:relative;top:-.3mm}}
.sec h2{{font-size:11.5pt;font-weight:700;letter-spacing:-.01em;margin:0;line-height:1.2}}
.lead{{font-size:7.3pt;color:#52525b;margin:0 0 2.2mm;line-height:1.4}}
table{{width:100%;border-collapse:collapse;table-layout:fixed}}
th,td{{border:.2mm solid #a1a1aa;padding:1.05mm 1.3mm;vertical-align:top;text-align:left;font-size:7.3pt;line-height:1.3;word-wrap:break-word;overflow-wrap:anywhere;hyphens:auto}}
th{{background:#eceeff;font-weight:600;font-size:6.6pt;color:#27272a;vertical-align:middle;line-height:1.22}}
th.c,td.c{{text-align:center}}
td.mono{{font-variant-numeric:tabular-nums}}
.ink{{font-style:italic;color:#1f3fae;font-weight:500}}
td.ink,td .ink{{font-style:italic;color:#1f3fae;font-weight:500}}
.sig{{display:inline-block;vertical-align:middle}}
.tight td{{padding-top:.8mm;padding-bottom:.8mm}}
.rowh td{{height:7.2mm}}
.note{{font-size:6.6pt;color:#52525b;line-height:1.4;margin:1.6mm 0 0}}
.note b{{color:#18181b}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}
.box{{border:.25mm solid #a1a1aa;border-radius:1.2mm;padding:2.6mm 3mm}}
.box h3{{font-size:7.4pt;text-transform:uppercase;letter-spacing:.08em;color:#615fff;margin:0 0 1.6mm;font-weight:700}}
.kv{{display:grid;grid-template-columns:30mm 1fr;gap:.9mm 3mm;font-size:7.6pt}}
.kv span{{color:#71717a}}
.line{{border-bottom:.2mm solid #71717a;min-height:4.6mm;display:block}}
/* титул */
.t-hd{{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:4mm;border-bottom:.7mm solid #615fff}}
.t-hd .lg{{width:15mm;height:15mm}}
.t-hd .bn{{font-size:17pt}}
.t-hd .bn small{{font-size:8pt}}
.t-hd .bt{{font-size:7.6pt}}
.t-hd .hr{{font-size:7.8pt}}
.t-main{{margin:9mm 0 4mm}}
.t-kicker{{font-size:8pt;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:#615fff}}
.t-title{{font-size:34pt;font-weight:800;letter-spacing:-.035em;line-height:1;margin:3mm 0 2.5mm}}
.t-sub{{font-size:12pt;color:#3f3f46;line-height:1.3;max-width:178mm}}
.t-no{{display:inline-flex;align-items:center;gap:3mm;margin-top:5mm;font-size:10pt;font-weight:600}}
.t-no i{{font-style:normal;border:.35mm solid #09090b;border-radius:1.2mm;padding:1.2mm 3.4mm;font-size:12pt;letter-spacing:.02em}}
.t-fields{{width:100%;border-collapse:collapse;margin-top:2mm}}
.t-fields td{{border:0;border-bottom:.2mm solid #a1a1aa;padding:2.3mm 0 1.3mm;font-size:8.6pt;vertical-align:bottom}}
.t-fields td:first-child{{width:56mm;color:#71717a;font-size:7.6pt;padding-right:3mm}}
.t-dates{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6mm;margin-top:5mm}}
.t-dates div{{border:.3mm solid #09090b;border-radius:1.2mm;padding:2.4mm 3mm}}
.t-dates>div>span{{display:block;font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;color:#71717a;margin-bottom:1.6mm}}
.t-dates b{{font-size:11pt;font-weight:600;min-height:5mm;display:block}}
.t-exec{{margin-top:7mm;display:grid;grid-template-columns:1.25fr 1fr;gap:5mm}}
.t-exec .box{{font-size:7.5pt;line-height:1.5}}
.t-exec .box p{{margin:0}}
.toc{{list-style:none;margin:0;padding:0;columns:1;font-size:7.5pt;line-height:1.55}}
.toc li{{display:flex;gap:2mm}}
.toc li b{{color:#615fff;width:7mm;flex:none}}
.toc li i{{margin-left:auto;font-style:normal;color:#71717a;white-space:nowrap;padding-left:2mm}}
.t-foot{{margin-top:auto;font-size:6.8pt;color:#52525b;line-height:1.45;padding-top:3mm;border-top:.25mm solid #d4d4d8}}
/* матрица */
.mx th,.mx td{{font-size:6.5pt;padding:.42mm 1mm;line-height:1.13}}
.mx td.v{{text-align:center;font-style:italic;color:#1f3fae;font-weight:600}}
.mx td.v.hl{{background:#fff4c2}}
.mx td.v.cr{{background:#ffe1e1}}
.mx td.v.na{{color:#a1a1aa;font-style:normal;font-weight:400}}
.mx tr.zone td{{background:#f4f4f5;font-weight:600;font-size:6.4pt;letter-spacing:.06em;text-transform:uppercase;color:#52525b;padding:.35mm 1mm}}
.legend{{display:flex;flex-wrap:wrap;gap:1.2mm 4mm;font-size:6.5pt;color:#3f3f46;margin-top:1.8mm}}
.legend b{{display:inline-block;min-width:5.4mm;text-align:center;border:.2mm solid #a1a1aa;border-radius:.8mm;margin-right:1mm;font-weight:700;color:#1f3fae;font-style:italic}}
.chart{{margin-top:3mm;display:grid;grid-template-columns:1fr 64mm;gap:5mm;align-items:start}}
.stamp{{display:inline-grid;place-items:center;width:30mm;height:30mm;border:.3mm dashed #a1a1aa;border-radius:50%;color:#a1a1aa;font-size:7pt;letter-spacing:.1em}}
.cert{{margin-top:5mm;border:.35mm solid #09090b;border-radius:1.4mm;padding:4mm 5mm}}
.cert h3{{margin:0 0 2mm;font-size:9pt;text-transform:uppercase;letter-spacing:.1em}}
.cert .row{{display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:4mm;font-size:7.5pt}}
.rules{{margin:0;padding-left:4.2mm;font-size:7.3pt;line-height:1.45}}
.rules li{{margin-bottom:.6mm}}
"""


# ---------------------------------------------------------------- компоненты

def header_full(sample):
    badge = '<span class="badge b-s">Образец заполнения</span>' if sample else '<span class="badge b-b">Форма · бланк для печати</span>'
    return f"""<div class="t-hd"><div class="brand">{LOGO}<div><div class="bn">ПЕСТКОНТРОЛЬ<small>ЦЕНТР</small></div>
<div class="bt">Пест-контроль, дератизация и дезинсекция для организаций · IPM / ХАССП</div></div></div>
<div class="hr">{badge}<br>{CO['site']} · {CO['phone']}<br>{CO['mail']}</div></div>"""


def header_small(sample, sec_no, total_no):
    jn = f'<b>{J_NO}</b>' if sample else '<b>№ ________</b>'
    obj = 'ООО «Пекарня Пример», Химки' if sample else '______________________________'
    badge = '<span class="badge b-s">Образец заполнения</span>' if sample else '<span class="badge b-b">Бланк</span>'
    return f"""<div class="hd sm"><div class="brand">{LOGO}<div><div class="bn">ПЕСТКОНТРОЛЬ<small>ЦЕНТР</small></div>
<div class="jmeta">Журнал пест-контроля {jn} · Объект: {obj}</div></div></div>
<div class="hr">{badge}<br>Раздел {sec_no}</div></div>"""


def footer(page, total):
    return f"""<div class="ft"><div><b>{CO['brand']}</b> · {CO['legal']} · ИНН {CO['inn']} · ОГРН {CO['ogrn']} · Лицензия <span style="white-space:nowrap">{CO['lic']}</span><br>
{CO['addr']} · {CO['phone']} · {CO['mail']} · {CO['site']}</div><div class="pn">Лист {page} из {total}</div></div>"""


def sec(n, title, lead=''):
    s = f'<div class="sec"><span class="n">{n}</span><h2>{title}</h2></div>'
    if lead:
        s += f'<p class="lead">{lead}</p>'
    return s


def ink(v, sample):
    return f'<span class="ink">{v}</span>' if (sample and v) else ''


# ---------------------------------------------------------------- страницы

def p_title(sample):
    def fv(v):
        return f'<span class="ink">{v}</span>' if sample else ''
    rows = [
        ('Объект (наименование)', OBJ['name']),
        ('Адрес объекта', OBJ['addr']),
        ('Заказчик', OBJ['cust']),
        ('Договор на пест-контроль', OBJ['contract']),
        ('Ответственный от Заказчика', OBJ['resp_c']),
        ('Ответственный специалист Исполнителя', OBJ['resp_e']),
    ]
    trs = ''.join(f'<tr><td>{k}</td><td>{fv(v)}</td></tr>' for k, v in rows)
    no = f'<i>{J_NO}</i>' if sample else '<i>№ ____________</i>'
    start = f'<span class="ink">{OBJ["start"]}</span>' if sample else ''
    sheets = '<span class="ink">10 (десять)</span>' if sample else ''
    toc = [('1', 'Паспорт объекта и порядок ведения журнала', '2'), ('2', 'Реестр точек пест-контроля (ТПК)', '3'),
           ('3', 'Перечень применяемых средств и материалов', '4'), ('4', 'Ведомость визитов и расхода средств', '5'),
           ('5', 'Поточечный лист осмотра ТПК', '6'), ('6', 'Учёт насекомых по видам и динамика', '7'),
           ('7', 'Замечания, предписания и корректирующие действия', '8'), ('8', 'Сигнальный лист персонала · инструктажи', '9'),
           ('9', 'Ежемесячная сводка · заверительная надпись', '10')]
    toc_html = ''.join(f'<li><b>{a}</b><span>{b}</span><i>лист {c}</i></li>' for a, b, c in toc)
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_full(sample)}
<div class="t-main"><div class="t-kicker">Объектовый журнал · IPM / ХАССП</div>
<div class="t-title">ЖУРНАЛ<br>ПЕСТ-КОНТРОЛЯ</div>
<div class="t-sub">учёта мониторинга вредителей, дератизации и дезинсекции на объекте</div>
<div class="t-no">Журнал {no}</div></div>
<table class="t-fields">{trs}</table>
<div class="t-dates"><div><span>Журнал начат</span><b>{start}</b></div><div><span>Журнал окончен</span><b></b></div><div><span>Листов в журнале</span><b>{sheets}</b></div></div>
<div class="t-exec"><div class="box"><h3>Исполнитель</h3>
<p><b>{CO['brand']}</b> — {CO['legal']}</p>
<p>ИНН {CO['inn']} · КПП {CO['kpp']} · ОГРН {CO['ogrn']}</p>
<p>{CO['addr']}</p>
<p>Лицензия на дезинфекционную деятельность (Роспотребнадзор) <span style="white-space:nowrap">{CO['lic']}</span></p>
<p>{CO['phone']} · {CO['mail']}</p>
<p>{CO['site']}</p>
<p>Пн–Пт 8:00–20:00 · срочные выезды 24/7</p></div>
<div class="box"><h3>Состав журнала</h3><ul class="toc">{toc_html}</ul></div></div>
<div class="t-foot">Журнал хранится на объекте у ответственного за пест-контроль и предъявляется при проверках Роспотребнадзора, аудитах ХАССП, ISO 22000 / FSSC 22000 и торговых сетей. Основание ведения: СанПиН 3.3686-21 (раздел III, пп. 82, 98–124), МР 3.5.3.0374-25, ТР ТС 021/2011 (ст. 10), ГОСТ Р 54762-2011 (раздел 12), программа пест-контроля объекта. Листы пронумерованы; журнал прошнурован, последняя страница — заверительная надпись.</div>
{footer(1, 10)}</section>"""


def p_passport(sample):
    def v(x):
        return f'<span class="ink">{x}</span>' if sample else ''
    kv = [
        ('Вид деятельности', 'Производство хлебобулочных и мучных кондитерских изделий'),
        ('Площадь здания / территории', '1 850 м² / 3 200 м²'),
        ('Режим работы', 'Круглосуточно, 3 смены; приёмка сырья 7:00–15:00'),
        ('Зоны (контуры защиты)', 'К1 — территория; К2 — периметр здания (ворота, доки, входы); К3 — склад сырья, цех, упаковка, бытовые'),
        ('Целевые вредители', 'Мышь домовая, серая крыса; рыжий таракан; мухи; пищевые огнёвки'),
        ('Кратность визитов', '2 раза в месяц (не реже, СанПиН 3.3686-21 п. 101) + внеплановые по сигналу'),
        ('Метод', 'Мониторинг по ТПК; истребительные меры — только по показаниям'),
        ('Прилагается к журналу', 'Прил. 1 — план-схема ТПК; 2 — программа пест-контроля; 3 — договор; 4 — копии СГР/инструкций; 5 — листы инструктажа'),
    ]
    rows = ''.join(f'<span>{k}</span><div class="{"" if sample else "line"}">{v(x)}</div>' for k, x in kv)
    contacts = [
        ('Ответственный Заказчика', 'Иванова Е.\u00a0В., +7 (9••) •••-••-12'),
        ('Замещающее лицо', 'Козлов И.\u00a0А., мастер смены'),
        ('Специалист Исполнителя', 'Смирнов А.\u00a0Н., инженер пест-менеджер'),
        ('Срочная заявка', f'{CO["phone"]} · Telegram t.me/Centr_Dezinfection'),
    ]
    crow = ''.join(f'<span>{k}</span><div class="{"" if sample else "line"}">{v(x) if k != "Срочная заявка" else x}</div>' for k, x in contacts)
    if sample:
        sched = ''.join(f'<tr><td class="ink">{m}</td><td class="ink">{pd}</td><td class="ink">{fd}</td><td class="c">{sig("ivanova", 30) if fd else ""}</td></tr>' for m, pd, fd in [
            ('Сентябрь 2026', '02.09 · 16.09 · 30.09', '02.09 · 16.09 · 30.09 — по графику'),
            ('Октябрь 2026', '14.10 · 28.10', '14.10 · 28.10; внеплановый 21.10 (сигнал №\u00a02)'),
            ('Ноябрь 2026', '11.11 · 25.11', ''), ('Декабрь 2026', '09.12 · 23.12', '')])
    else:
        sched = '<tr class="rowh"><td></td><td></td><td></td><td></td></tr>' * 2
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '1', 10)}
{sec('1', 'Паспорт объекта', 'Заполняется при заведении журнала и обновляется при перепланировке, смене зон хранения или ответственных лиц.')}
<div class="box"><div class="kv">{rows}</div></div>
<div class="sec"><span class="n">1.1</span><h2>Контакты и порядок связи</h2></div>
<div class="box"><div class="kv">{crow}</div></div>
<div class="sec"><span class="n">1.2</span><h2>Порядок ведения журнала</h2></div>
<ol class="rules">
<li>Записи вносит специалист Исполнителя в день визита, до ухода с объекта. Представитель Заказчика подтверждает визит подписью в разделах 4 и 5.</li>
<li>Каждая ТПК записывается отдельно под своим номером с план-схемы. Пустые клетки не допускаются: при отсутствии находок ставится «0», при отсутствии доступа — «Д» с записью в раздел 7.</li>
<li>Для каждого применённого средства указываются номер по перечню (раздел 3), место применения и расход. Родентициды в помещениях с открытой пищевой продукцией не применяются.</li>
<li>Исправления: зачеркнуть одной линией, рядом — верная запись, дата, подпись. Подчистки, корректор и вклейка листов не допускаются.</li>
<li>Персонал объекта записывает наблюдения вредителей между визитами в сигнальный лист (раздел 8) и сообщает ответственному.</li>
<li>Ежемесячно специалист Исполнителя заполняет сводку (раздел 9) и передаёт отчёт с анализом тенденций службе качества.</li>
<li>Заполненный журнал хранится на объекте вместе с актами и план-схемой; срок хранения устанавливается внутренним порядком Заказчика.</li>
</ol>
<div class="sec"><span class="n">1.3</span><h2>График плановых визитов</h2></div>
<table class="fill" data-rh="7.5"><tr><th style="width:28mm">Месяц</th><th style="width:44mm">Плановые даты</th><th>Фактические даты, отклонения</th><th style="width:30mm" class="c">Подпись Заказчика</th></tr>{sched}</table>
{footer(2, 10)}</section>"""


def p_registry(sample):
    head = '<tr><th style="width:15mm">№ ТПК</th><th style="width:50mm">Тип устройства</th><th style="width:24mm">Контур</th><th>Место установки (по план-схеме)</th><th style="width:15mm" class="c">Уста&shy;нов&shy;лена</th><th style="width:21mm" class="c">Порог</th></tr>'
    body = ''
    if sample:
        for code, typ, ct, place, thr in POINTS:
            body += f'<tr><td class="ink">{code}</td><td>{typ}</td><td>{CSHORT[ct]}</td><td class="ink">{place}</td><td class="c ink">02.09.26</td><td class="c ink">{thr}</td></tr>'
    else:
        body = '<tr class="rowh"><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 24
    chg = ('<tr><td class="ink">21.10.2026</td><td class="ink">МЛ-10</td><td class="ink">Ловушка сдвинута на 0,5 м к углу стеллажа А-2 — ближе к найденному вводу кабеля</td><td class="c ink">да, ред. 2</td><td class="c">' + sig('orlov', 30) + '</td></tr>') if sample else ''
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    cls = 'tight' if sample else 'tight'
    return f"""<section class="pg">{wm}{header_small(sample, '2', 10)}
{sec('2', 'Реестр точек пест-контроля (ТПК)', 'Номера совпадают с план-схемой (прил. 1) и настенными указателями. Порог — уровень, при котором Исполнитель назначает корректирующие действия; устанавливается программой пест-контроля.')}
<table class="{cls}">{head}{body}</table>
<p class="note"><b>Обозначения:</b> КИК — станция контроля грызунов с приманкой; МЛ — механическая или клеевая ловушка для грызунов; ИМ — клеевой монитор насекомых; ИЛ — световая ловушка; ФЛ — феромонная ловушка. Порог для КИК — доля съеденной приманки; для ИЛ и ФЛ — число особей за 14 суток.</p>
<div class="sec"><span class="n">2.1</span><h2>Изменения расстановки ТПК</h2></div>
<table class="fill" data-rh="8"><tr><th style="width:18mm">Дата</th><th style="width:16mm">№ ТПК</th><th>Изменение (установлена, перенесена, снята) и причина</th><th style="width:24mm" class="c">План-схема обновлена</th><th style="width:22mm" class="c">Подпись</th></tr>{chg}</table>
{footer(3, 10)}</section>"""


def p_agents_log(sample):
    head = '<tr><th style="width:7mm" class="c">№</th><th style="width:52mm">Наименование, препаративная форма</th><th style="width:26mm">Действующее вещество</th><th style="width:38mm">СГР / декларация, срок годности</th><th>Где и как применяется, ограничения</th></tr>'
    body = ''
    if sample:
        for i, (n, dv, use) in enumerate(AGENTS, 1):
            sgr = SGR_MASK if dv not in ('—',) else 'декларация / сертификат (прил.\u00a04)'
            body += f'<tr><td class="c">{i}</td><td class="ink">{n}</td><td class="ink">{dv}</td><td class="ink" style="font-size:6.6pt">{sgr}</td><td>{use}</td></tr>'
    else:
        body = ''.join(f'<tr class="rowh"><td class="c">{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 9))
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    note = ('<p class="note"><b>В образце</b> номера свидетельств о государственной регистрации скрыты. В рабочем журнале указывают торговое наименование и полный номер СГР по реестру ЕАЭС; копии свидетельств и инструкций лежат в папке объекта (прил.\u00a04).</p>'
            if sample else '<p class="note">Указывают торговое наименование, действующее вещество и концентрацию, полный номер СГР по реестру ЕАЭС, срок годности партии. Копии свидетельств и инструкций — в папке объекта.</p>')
    return f"""<section class="pg">{wm}{header_small(sample, '3', 10)}
{sec('3', 'Перечень применяемых средств и материалов', 'Согласуется с Заказчиком до начала работ. Средство вне перечня на объекте не применяется.')}
<table>{head}{body}</table>
{note}
<div class="sec"><span class="n">3.1</span><h2>Согласование перечня</h2></div>
<div class="grid2"><div class="box" style="font-size:7.5pt">Исполнитель: инженер пест-менеджер<br><br>{('<span class="ink">Смирнов А. Н.</span> ' + sig('smirnov') + ' <span class="ink">02.09.2026</span>') if sample else '_______________ / _______________ / ____.____.20___'}</div>
<div class="box" style="font-size:7.5pt">Заказчик: ответственный за пест-контроль<br><br>{('<span class="ink">Иванова Е. В.</span> ' + sig('ivanova') + ' <span class="ink">02.09.2026</span>') if sample else '_______________ / _______________ / ____.____.20___'}</div></div>
<div class="sec"><span class="n">3.2</span><h2>Изменения перечня средств</h2></div>
<table class="fill" data-rh="9"><tr><th style="width:20mm">Дата</th><th>Что изменено (добавлено, исключено, замена партии)</th><th style="width:40mm">Основание</th><th style="width:24mm" class="c">Исполнитель</th><th style="width:24mm" class="c">Заказчик</th></tr><tr class="rowh"><td></td><td></td><td></td><td></td><td></td></tr></table>
{footer(4, 10)}</section>"""


def p_log(sample):
    head = ('<tr><th style="width:17.5mm">Дата</th><th style="width:13mm">Время</th><th style="width:22mm">Вид визита</th><th>Выполненные работы, результаты</th>'
            '<th style="width:31mm">Средства (№ по разд. 3) и расход</th><th style="width:14mm" class="c">№ акта</th><th style="width:19mm" class="c">Специалист</th><th style="width:19mm" class="c">Заказчик</th></tr>')
    body = ''
    if sample:
        for d, t, k, w, a, act, who in LOG:
            body += (f'<tr><td class="ink" style="white-space:nowrap">{d}</td><td class="ink">{t}</td><td class="ink">{k}</td><td class="ink">{w}</td><td class="ink">{a}</td>'
                     f'<td class="c ink">{act}</td><td class="c">{sig(who, 38)}</td><td class="c">{sig("ivanova", 38)}</td></tr>')
        body += '<tr class="rowh"><td class="ink" style="height:11mm;white-space:nowrap">11.11.2026</td><td></td><td class="ink">Плановый</td><td></td><td></td><td></td><td></td><td></td></tr>'
    else:
        body = '<tr class="rowh" style="height:13mm"><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 14
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '4', 10)}
{sec('4', 'Ведомость визитов и расхода средств', 'Одна строка — один выезд. Номер акта выполненных работ совпадает с актом в бухгалтерии и ЭДО.')}
<table class="fill" data-rh="11">{head}{body}</table>
{footer(5, 10)}</section>"""


def p_matrix(sample):
    nv = 8
    dates = VISITS if sample else [''] * nv
    kinds = VKIND if sample else [''] * nv
    th = ''.join(f'<th class="c" style="width:15.5mm">{("<span class=ink>" + d + "</span>") if d else "____.____"}<br><span style="font-weight:400">{("<span class=ink>" + k + "</span>") if k else "план / внепл."}</span></th>' for d, k in zip(dates, kinds))
    head = f'<tr><th style="width:14mm">№ ТПК</th><th style="width:60mm">Место установки</th>{th}<th>Примечание</th></tr>'
    body = ''
    cur = None
    notes = {'КИК-05': 'норы у отмостки — пр. 4', 'МЛ-04': 'доступ восстановлен 30.09', 'МЛ-10': 'мышь домовая — пр. 7', 'ИМ-03': 'Blattella germanica — пр. 6', 'ФЛ-01': 'огнёвка — пр. 3', 'КИК-03': 'площадка ТКО — пр. 8'}
    if not sample:
        body = '<tr><td style="height:4.2mm"></td><td></td>' + '<td></td>' * nv + '<td></td></tr>'
        body = body * 30
    for code, typ, ct, place, thr in (POINTS if sample else []):
        if ct != cur:
            cur = ct
            body += f'<tr class="zone"><td colspan="{nv + 3}">{CONTOUR[ct]}</td></tr>'
        if sample:
            cells = ''
            for vi in range(nv):
                v = cell(vi, code)
                cls = 'v'
                if v == '—':
                    cls += ' na'
                cls += {(1, 'КИК-03'): ' hl', (2, 'КИК-05'): ' cr', (2, 'МЛ-04'): ' hl', (1, 'ФЛ-01'): ' hl', (3, 'ИМ-03'): ' cr', (4, 'МЛ-10'): ' cr'}.get((vi, code), '')
                cells += f'<td class="{cls}">{v}</td>'
            body += f'<tr><td class="ink">{code}</td><td>{place}</td>{cells}<td class="ink" style="font-size:6.2pt">{notes.get(code, "")}</td></tr>'
        else:
            body += f'<tr><td>{code}</td><td>{place}</td>' + '<td></td>' * nv + '<td></td></tr>'
    if sample:
        s1 = ''.join(f'<td class="c">{sig("orlov" if i == 4 else "smirnov", 30) if i < 6 else ""}</td>' for i in range(nv))
        s2 = ''.join(f'<td class="c">{sig("ivanova", 30) if i < 6 else ""}</td>' for i in range(nv))
    else:
        s1 = s2 = '<td></td>' * nv
    body += f'<tr><td colspan="2"><b>Подпись специалиста Исполнителя</b></td>{s1}<td></td></tr>'
    body += f'<tr><td colspan="2"><b>Подпись представителя Заказчика</b></td>{s2}<td></td></tr>'
    if not sample:
        # бланк: ТПК пустые, места не заполнены
        body = body
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    legend = ''.join(f'<span><b>{c}</b>{t}</span>' for c, t in [
        ('0', 'осмотрена, находок нет, исправна'), ('П%', 'поедаемость приманки, %'), ('М / К', 'отлов: мышь / крыса, особей'),
        ('С', 'следы (помёт, погрызы)'), ('Н', 'насекомые на клеевой поверхности, особей'), ('З', 'замена приманки / пластины'),
        ('Д', 'нет доступа → разд. 7'), ('Р', 'повреждена, заменена'), ('У', 'установлена'), ('—', 'вне объёма внепланового визита')])
    return f"""<section class="pg land">{wm}{header_small(sample, '5', 10)}
{sec('5', 'Поточечный лист осмотра точек пест-контроля', 'Отметка ставится по каждой ТПК на каждом визите. Через «/» — выполненное действие. Жёлтым — достигнут порог, красным — превышение или отлов внутри здания.')}
<table class="mx">{head}{body}</table>
<div class="legend">{legend}</div>
{footer(6, 10)}</section>"""


def bar_chart():
    data = [('16.09', 28), ('30.09', 20), ('14.10', 13), ('28.10', 7)]
    w, h, pad = 220, 96, 18
    bw = 30
    gap = (w - pad * 2 - bw * len(data)) / (len(data) - 1)
    mx = 30
    bars = ''
    for i, (d, v) in enumerate(data):
        x = pad + i * (bw + gap)
        bh = (h - 30) * v / mx
        y = h - 16 - bh
        bars += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" rx="2" fill="#615fff"/>'
        bars += f'<text x="{x + bw / 2:.1f}" y="{y - 3:.1f}" text-anchor="middle" font-size="8" font-weight="600" fill="#18181b">{v}</text>'
        bars += f'<text x="{x + bw / 2:.1f}" y="{h - 5}" text-anchor="middle" font-size="7.5" fill="#52525b">{d}</text>'
    return (f'<svg viewBox="0 0 {w} {h}" width="64mm" height="{64 * h / w:.1f}mm" font-family="Inter">'
            f'<line x1="{pad - 4}" y1="{h - 16}" x2="{w - pad + 4}" y2="{h - 16}" stroke="#a1a1aa" stroke-width=".6"/>{bars}</svg>')


def p_insects(sample):
    head = ('<tr><th style="width:13mm">Дата</th><th style="width:18mm">ТПК</th><th>Вид (группа), стадия, число особей</th><th style="width:12mm" class="c">Всего</th>'
            '<th style="width:20mm" class="c">Оценка к порогу</th><th style="width:50mm">Принятые меры</th></tr>')
    body = ''
    if sample:
        for d, t, sp, n, ev, act in INSECTS:
            col = {'превышение': 'background:#ffe1e1', 'на пороге': 'background:#fff4c2'}.get(ev, '')
            body += f'<tr><td class="ink">{d}</td><td class="ink">{t}</td><td class="ink">{sp}</td><td class="c ink">{n}</td><td class="c ink" style="{col}">{ev}</td><td class="ink">{act}</td></tr>'
        body += '<tr class="rowh"><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 4
        chart = f"""<div class="chart"><div class="box"><h3>Вывод специалиста по динамике</h3><div class="ink" style="font-size:7.6pt;line-height:1.5">Отлов летающих насекомых снижается от визита к визиту (28 → 7) — сезонное снижение и замена уплотнителя ворот дока №\u00a01. Пищевые огнёвки после уборки просыпей не выявляются с 14.10. Очаг рыжего таракана в моечной ликвидирован: на контроле 28.10 — 0. Рекомендация: сохранить кратность 2 раза в месяц, ИМ-03 оставить в зоне особого внимания.</div><div style="margin-top:2mm;font-size:7.2pt">Инженер пест-менеджер <span class="ink">Смирнов А. Н.</span> {sig('smirnov')}</div></div>
<div class="box"><h3>ИЛ-01…04: особей за визит</h3>{bar_chart()}</div></div>"""
    else:
        body = '<tr class="rowh" style="height:9mm"><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 16
        chart = '<div class="box" style="margin-top:3mm"><h3>Вывод специалиста по динамике</h3><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>'
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '6', 10)}
{sec('6', 'Учёт насекомых по видам и динамика', 'Расшифровка находок с клеевых мониторов, световых и феромонных ловушек. Вид определяет специалист Исполнителя (СанПиН 3.3686-21, п. 99).')}
<table class="fill" data-rh="8">{head}{body}</table>
{chart}
{footer(7, 10)}</section>"""


def p_actions(sample):
    head = ('<tr><th style="width:7mm" class="c">№</th><th style="width:12mm">Дата</th><th style="width:14mm">ТПК / зона</th><th>Выявлено (причина риска)</th><th style="width:38mm">Рекомендация Исполнителя</th>'
            '<th style="width:24mm">Ответственный, срок</th><th style="width:24mm">Отметка Заказчика о выполнении</th><th style="width:16mm" class="c">Проверено Исполнителем</th></tr>')
    body = ''
    if sample:
        for n, d, tpk, found, rec, resp, done, chk, who in ACTIONS:
            st = '' if done != 'В работе' else 'background:#fff4c2'
            s = sig(who, 30) if who else ''
            body += (f'<tr><td class="c">{n}</td><td class="ink">{d}</td><td class="ink">{tpk}</td><td class="ink">{found}</td><td class="ink">{rec}</td>'
                     f'<td class="ink">{resp}</td><td class="ink" style="{st}">{done} {s}</td><td class="c ink">{chk}{(" " + sig("smirnov", 26)) if chk else ""}</td></tr>')
        body += ''.join(f'<tr class="rowh" style="height:11mm"><td class="c">{i}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(9, 13))
    else:
        body = ''.join(f'<tr class="rowh" style="height:16mm"><td class="c">{i}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 14))
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '7', 10)}
{sec('7', 'Замечания, предписания и корректирующие действия', 'Санитарно-технические причины находок: щели, уплотнители, сетки, просыпи, влага, захламлённость. Запись закрывается только после проверки Исполнителем на объекте.')}
<table class="fill" data-rh="12" data-num="1">{head}{body}</table>
{footer(8, 10)}</section>"""


def p_signals(sample):
    head = ('<tr><th style="width:7mm" class="c">№</th><th style="width:20mm">Дата, время</th><th style="width:25mm">Место</th><th>Что обнаружено</th><th style="width:28mm">Кто сообщил (ФИО, должность), подпись</th>'
            '<th style="width:26mm">Кому передано, когда</th><th style="width:34mm">Отметка Исполнителя</th></tr>')
    body = ''
    if sample:
        for n, dt, pl, what, who, to, mark, s1, s2 in SIGNALS:
            body += (f'<tr><td class="c">{n}</td><td class="ink">{dt}</td><td class="ink">{pl}</td><td class="ink">{what}</td><td class="ink">{who} {sig(s1, 28)}</td>'
                     f'<td class="ink">{to}</td><td class="ink">{mark} {sig(s2, 26)}</td></tr>')
        body += ''.join(f'<tr class="rowh" style="height:10mm"><td class="c">{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(3, 9))
    else:
        body = ''.join(f'<tr class="rowh" style="height:11.5mm"><td class="c">{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 11))
    bh = ('<tr><th style="width:20mm">Дата</th><th>Кто проинструктирован</th><th style="width:58mm">Тема</th><th style="width:26mm">Провёл</th><th style="width:20mm" class="c">Подпись</th></tr>')
    bb = ''
    if sample:
        for d, w, t, by, s in BRIEF:
            bb += f'<tr><td class="ink">{d}</td><td class="ink">{w}</td><td class="ink">{t}</td><td class="ink">{by}</td><td class="c">{sig(s, 30)}</td></tr>'
        bb += '<tr class="rowh" style="height:9mm"><td></td><td></td><td></td><td></td><td></td></tr>' * 2
    else:
        bb = '<tr class="rowh" style="height:10mm"><td></td><td></td><td></td><td></td><td></td></tr>' * 4
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '8', 10)}
{sec('8', 'Сигнальный лист персонала объекта', 'Заполняют сотрудники Заказчика, если между визитами увидели грызуна, насекомое или следы. Сразу сообщить ответственному; срочная заявка Исполнителю — ' + CO['phone'] + '.')}
<table>{head}{body}</table>
<div class="sec"><span class="n">8.1</span><h2>Инструктажи персонала по пест-контролю</h2></div>
<table class="fill" data-rh="9">{bh}{bb}</table>
{footer(9, 10)}</section>"""


def p_summary(sample):
    head = ('<tr><th style="width:20mm">Месяц</th><th style="width:15mm" class="c">Визиты план / внепл.</th><th style="width:13mm" class="c">Осмотров ТПК</th><th>Грызуны</th><th style="width:38mm">Насекомые</th>'
            '<th style="width:16mm" class="c">Предписания выдано / закрыто</th><th style="width:26mm">Оценка риска, тенденция</th></tr>')
    body = ''
    if sample:
        for m in MONTHS:
            body += '<tr>' + ''.join(f'<td class="{"c " if i in (1, 2, 5) else ""}ink">{x}</td>' for i, x in enumerate(m)) + '</tr>'
        body += '<tr class="rowh" style="height:11mm"><td class="ink">Ноябрь 2026</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
        body += '<tr class="rowh" style="height:11mm"><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
    else:
        body = '<tr class="rowh" style="height:13mm"><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 6
    if sample:
        cert_txt = 'В настоящем журнале пронумеровано, прошнуровано и скреплено печатью <span class="ink">10 (десять)</span> листов.'
        sigs = (f'<div>Исполнитель: инженер пест-менеджер<br><span class="ink">Смирнов А. Н.</span> {sig("smirnov")} <span class="ink">02.09.2026</span><br><br><span class="stamp">М. П.</span></div>'
                f'<div>Заказчик: ответственный за пест-контроль<br><span class="ink">Иванова Е. В.</span> {sig("ivanova")} <span class="ink">02.09.2026</span><br><br><span class="stamp">М. П.</span></div>')
    else:
        cert_txt = 'В настоящем журнале пронумеровано, прошнуровано и скреплено печатью ______ (______________) листов.'
        sigs = ('<div>Исполнитель: _____________________<br><br>_______________ / _______________ / ____.____.20___<br><br><span class="stamp">М. П.</span></div>'
                '<div>Заказчик: _____________________<br><br>_______________ / _______________ / ____.____.20___<br><br><span class="stamp">М. П.</span></div>')
    wm = '<div class="wm">ОБРАЗЕЦ</div>' if sample else ''
    return f"""<section class="pg">{wm}{header_small(sample, '9', 10)}
{sec('9', 'Ежемесячная сводка и анализ тенденций', 'Заполняет Исполнитель по итогам месяца. Подробный отчёт с графиками по зонам передаётся службе качества и хранится вместе с журналом.')}
<table class="fill" data-rh="12">{head}{body}</table>
<div class="cert"><h3>Заверительная надпись</h3><div style="font-size:8pt">{cert_txt}</div><div class="row">{sigs}</div></div>
<p class="note" style="margin-top:4mm">Журнал сформирован по форме {CO['brand']} для объектов пищевой промышленности, общественного питания, торговли и хранения пищевой продукции. Форма не является утверждённой государственной: СанПиН 3.3686-21 не устанавливает единого бланка, но требует учёта численности вредителей, контроля эффективности и производственного контроля за дезинфекционными мероприятиями.</p>
{footer(10, 10)}</section>"""


def build(sample):
    title = ('Образец заполнения журнала пест-контроля' if sample else 'Бланк журнала пест-контроля') + ' — ПЕСТКОНТРОЛЬ Центр'
    pages = [p_title(sample), p_passport(sample), p_registry(sample), p_agents_log(sample), p_log(sample), p_matrix(sample),
             p_insects(sample), p_actions(sample), p_signals(sample), p_summary(sample)]
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{css()}</style></head><body>{"".join(pages)}</body></html>'


(OUT / 'sample.html').write_text(build(True), encoding='utf-8')
(OUT / 'blank.html').write_text(build(False), encoding='utf-8')
print('ok', OUT)
