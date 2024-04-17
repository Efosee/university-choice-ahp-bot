from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, CallbackData, InlineKeyboardMarkup

class AddingList(CallbackData, prefix="vuz"): #При использовании фабрики колбеков обязаельнов в хандлере поставить фильр AddingList.filters()
    action: str


def inline_vuz(name="ВУЗ"):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=f"Добавить {name}", callback_data=AddingList(action="add").pack()),
        InlineKeyboardButton(text="Далее", callback_data=AddingList(action="next").pack()),
        InlineKeyboardButton(text="Отмена ввода", callback_data=AddingList(action="cancel").pack())
    )
    builder.adjust(2,1)
    return builder.as_markup()

#fc - first call
fc_inline_vuz = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text=f"Добавить ВУЗ", callback_data=AddingList(action="add").pack())
        ]
    ]
)
fc_inline_criteria = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text=f"Добавить критерий", callback_data=AddingList(action="add").pack())
        ]
    ]
)

class Compare(CallbackData, prefix="comp"):
    value: float #Для определения значения превосходства
    index: int #Для определения первого или второго объекта

def inline_compare(index: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Равнозначны", callback_data=Compare(value=1, index=index).pack()),
        InlineKeyboardButton(text="Немного лучше", callback_data=Compare(value=3, index=index).pack()),
        InlineKeyboardButton(text="Немного хуже", callback_data=Compare(value=1/3, index=index).pack()),
        InlineKeyboardButton(text="Лучше", callback_data=Compare(value=5, index=index).pack()),
        InlineKeyboardButton(text="Хуже", callback_data=Compare(value=1/5, index=index).pack()),
        InlineKeyboardButton(text="Значительно лучше", callback_data=Compare(value=7, index=index).pack()),
        InlineKeyboardButton(text="Значительно хуже", callback_data=Compare(value=1/7, index=index).pack()),
        InlineKeyboardButton(text="Принципиально лушче", callback_data=Compare(value=9, index=index).pack()),
        InlineKeyboardButton(text="Принципиально хуже", callback_data=Compare(value=1/9, index=index).pack())
    )
    builder.adjust(1,2,2,2,2)
    return builder.as_markup()

#fc - first call
fc_inline_vuz = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Добавить ВУЗ", callback_data=AddingList(action="add").pack())
        ]
    ]
)