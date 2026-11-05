#!/usr/bin/env python3
"""Редактируемый шаблон журнала пест-контроля (Word) в фирменном стиле ПЕСТКОНТРОЛЬ Центр.
python3 build_docx.py <logo.png> <out.docx>
После сборки обязательно: asi-validate --repair <out.docx> (порядок элементов rPr/pPr по схеме Word)."""
import sys
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

LOGO, OUT = sys.argv[1], sys.argv[2]
INDIGO = RGBColor(0x61, 0x5F, 0xFF)
GRAY = RGBColor(0x71, 0x71, 0x7A)
DARK = RGBColor(0x18, 0x18, 0x1B)
FONT = 'Arial'

CO_LINE1 = 'ПЕСТКОНТРОЛЬ Центр · ООО «Центр дезинфекционных услуг» · ИНН 7714462211 · КПП 771401001 · ОГРН 1207700257775'
CO_LINE2 = 'Лицензия Роспотребнадзора № Л064-00111-77/01942445 · 123007, г. Москва, 2-й Хорошёвский проезд, д. 7, к. 1, помещ. 1'
CO_LINE3 = '+7 (495) 104-35-70 · b2b@pestcontrol-center.ru · пестконтроль-центр.рф'

doc = Document()
st = doc.styles['Normal']
st.font.name = FONT
st.font.size = Pt(9)
st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.line_spacing = 1.1
doc.core_properties.title = 'Шаблон журнала пест-контроля — ПЕСТКОНТРОЛЬ Центр'
doc.core_properties.author = 'ПЕСТКОНТРОЛЬ Центр'
doc.core_properties.subject = 'Форма объектового журнала пест-контроля (дератизация, дезинсекция, мониторинг) для заполнения'


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)


def borders(table, color='A1A1AA', sz=4):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement(f'w:{e}')
        el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), str(sz)); el.set(qn('w:space'), '0'); el.set(qn('w:color'), color)
        b.append(el)
    nxt = None
    for tag in ('shd', 'tblLayout', 'tblCellMar', 'tblLook', 'tblCaption', 'tblDescription'):
        nxt = tblPr.find(qn('w:' + tag))
        if nxt is not None:
            break
    if nxt is not None:
        nxt.addprevious(b)
    else:
        tblPr.append(b)


def row_height(row, mm):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement('w:trHeight'); h.set(qn('w:val'), str(int(mm * 56.7))); h.set(qn('w:hRule'), 'atLeast')
    trPr.append(h)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement('w:tblHeader'); el.set(qn('w:val'), 'true'); trPr.append(el)


def run(p, text, size=None, bold=False, color=None, italic=False, spacing=None):
    r = p.add_run(text)
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    if size: r.font.size = Pt(size)
    r.bold = bold; r.italic = italic
    if color is not None: r.font.color.rgb = color
    if spacing is not None:
        rPr = r._element.get_or_add_rPr(); sp = OxmlElement('w:spacing'); sp.set(qn('w:val'), str(spacing)); rPr.append(sp)
    return r


def bottom_rule(p, color='615FFF', sz=12):
    pPr = p._p.get_or_add_pPr()
    pb = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), str(sz)); bt.set(qn('w:space'), '4'); bt.set(qn('w:color'), color)
    pb.append(bt); pPr.append(pb)


def setup_section(sec, landscape=False):
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Mm(297), Mm(210)
        sec.left_margin, sec.right_margin, sec.top_margin, sec.bottom_margin = Mm(16), Mm(12), Mm(10), Mm(10)
    else:
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        sec.left_margin, sec.right_margin, sec.top_margin, sec.bottom_margin = Mm(20), Mm(12), Mm(10), Mm(10)
    sec.header_distance = Mm(6); sec.footer_distance = Mm(6)
    sec.header.is_linked_to_previous = False
    sec.footer.is_linked_to_previous = False
    hd = sec.header
    for p in hd.paragraphs:
        p.text = ''
    width = sec.page_width - sec.left_margin - sec.right_margin
    t = hd.add_table(rows=1, cols=3, width=width)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cl, c0, c1 = t.rows[0].cells
    wl = Mm(14)
    t.columns[0].width = cl.width = wl
    t.columns[1].width = c0.width = int((width - wl) * 0.66)
    t.columns[2].width = c1.width = int((width - wl) * 0.34)
    cl.paragraphs[0].add_run().add_picture(LOGO, width=Mm(8.5))
    cl.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c0.paragraphs[0]
    run(p, 'ПЕСТКОНТРОЛЬ', 11, True, DARK)
    run(p, ' ЦЕНТР', 7, True, INDIGO, spacing=30)
    p2 = c0.add_paragraph(); run(p2, 'Журнал пест-контроля № __________ · Объект: ______________________________', 7, color=GRAY)
    q = c1.paragraphs[0]; q.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(q, 'ФОРМА · ШАБЛОН', 7, True, INDIGO, spacing=20)
    q2 = c1.add_paragraph(); q2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(q2, '+7 (495) 104-35-70 · пестконтроль-центр.рф', 7, color=GRAY)
    c0.vertical_alignment = c1.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    rule = hd.add_paragraph(); bottom_rule(rule); rule.paragraph_format.space_after = Pt(0)
    ft = sec.footer
    fp = ft.paragraphs[0]; fp.text = ''
    top = OxmlElement('w:pBdr'); tb = OxmlElement('w:top'); tb.set(qn('w:val'), 'single'); tb.set(qn('w:sz'), '4'); tb.set(qn('w:space'), '4'); tb.set(qn('w:color'), 'D4D4D8'); top.append(tb); fp._p.get_or_add_pPr().append(top)
    run(fp, CO_LINE1 + '\n' + CO_LINE2 + '\n' + CO_LINE3, 6.5, color=GRAY)
    fp2 = ft.add_paragraph(); fp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(fp2, 'Лист ', 7, True, DARK)
    for code in ('PAGE',):
        r = fp2.add_run(); r.font.size = Pt(7); r.bold = True
        f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = code
        f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
        r._r.append(f1); r._r.append(it); r._r.append(f2)


def h(num, title, lead=None):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    run(p, f' {num} ', 9, True, RGBColor(0xFF, 0xFF, 0xFF))
    rPr = p.runs[-1]._element.get_or_add_rPr(); hl = OxmlElement('w:shd'); hl.set(qn('w:val'), 'clear'); hl.set(qn('w:fill'), '615FFF'); rPr.append(hl)
    run(p, '  ' + title, 12, True, DARK)
    if lead:
        q = doc.add_paragraph(); run(q, lead, 7.5, color=GRAY); q.paragraph_format.space_after = Pt(4)


def table(headers, widths_mm, rows, rh=7.5, numbered=False, first_col=None):
    t = doc.add_table(rows=1 + rows, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    borders(t)
    for i, hd in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ''
        run(c.paragraphs[0], hd, 7, True, DARK)
        shade(c, 'ECEEFF'); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    repeat_header(t.rows[0])
    for i, col in enumerate(t.columns):
        col.width = Mm(widths_mm[i])
    for r_i, row in enumerate(t.rows):
        for i, c in enumerate(row.cells):
            c.width = Mm(widths_mm[i])
        if r_i:
            row_height(row, rh)
            if numbered:
                run(row.cells[0].paragraphs[0], str(r_i), 7.5)
            if first_col and r_i - 1 < len(first_col):
                run(row.cells[0].paragraphs[0], first_col[r_i - 1], 7.5)
    return t


def kv(labels, w1=48, w2=130, rh=7):
    t = doc.add_table(rows=len(labels), cols=2)
    t.autofit = False
    t.columns[0].width, t.columns[1].width = Mm(w1), Mm(w2)
    for i, lab in enumerate(labels):
        c0, c1 = t.rows[i].cells
        c0.width, c1.width = Mm(w1), Mm(w2)
        run(c0.paragraphs[0], lab, 8, color=GRAY)
        row_height(t.rows[i], rh)
        tcPr = c1._tc.get_or_add_tcPr(); b = OxmlElement('w:tcBorders'); bt = OxmlElement('w:bottom')
        bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '4'); bt.set(qn('w:color'), 'A1A1AA'); b.append(bt); tcPr.append(b)
    return t


def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ----------------------------------------------------------------- титул
setup_section(doc.sections[0])
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(26)
run(p, 'ОБЪЕКТОВЫЙ ЖУРНАЛ · IPM / ХАССП', 8, True, INDIGO, spacing=40)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4); p.paragraph_format.line_spacing = 0.95
run(p, 'ЖУРНАЛ\nПЕСТ-КОНТРОЛЯ', 32, True, DARK)
p = doc.add_paragraph(); run(p, 'учёта мониторинга вредителей, дератизации и дезинсекции на объекте', 12, color=RGBColor(0x3F, 0x3F, 0x46))
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(10)
run(p, 'Журнал № ____________', 13, True, DARK)
kv(['Объект (наименование)', 'Адрес объекта', 'Заказчик', 'Договор на пест-контроль', 'Ответственный от Заказчика', 'Ответственный специалист Исполнителя',
    'Журнал начат', 'Журнал окончен', 'Листов в журнале'], rh=8.5)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
run(p, 'ИСПОЛНИТЕЛЬ', 8, True, INDIGO, spacing=30)
p = doc.add_paragraph()
run(p, 'ПЕСТКОНТРОЛЬ Центр', 9, True)
run(p, ' — ООО «Центр дезинфекционных услуг»\nИНН 7714462211 · КПП 771401001 · ОГРН 1207700257775\n123007, г. Москва, 2-й Хорошёвский проезд, д. 7, к. 1, помещ. 1\n'
       'Лицензия на дезинфекционную деятельность (Роспотребнадзор) № Л064-00111-77/01942445\n+7 (495) 104-35-70 · b2b@pestcontrol-center.ru · пестконтроль-центр.рф\nПн–Пт 8:00–20:00 · срочные выезды 24/7', 8.5)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
run(p, 'СОСТАВ ЖУРНАЛА', 8, True, INDIGO, spacing=30)
for n, t_ in [('1', 'Паспорт объекта, порядок ведения, график визитов'), ('2', 'Реестр точек пест-контроля (ТПК)'), ('3', 'Перечень применяемых средств и материалов'),
              ('4', 'Ведомость визитов и расхода средств'), ('5', 'Поточечный лист осмотра ТПК'), ('6', 'Учёт насекомых по видам и динамика'),
              ('7', 'Замечания, предписания и корректирующие действия'), ('8', 'Сигнальный лист персонала · инструктажи'), ('9', 'Ежемесячная сводка · заверительная надпись')]:
    q = doc.add_paragraph(); q.paragraph_format.space_after = Pt(0); run(q, f'{n}   ', 8.5, True, INDIGO); run(q, t_, 8.5)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(12)
run(p, 'Журнал хранится на объекте у ответственного за пест-контроль и предъявляется при проверках Роспотребнадзора, аудитах ХАССП, ISO 22000 / FSSC 22000 и торговых сетей. '
       'Основание ведения: СанПиН 3.3686-21 (раздел III, пп. 82, 98–124), МР 3.5.3.0374-25, ТР ТС 021/2011 (ст. 10), ГОСТ Р 54762-2011 (раздел 12), программа пест-контроля объекта.', 7, color=GRAY)
page_break()

# ----------------------------------------------------------------- 1
h('1', 'Паспорт объекта', 'Заполняется при заведении журнала и обновляется при перепланировке, смене зон хранения или ответственных лиц.')
kv(['Вид деятельности', 'Площадь здания / территории', 'Режим работы', 'Зоны (контуры защиты)', 'Целевые вредители', 'Кратность визитов', 'Метод', 'Прилагается к журналу'])
h('1.1', 'Контакты и порядок связи')
kv(['Ответственный Заказчика', 'Замещающее лицо', 'Специалист Исполнителя', 'Срочная заявка: +7 (495) 104-35-70'])
h('1.2', 'Порядок ведения журнала')
for i, r_ in enumerate([
    'Записи вносит специалист Исполнителя в день визита, до ухода с объекта. Представитель Заказчика подтверждает визит подписью в разделах 4 и 5.',
    'Каждая ТПК записывается отдельно под своим номером с план-схемы. Пустые клетки не допускаются: при отсутствии находок ставится «0», при отсутствии доступа — «Д» с записью в раздел 7.',
    'Для каждого применённого средства указываются номер по перечню (раздел 3), место применения и расход. Родентициды в помещениях с открытой пищевой продукцией не применяются.',
    'Исправления: зачеркнуть одной линией, рядом — верная запись, дата, подпись. Подчистки, корректор и вклейка листов не допускаются.',
    'Персонал объекта записывает наблюдения вредителей между визитами в сигнальный лист (раздел 8) и сообщает ответственному.',
    'Ежемесячно специалист Исполнителя заполняет сводку (раздел 9) и передаёт отчёт с анализом тенденций службе качества.'], 1):
    q = doc.add_paragraph(); q.paragraph_format.space_after = Pt(1); run(q, f'{i}. ', 8, True, INDIGO); run(q, r_, 8)
h('1.3', 'График плановых визитов')
table(['Месяц', 'Плановые даты', 'Фактические даты, отклонения', 'Подпись Заказчика'], [28, 44, 76, 30], 6)
page_break()

# ----------------------------------------------------------------- 2
h('2', 'Реестр точек пест-контроля (ТПК)', 'Номера совпадают с план-схемой и настенными указателями. Порог — уровень, при котором назначаются корректирующие действия (по программе пест-контроля).')
table(['№ ТПК', 'Тип устройства', 'Контур', 'Место установки (по план-схеме)', 'Установлена', 'Порог'], [15, 42, 24, 60, 17, 20], 22, rh=6.6)
q = doc.add_paragraph(); run(q, 'Обозначения: КИК — станция контроля грызунов с приманкой; МЛ — механическая или клеевая ловушка; ИМ — клеевой монитор насекомых; ИЛ — световая ловушка; ФЛ — феромонная ловушка.', 7, color=GRAY)
h('2.1', 'Изменения расстановки ТПК')
table(['Дата', '№ ТПК', 'Изменение (установлена, перенесена, снята) и причина', 'План-схема обновлена', 'Подпись'], [18, 16, 98, 24, 22], 6)
page_break()

# ----------------------------------------------------------------- 3
h('3', 'Перечень применяемых средств и материалов', 'Согласуется с Заказчиком до начала работ. Средство вне перечня на объекте не применяется.')
table(['№', 'Наименование, препаративная форма', 'Действующее вещество', 'СГР / декларация, срок годности', 'Где и как применяется, ограничения'], [8, 50, 28, 38, 54], 8, rh=11, numbered=True)
h('3.1', 'Согласование перечня')
q = doc.add_paragraph(); run(q, 'Исполнитель: _______________ / _______________ / ____.____.20___\t\tЗаказчик: _______________ / _______________ / ____.____.20___', 8)
h('3.2', 'Изменения перечня средств')
table(['Дата', 'Что изменено (добавлено, исключено, замена партии)', 'Основание', 'Исполнитель', 'Заказчик'], [20, 70, 40, 24, 24], 8, rh=9)
page_break()

# ----------------------------------------------------------------- 4
h('4', 'Ведомость визитов и расхода средств', 'Одна строка — один выезд. Номер акта выполненных работ совпадает с актом в бухгалтерии и ЭДО.')
table(['Дата', 'Время', 'Вид визита', 'Выполненные работы, результаты', 'Средства (№ по разд. 3) и расход', '№ акта', 'Специалист', 'Заказчик'], [17, 14, 22, 50, 31, 14, 15, 15], 16, rh=12)

# ----------------------------------------------------------------- 5 (landscape)
s5 = doc.add_section()
setup_section(s5, landscape=True)
h('5', 'Поточечный лист осмотра точек пест-контроля', 'Отметка ставится по каждой ТПК на каждом визите. Через «/» — выполненное действие.')
t = table(['№ ТПК', 'Место установки'] + ['Дата\n__.__'] * 8 + ['Примечание'], [15, 58] + [16.5] * 8 + [64], 22, rh=4.4)
for lab in ('Подпись специалиста Исполнителя', 'Подпись представителя Заказчика'):
    r_ = t.add_row(); row_height(r_, 6)
    m = r_.cells[0].merge(r_.cells[1]); m.text = ''; run(m.paragraphs[0], lab, 7, True)
q = doc.add_paragraph(); q.paragraph_format.space_before = Pt(3)
run(q, 'Коды: 0 — осмотрена, находок нет; П% — поедаемость приманки; М / К — отлов мыши / крысы; С — следы; Н — насекомые, особей; З — замена приманки / пластины; Д — нет доступа → разд. 7; Р — повреждена, заменена; У — установлена; «—» — вне объёма визита.', 7, color=GRAY)

# ----------------------------------------------------------------- 6..9 (portrait)
s6 = doc.add_section()
setup_section(s6)
h('6', 'Учёт насекомых по видам и динамика', 'Расшифровка находок с клеевых мониторов, световых и феромонных ловушек. Вид определяет специалист Исполнителя (СанПиН 3.3686-21, п. 99).')
table(['Дата', 'ТПК', 'Вид (группа), стадия, число особей', 'Всего', 'Оценка к порогу', 'Принятые меры'], [14, 18, 64, 12, 20, 50], 18, rh=8)
h('6.1', 'Вывод специалиста по динамике')
for _ in range(4):
    q = doc.add_paragraph('_' * 110); q.paragraph_format.space_after = Pt(3)
page_break()
h('7', 'Замечания, предписания и корректирующие действия', 'Санитарно-технические причины находок: щели, уплотнители, сетки, просыпи, влага, захламлённость. Запись закрывается после проверки Исполнителем.')
table(['№', 'Дата', 'ТПК / зона', 'Выявлено (причина риска)', 'Рекомендация Исполнителя', 'Ответственный, срок', 'Отметка Заказчика о выполнении', 'Проверено Исполнителем'], [8, 13, 15, 40, 38, 24, 24, 16], 13, rh=14, numbered=True)
page_break()
h('8', 'Сигнальный лист персонала объекта', 'Заполняют сотрудники Заказчика, если между визитами увидели грызуна, насекомое или следы. Срочная заявка Исполнителю — +7 (495) 104-35-70.')
table(['№', 'Дата, время', 'Место', 'Что обнаружено', 'Кто сообщил (ФИО, должность), подпись', 'Кому передано, когда', 'Отметка Исполнителя'], [8, 20, 25, 35, 30, 26, 34], 9, rh=11, numbered=True)
h('8.1', 'Инструктажи персонала по пест-контролю')
table(['Дата', 'Кто проинструктирован', 'Тема', 'Провёл', 'Подпись'], [20, 52, 56, 30, 20], 6, rh=9)
page_break()
h('9', 'Ежемесячная сводка и анализ тенденций', 'Заполняет Исполнитель по итогам месяца. Подробный отчёт с графиками по зонам передаётся службе качества.')
table(['Месяц', 'Визиты план / внепл.', 'Осмотров ТПК', 'Грызуны', 'Насекомые', 'Предписания выдано / закрыто', 'Оценка риска, тенденция'], [22, 16, 14, 42, 38, 18, 28], 9, rh=12)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
run(p, 'ЗАВЕРИТЕЛЬНАЯ НАДПИСЬ', 9, True, DARK, spacing=30)
p = doc.add_paragraph(); run(p, 'В настоящем журнале пронумеровано, прошнуровано и скреплено печатью ______ (______________) листов.', 9)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
run(p, 'Исполнитель: _______________ / _______________ / ____.____.20___        М. П.\n\nЗаказчик: _______________ / _______________ / ____.____.20___        М. П.', 9)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(12)
run(p, 'Форма ПЕСТКОНТРОЛЬ Центр для объектов пищевой промышленности, общественного питания, торговли и хранения пищевой продукции. Форма не является утверждённой государственной: '
       'СанПиН 3.3686-21 не устанавливает единого бланка журнала, но требует учёта численности вредителей, контроля эффективности и производственного контроля за дезинфекционными мероприятиями. '
       'Пример заполнения: пестконтроль-центр.рф/materialy/zhurnal-pest-kontrolya/', 7, color=GRAY)

doc.save(OUT)
print('saved', OUT)
