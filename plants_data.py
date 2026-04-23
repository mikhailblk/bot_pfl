import os
from typing import Dict, List, Optional
from language import Language


class Plant:
    def __init__(self, plant_id: str, display_name: str, price_per_gram: float,
                 thc: float, cbd: float, genetics: Dict[Language, str],
                 origin: Dict[Language, str], irradiation: Dict[Language, str],
                 manufacturer: str, strain: str, terpenes: List[str],
                 description: Dict[Language, str], photo_number: Optional[int] = None):
        self.id = plant_id
        self.display_name = display_name
        self.price_per_gram = price_per_gram
        self.thc = thc
        self.cbd = cbd
        self.genetics = genetics
        self.origin = origin
        self.irradiation = irradiation
        self.manufacturer = manufacturer
        self.strain = strain
        self.terpenes = terpenes
        self.description = description
        self.photo_number = photo_number  # Номер фото (1, 2, 3...)

    def get_name(self, lang: Language) -> str:
        return self.display_name

    def get_price(self, lang: Language) -> str:
        return f"{self.price_per_gram:.2f} €"

    def get_description(self, lang: Language) -> str:
        return self.description.get(lang, self.description[Language.DE])

    def get_genetics_key(self, lang: Language) -> str:
        """Получить ключ генетики для фильтрации (sativa/indica/hybrid)"""
        genetics_text = self.genetics.get(lang, self.genetics[Language.DE]).lower()

        # Проверяем на русском и английском
        if "сатива" in genetics_text or "sativa" in genetics_text:
            return "sativa"
        elif "индика" in genetics_text or "indica" in genetics_text:
            return "indica"
        elif "гибрид" in genetics_text or "hybrid" in genetics_text:
            return "hybrid"
        else:
            print(f"DEBUG: Неизвестный тип генетики для {self.display_name}: {genetics_text}")
            return "hybrid"

    def get_photo_path(self) -> Optional[str]:
        """Получить путь к файлу фото по номеру"""
        if self.photo_number:
            # Пробуем разные расширения
            for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                photo_path = f"photos/{self.photo_number}{ext}"
                if os.path.exists(photo_path):
                    return photo_path
        return None

    def get_short_info(self, lang: Language) -> str:
        """Короткая информация для карточки"""
        genetics_text = self.genetics.get(lang, self.genetics[Language.DE])
        origin_text = self.origin.get(lang, self.origin[Language.DE])
        irradiation_text = self.irradiation.get(lang, self.irradiation[Language.DE])

        if lang == Language.RU:
            return f"🔥 THC: {self.thc}% | CBD: {self.cbd}%\n🌱 Генетика: {genetics_text}\n🌍 Страна: {origin_text}\n⚡️ Облучение: {irradiation_text}"
        elif lang == Language.EN:
            return f"🔥 THC: {self.thc}% | CBD: {self.cbd}%\n🌱 Genetics: {genetics_text}\n🌍 Origin: {origin_text}\n⚡️ Irradiation: {irradiation_text}"
        else:
            return f"🔥 THC: {self.thc}% | CBD: {self.cbd}%\n🌱 Genetik: {genetics_text}\n🌍 Herkunft: {origin_text}\n⚡️ Bestrahlung: {irradiation_text}"

    def get_full_info_text(self, lang: Language) -> str:
        """Полная информация о растении (только текст, без фото)"""
        genetics_text = self.genetics.get(lang, self.genetics[Language.DE])
        origin_text = self.origin.get(lang, self.origin[Language.DE])
        irradiation_text = self.irradiation.get(lang, self.irradiation[Language.DE])

        if lang == Language.RU:
            thc_label = "THC"
            cbd_label = "CBD"
            genetics_label = "Генетика"
            origin_label = "Происхождение"
            irradiation_label = "Облучение"
            manufacturer_label = "Производитель"
            strain_label = "Штамм"
            terpenes_label = "Терпены"
        elif lang == Language.EN:
            thc_label = "THC"
            cbd_label = "CBD"
            genetics_label = "Genetics"
            origin_label = "Origin"
            irradiation_label = "Irradiation"
            manufacturer_label = "Manufacturer"
            strain_label = "Strain"
            terpenes_label = "Terpenes"
        else:
            thc_label = "THC"
            cbd_label = "CBD"
            genetics_label = "Genetik"
            origin_label = "Herkunft"
            irradiation_label = "Bestrahlung"
            manufacturer_label = "Hersteller"
            strain_label = "Strain"
            terpenes_label = "Terpene"

        terpenes_str = ", ".join(self.terpenes)

        info = (
            f"*{self.display_name}*\n\n"
            f"💰 *{self.price_per_gram:.2f} €/g*\n\n"
            f"🔥 *{thc_label}:* {self.thc}% | *{cbd_label}:* {self.cbd}%\n"
            f"🌱 *{genetics_label}:* {genetics_text}\n"
            f"🌍 *{origin_label}:* {origin_text}\n"
            f"⚡️ *{irradiation_label}:* {irradiation_text}\n"
            f"🏭 *{manufacturer_label}:* {self.manufacturer}\n"
            f"🔬 *{strain_label}:* {self.strain}\n"
            f"🌿 *{terpenes_label}:* {terpenes_str}\n\n"
            f"📝 {self.description.get(lang, self.description[Language.DE])}"
        )
        return info


# Хранилище растений
PLANTS: Dict[str, Plant] = {}


# ========== 1. Garlic Skittlez (фото 1) ==========
PLANTS["garlic_skittlez"] = Plant(
    plant_id="garlic_skittlez",
    display_name="🧄 Garlic Skittlez",
    price_per_gram=10 //4,25
    thc=30.0,
    cbd=1.0,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Remexian Pharma",
    strain="Garlic Skittlez",
    terpenes=["Beta-Caryophyllen", "Beta-Myrcen", "Alpha-Humulen"],
    description={
        Language.DE: "Eufloria 30/1 GSZ mit dem Strain Garlic Skittlez hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 30,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Eufloria 30/1 GSZ with the Garlic Skittlez strain has hybrid genetics. The active ingredient content is approximately 30.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Eufloria 30/1 GSZ со штаммом Garlic Skittlez имеет гибридную генетику. Содержание действующего вещества составляет примерно 30,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=1  # Фото 1
)


# ========== 2. Minty Cookies (фото 2) ==========
PLANTS["minty_cookies"] = Plant(
    plant_id="minty_cookies",
    display_name="🍪 Minty Cookies",
    price_per_gram=10 //4.25,
    thc=27.0,
    cbd=1.0,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="Minty Cookies",
    terpenes=["Linalool", "D-Limonen", "Beta-Caryophyllen"],
    description={
        Language.DE: "enua 27/1 PS3 CA MYC mit dem Strain Minty Cookies hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 27,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "enua 27/1 PS3 CA MYC with the Minty Cookies strain has hybrid genetics. The active ingredient content is approximately 27.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "enua 27/1 PS3 CA MYC со штаммом Minty Cookies имеет гибридную генетику. Содержание действующего вещества составляет примерно 27,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=2  # Фото 2
)


# ========== 3. Crispy Doughnut (фото 3) ==========
PLANTS["crispy_doughnut"] = Plant(
    plant_id="crispy_doughnut",
    display_name="🍩 Crispy Doughnut",
    price_per_gram=10 //4.25,
    thc=25.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="Crispy Doughnut",
    terpenes=["Beta-Ocimem", "Beta-Myrcen", "Beta-Caryophyllen"],
    description={
        Language.DE: "enua 25/1 CDG CA mit dem Strain Crispy Doughnut hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 25,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "enua 25/1 CDG CA with the Crispy Doughnut strain has hybrid genetics. The active ingredient content is approximately 25.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "enua 25/1 CDG CA со штаммом Crispy Doughnut имеет гибридную генетику. Содержание действующего вещества составляет примерно 25,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=3  # Фото 3
)


# ========== 4. Scented Marker (фото 4) ==========
PLANTS["scented_marker"] = Plant(
    plant_id="scented_marker",
    display_name="🖍️ Scented Marker",
    price_per_gram=12 //5.95,
    thc=33.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Four 20 Pharma",
    strain="Scented Marker",
    terpenes=["Linalool", "D-Limonen", "Beta-Caryophyllen"],
    description={
        Language.DE: "420 Evolution 33/1 CA SCM mit dem Strain Scented Marker hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 33,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "420 Evolution 33/1 CA SCM with the Scented Marker strain has hybrid genetics. The active ingredient content is approximately 33.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "420 Evolution 33/1 CA SCM со штаммом Scented Marker имеет гибридную генетику. Содержание действующего вещества составляет примерно 33,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=4  # Фото 4
)


# ========== 5. Pink Kush (фото 5) ==========
PLANTS["pink_kush"] = Plant(
    plant_id="pink_kush",
    display_name="🌸 Pink Kush",
    price_per_gram=10 //4.25,
    thc=24.5,
    cbd=1.0,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="Pink Kush",
    terpenes=["Ocimen", "Linalool", "Bisabolol"],
    description={
        Language.DE: "enua 27/1 PS3 PNK mit dem Strain Pink Kush hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 24,5% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "enua 27/1 PS3 PNK with the Pink Kush strain has hybrid genetics. The active ingredient content is approximately 24.5% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "enua 27/1 PS3 PNK со штаммом Pink Kush имеет гибридную генетику. Содержание действующего вещества составляет примерно 24,5% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=5  # Фото 5
)


# ========== 6. Munyunz (фото 6) ==========
PLANTS["munyunz"] = Plant(
    plant_id="munyunz",
    display_name="🍬 Munyunz",
    price_per_gram=10 //4.25,
    thc=27.0,
    cbd=1.0,
    genetics={
        Language.DE: "Sativa dominant",
        Language.EN: "Sativa dominant",
        Language.RU: "Сатива доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Remexian Pharma",
    strain="Munyunz",
    terpenes=["Pinene", "Linalool", "Limonen"],
    description={
        Language.DE: "Remexian 27/1 GJY MUN mit dem Strain Munyunz hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 27,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Remexian 27/1 GJY MUN with the Munyunz strain has hybrid genetics. The active ingredient content is approximately 27.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Remexian 27/1 GJY MUN со штаммом Munyunz имеет гибридную генетику. Содержание действующего вещества составляет примерно 27,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=6  # Фото 6
)


# ========== 7. Purple Churro (фото 7) ==========
PLANTS["purple_churro"] = Plant(
    plant_id="purple_churro",
    display_name="🟣 Purple Churro",
    price_per_gram=12 //5.20,
    thc=27.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Remexian Pharma",
    strain="Purple Churro",
    terpenes=["Linalool", "Humulen", "Beta-Pinen"],
    description={
        Language.DE: "Eufloria 27/1 PCH mit dem Strain Purple Churro hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 27,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Eufloria 27/1 PCH with the Purple Churro strain has hybrid genetics. The active ingredient content is approximately 27.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Eufloria 27/1 PCH со штаммом Purple Churro имеет гибридную генетику. Содержание действующего вещества составляет примерно 27,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=7  # Фото 7
)


# ========== 8. Zlush Runtz (фото 8) ==========
PLANTS["zlush_runtz"] = Plant(
    plant_id="zlush_runtz",
    display_name="🍬 Zlush Runtz",
    price_per_gram=12 //5.20,
    thc=30.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Portugal",
        Language.EN: "Portugal",
        Language.RU: "Португалия"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Remexian Pharma",
    strain="Zlush Runtz",
    terpenes=["Linalool", "Humulen", "Beta-Pinen"],
    description={
        Language.DE: "Eufloria 30/1 ZRU mit dem Strain Zlush Runtz hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 30,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Portugal produziert.",
        Language.EN: "Eufloria 30/1 ZRU with the Zlush Runtz strain has hybrid genetics. The active ingredient content is approximately 30.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Portugal.",
        Language.RU: "Eufloria 30/1 ZRU со штаммом Zlush Runtz имеет гибридную генетику. Содержание действующего вещества составляет примерно 30,0% THC и 1,0% CBD. Сорт необлучённый и производится в Португалии."
    },
    photo_number=8  # Фото 8
)


# ========== 9. OG Kush (фото 9) ==========
PLANTS["og_kush"] = Plant(
    plant_id="og_kush",
    display_name="🌲 OG Kush",
    price_per_gram=10 //4.25,
    thc=22.0,
    cbd=1.0,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="OG Kush",
    terpenes=["D-Limonen", "Beta-Caryophyllen", "Beta-Myrcen"],
    description={
        Language.DE: "Slouu 22/1 PS3 CA OGK mit dem Strain OG Kush hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 22,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Slouu 22/1 PS3 CA OGK with the OG Kush strain has hybrid genetics. The active ingredient content is approximately 22.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Slouu 22/1 PS3 CA OGK со штаммом OG Kush имеет гибридную генетику. Содержание действующего вещества составляет примерно 22,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=9  # Фото 9
)


# ========== 10. White Widow (фото 10) ==========
PLANTS["white_widow"] = Plant(
    plant_id="white_widow",
    display_name="🕷️ White Widow",
    price_per_gram=10 //4.90,
    thc=18.0,
    cbd=1.0,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Dänemark",
        Language.EN: "Denmark",
        Language.RU: "Дания"
    },
    irradiation={
        Language.DE: "Bestrahlt",
        Language.EN: "Irradiated",
        Language.RU: "Облучённый"
    },
    manufacturer="Weeco",
    strain="White Widow",
    terpenes=["Nerolidol", "Myrcen", "Linalool"],
    description={
        Language.DE: "Weeco 1A 18/1 WW mit dem Strain White Widow hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 18,0% THC und 1,0% CBD. Die Blütensorte ist bestrahlt und wird in Dänemark produziert.",
        Language.EN: "Weeco 1A 18/1 WW with the White Widow strain has hybrid genetics. The active ingredient content is approximately 18.0% THC and 1.0% CBD. The flower variety is irradiated and produced in Denmark.",
        Language.RU: "Weeco 1A 18/1 WW со штаммом White Widow имеет гибридную генетику. Содержание действующего вещества составляет примерно 18,0% THC и 1,0% CBD. Сорт облучённый и производится в Дании."
    },
    photo_number=10  # Фото 10
)


# ========== 11. Marshmallow OG (фото 11) ==========
PLANTS["marshmallow_og"] = Plant(
    plant_id="marshmallow_og",
    display_name="🍡 Marshmallow OG",
    price_per_gram=12 //5.20,
    thc=27.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Remexian Pharma",
    strain="Marshmallow OG",
    terpenes=["Limonen", "Beta-Myrcen", "Alpha-Caryophyllene"],
    description={
        Language.DE: "Eufloria 27/1 MOG mit dem Strain Marshmallow OG hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 27,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Eufloria 27/1 MOG with the Marshmallow OG strain has hybrid genetics. The active ingredient content is approximately 27.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Eufloria 27/1 MOG со штаммом Marshmallow OG имеет гибридную генетику. Содержание действующего вещества составляет примерно 27,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=11  # Фото 11
)


# ========== 12. Pineapple Fruz (фото 12) ==========
PLANTS["pineapple_fruz"] = Plant(
    plant_id="pineapple_fruz",
    display_name="🍍 Pineapple Fruz",
    price_per_gram=12 //5.95,
    thc=27.0,
    cbd=1.0,
    genetics={
        Language.DE: "Sativa dominant",
        Language.EN: "Sativa dominant",
        Language.RU: "Сатива доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Four 20 Pharma",
    strain="Pineapple Fruz",
    terpenes=["Selinadiene", "Germacrene", "D-Limonen"],
    description={
        Language.DE: "420 Evolution 27/1 CA PEX mit dem Strain Pineapple Fruz hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 27,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "420 Evolution 27/1 CA PEX with the Pineapple Fruz strain has hybrid genetics. The active ingredient content is approximately 27.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "420 Evolution 27/1 CA PEX со штаммом Pineapple Fruz имеет гибридную генетику. Содержание действующего вещества составляет примерно 27,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=12  # Фото 12
)


# ========== 13. Sweet San Valley (фото 13) ==========
PLANTS["sweet_san_valley"] = Plant(
    plant_id="sweet_san_valley",
    display_name="🍬 Sweet San Valley",
    price_per_gram=12 //5.60,
    thc=30.0,
    cbd=1.0,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="Sweet San Valley",
    terpenes=["D-Limonen", "Beta-Caryophyllen", "Beta-Myrcen"],
    description={
        Language.DE: "enua SSV CA 30/1 mit dem Strain Sweet San Valley hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 30,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "enua SSV CA 30/1 with the Sweet San Valley strain has hybrid genetics. The active ingredient content is approximately 30.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "enua SSV CA 30/1 со штаммом Sweet San Valley имеет гибридную генетику. Содержание действующего вещества составляет примерно 30,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=13  # Фото 13
)


# ========== 14. Pineapple God (фото 14) ==========
PLANTS["pineapple_god"] = Plant(
    plant_id="pineapple_god",
    display_name="🍍 Pineapple God",
    price_per_gram=12 //5.20,
    thc=25.0,
    cbd=1.0,
    genetics={
        Language.DE: "Sativa dominant",
        Language.EN: "Sativa dominant",
        Language.RU: "Сатива доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Four 20 Pharma",
    strain="Pineapple God",
    terpenes=["Linalool", "D-Limonen", "Beta-Caryophyllen"],
    description={
        Language.DE: "Huala 25/1 CA POG mit dem Strain Pineapple God hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 25,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Huala 25/1 CA POG with the Pineapple God strain has hybrid genetics. The active ingredient content is approximately 25.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Huala 25/1 CA POG со штаммом Pineapple God имеет гибридную генетику. Содержание действующего вещества составляет примерно 25,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=14  # Фото 14
)


# ========== 15. Jungle Fumes (фото 15) ==========
PLANTS["jungle_fumes"] = Plant(
    plant_id="jungle_fumes",
    display_name="🌴 Jungle Fumes",
    price_per_gram=15 //7.45,
    thc=36.0,
    cbd=1.0,
    genetics={
        Language.DE: "Sativa dominant",
        Language.EN: "Sativa dominant",
        Language.RU: "Сатива доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="enua Pharma",
    strain="Jungle Fumes",
    terpenes=["Myrcen", "Limonen", "Beta-Caryophyllen"],
    description={
        Language.DE: "enua 36/1 JGF CA mit dem Strain Jungle Fumes hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 36,0% THC und 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "enua 36/1 JGF CA with the Jungle Fumes strain has hybrid genetics. The active ingredient content is approximately 36.0% THC and 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "enua 36/1 JGF CA со штаммом Jungle Fumes имеет гибридную генетику. Содержание действующего вещества составляет примерно 36,0% THC и 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=15  # Фото 15
)


# ========== 16. Cookies OG (фото 16) ==========
PLANTS["cookies_og"] = Plant(
    plant_id="cookies_og",
    display_name="🍪 Cookies OG",
    price_per_gram=10 //5.30,
    thc=30.0,
    cbd=0.9,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Demecan",
    strain="Cookies OG",
    terpenes=["Beta-Caryophyllen", "Beta-Myrcen", "Alpha-Humulen"],
    description={
        Language.DE: "TRUU GT 30:01 mit dem Strain Cookies OG hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 30,0% THC und < 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "TRUU GT 30:01 with the Cookies OG strain has hybrid genetics. The active ingredient content is approximately 30.0% THC and < 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "TRUU GT 30:01 со штаммом Cookies OG имеет гибридную генетику. Содержание действующего вещества составляет примерно 30,0% THC и < 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=16  # Фото 16
)


# ========== 17. Amsterdam Amnesia (фото 17) ==========
PLANTS["amsterdam_amnesia"] = Plant(
    plant_id="amsterdam_amnesia",
    display_name="🧠 Amsterdam Amnesia",
    price_per_gram=16 //8.20,
    thc=24.0,
    cbd=0.9,
    genetics={
        Language.DE: "Sativa",
        Language.EN: "Sativa",
        Language.RU: "Сатива"
    },
    origin={
        Language.DE: "Nordmazedonien",
        Language.EN: "North Macedonia",
        Language.RU: "Северная Македония"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Cannamedical",
    strain="Amsterdam Amnesia",
    terpenes=["Linalool", "Limonen", "Beta-Pinen"],
    description={
        Language.DE: "Cannamedical Sativa Forte NM mit dem Strain Amsterdam Amnesia hat eine Sativa-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 24,0% THC und < 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Nordmazedonien produziert.",
        Language.EN: "Cannamedical Sativa Forte NM with the Amsterdam Amnesia strain has Sativa genetics. The active ingredient content is approximately 24.0% THC and < 1.0% CBD. The flower variety is non-irradiated and produced in North Macedonia.",
        Language.RU: "Cannamedical Sativa Forte NM со штаммом Amsterdam Amnesia имеет генетику Sativa. Содержание действующего вещества составляет примерно 24,0% THC и < 1,0% CBD. Сорт необлучённый и производится в Северной Македонии."
    },
    photo_number=17  # Фото 17
)


# ========== 18. Super Lemon G (фото 18) ==========
PLANTS["super_lemon_g"] = Plant(
    plant_id="super_lemon_g",
    display_name="🍋 Super Lemon G",
    price_per_gram=12 //6.00,
    thc=5.6,
    cbd=6.8,
    genetics={
        Language.DE: "Sativa",
        Language.EN: "Sativa",
        Language.RU: "Сатива"
    },
    origin={
        Language.DE: "Portugal",
        Language.EN: "Portugal",
        Language.RU: "Португалия"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Four 20 Pharma",
    strain="Super Lemon G",
    terpenes=["D-Limonen", "Beta-Caryophyllen", "Beta-Myrcen"],
    description={
        Language.DE: "420 Balanced Basic PT SLG mit dem Strain Super Lemon G hat eine Sativa-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 5,6% THC und 6,8% CBD. Die Blütensorte ist unbestrahlt und wird in Portugal produziert.",
        Language.EN: "420 Balanced Basic PT SLG with the Super Lemon G strain has Sativa genetics. The active ingredient content is approximately 5.6% THC and 6.8% CBD. The flower variety is non-irradiated and produced in Portugal.",
        Language.RU: "420 Balanced Basic PT SLG со штаммом Super Lemon G имеет генетику Sativa. Содержание действующего вещества составляет примерно 5,6% THC и 6,8% CBD. Сорт необлучённый и производится в Португалии."
    },
    photo_number=18  # Фото 18
)


# ========== 19. Purple Rain (фото 19) ==========
PLANTS["purple_rain"] = Plant(
    plant_id="purple_rain",
    display_name="🌧️ Purple Rain",
    price_per_gram=10 //4.10,
    thc=21.2,
    cbd=0.9,
    genetics={
        Language.DE: "Sativa",
        Language.EN: "Sativa",
        Language.RU: "Сатива"
    },
    origin={
        Language.DE: "Dänemark",
        Language.EN: "Denmark",
        Language.RU: "Дания"
    },
    irradiation={
        Language.DE: "Bestrahlt",
        Language.EN: "Irradiated",
        Language.RU: "Облучённый"
    },
    manufacturer="Weeco",
    strain="Purple Rain",
    terpenes=["Pinene", "Myrcen", "Alpha-Caryophyllene"],
    description={
        Language.DE: "Weeco Duke 20/1 mit dem Strain Purple Rain hat eine Sativa-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 21,2% THC und < 1,0% CBD. Die Blütensorte ist bestrahlt und wird in Dänemark produziert.",
        Language.EN: "Weeco Duke 20/1 with the Purple Rain strain has Sativa genetics. The active ingredient content is approximately 21.2% THC and < 1.0% CBD. The flower variety is irradiated and produced in Denmark.",
        Language.RU: "Weeco Duke 20/1 со штаммом Purple Rain имеет генетику Sativa. Содержание действующего вещества составляет примерно 21,2% THC и < 1,0% CBD. Сорт облучённый и производится в Дании."
    },
    photo_number=19  # Фото 19
)


# ========== 20. First Class Funk (фото 20) ==========
PLANTS["first_class_funk"] = Plant(
    plant_id="first_class_funk",
    display_name="💎 First Class Funk",
    price_per_gram=16 //8.50,
    thc=28.0,
    cbd=0.9,
    genetics={
        Language.DE: "Indica dominant",
        Language.EN: "Indica dominant",
        Language.RU: "Индика доминант"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Demecan",
    strain="First Class Funk",
    terpenes=["Pinene", "Myrcen", "Limonen"],
    description={
        Language.DE: "Demecan CRAFT FCF 28:01 mit dem Strain First Class Funk hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 28,0% THC und < 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "Demecan CRAFT FCF 28:01 with the First Class Funk strain has hybrid genetics. The active ingredient content is approximately 28.0% THC and < 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "Demecan CRAFT FCF 28:01 со штаммом First Class Funk имеет гибридную генетику. Содержание действующего вещества составляет примерно 28,0% THC и < 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=20  # Фото 20
)


# ========== 21. Lemon Slushie (фото 21) ==========
PLANTS["lemon_slushie"] = Plant(
    plant_id="lemon_slushie",
    display_name="🍋 Lemon Slushie",
    price_per_gram=15 //6.98,
    thc=20.0,
    cbd=1.0,
    genetics={
        Language.DE: "Sativa",
        Language.EN: "Sativa",
        Language.RU: "Сатива"
    },
    origin={
        Language.DE: "Mazedonien",
        Language.EN: "Macedonia",
        Language.RU: "Македония"
    },
    irradiation={
        Language.DE: "Bestrahlt",
        Language.EN: "Irradiated",
        Language.RU: "Облучённый"
    },
    manufacturer="Cannamedical",
    strain="Lemon Slushie",
    terpenes=["Linalool", "Limonen", "Beta-Caryophyllen"],
    description={
        Language.DE: "Cannamedical Sativa Classic mit dem Strain Lemon Slushie hat eine Sativa-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 20,0% THC und 1,0% CBD. Die Blütensorte ist bestrahlt und wird in Mazedonien produziert.",
        Language.EN: "Cannamedical Sativa Classic with the Lemon Slushie strain has Sativa genetics. The active ingredient content is approximately 20.0% THC and 1.0% CBD. The flower variety is irradiated and produced in Macedonia.",
        Language.RU: "Cannamedical Sativa Classic со штаммом Lemon Slushie имеет генетику Sativa. Содержание действующего вещества составляет примерно 20,0% THC и 1,0% CBD. Сорт облучённый и производится в Македонии."
    },
    photo_number=21  # Фото 21
)


# ========== 22. Wedding Tree (фото 22) ==========
PLANTS["wedding_tree"] = Plant(
    plant_id="wedding_tree",
    display_name="💍 Wedding Tree",
    price_per_gram=17 //8.30,
    thc=24.0,
    cbd=0.9,
    genetics={
        Language.DE: "Sativa",
        Language.EN: "Sativa",
        Language.RU: "Сатива"
    },
    origin={
        Language.DE: "Nordmazedonien",
        Language.EN: "North Macedonia",
        Language.RU: "Северная Македония"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Cannamedical",
    strain="Wedding Tree",
    terpenes=["Beta-Myrcen", "Beta-Caryophyllen", "Alpha-Pinen"],
    description={
        Language.DE: "Cannamedical Sativa forte NM mit dem Strain Wedding Tree hat eine Sativa-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 24,0% THC und < 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Nordmazedonien produziert.",
        Language.EN: "Cannamedical Sativa forte NM with the Wedding Tree strain has Sativa genetics. The active ingredient content is approximately 24.0% THC and < 1.0% CBD. The flower variety is non-irradiated and produced in North Macedonia.",
        Language.RU: "Cannamedical Sativa forte NM со штаммом Wedding Tree имеет генетику Sativa. Содержание действующего вещества составляет примерно 24,0% THC и < 1,0% CBD. Сорт необлучённый и производится в Северной Македонии."
    },
    photo_number=22  # Фото 22
)


# ========== 23. Peach Chementine (фото 23) ==========
PLANTS["peach_chementine"] = Plant(
    plant_id="peach_chementine",
    display_name="🍑 Peach Chementine",
    price_per_gram=15 //7.20,
    thc=30.0,
    cbd=0.9,
    genetics={
        Language.DE: "Hybrid",
        Language.EN: "Hybrid",
        Language.RU: "Гибрид"
    },
    origin={
        Language.DE: "Kanada",
        Language.EN: "Canada",
        Language.RU: "Канада"
    },
    irradiation={
        Language.DE: "Unbestrahlt",
        Language.EN: "Non-irradiated",
        Language.RU: "Необлучённый"
    },
    manufacturer="Four 20 Pharma",
    strain="Peach Chementine",
    terpenes=["Trans-Caryophyllen", "Limonen", "Farnesen"],
    description={
        Language.DE: "420 Evolution 30/1 CA PCH mit dem Strain Peach Chementine hat eine Hybrid-Genetik. Der Wirkstoffgehalt liegt bei ungefähr 30,0% THC und < 1,0% CBD. Die Blütensorte ist unbestrahlt und wird in Kanada produziert.",
        Language.EN: "420 Evolution 30/1 CA PCH with the Peach Chementine strain has hybrid genetics. The active ingredient content is approximately 30.0% THC and < 1.0% CBD. The flower variety is non-irradiated and produced in Canada.",
        Language.RU: "420 Evolution 30/1 CA PCH со штаммом Peach Chementine имеет гибридную генетику. Содержание действующего вещества составляет примерно 30,0% THC и < 1,0% CBD. Сорт необлучённый и производится в Канаде."
    },
    photo_number=23  # Фото 23
)


# ========== Вспомогательные функции ==========

def get_all_plants() -> List[Plant]:
    """Получить все растения"""
    return list(PLANTS.values())


def get_plant_by_id(plant_id: str) -> Plant:
    """Получить растение по ID"""
    return PLANTS.get(plant_id)


def get_plants_by_genetics_type(genetics_type: str, lang: Language) -> List[Plant]:
    """Фильтрация растений по типу генетики (sativa/indica/hybrid)"""
    result = []
    genetics_type_lower = genetics_type.lower()

    print(f"DEBUG: Фильтрация по типу: {genetics_type_lower}, язык: {lang}")

    for plant in PLANTS.values():
        # Получаем текст генетики на текущем языке
        genetics_text = plant.genetics.get(lang, plant.genetics[Language.DE]).lower()
        print(f"DEBUG: {plant.display_name} - genetics_text={genetics_text}")

        # Определяем тип растения в зависимости от языка
        plant_type = None

        # Проверяем на русском
        if "сатива" in genetics_text or "sativa" in genetics_text:
            plant_type = "sativa"
        elif "индика" in genetics_text or "indica" in genetics_text:
            plant_type = "indica"
        elif "гибрид" in genetics_text or "hybrid" in genetics_text:
            plant_type = "hybrid"

        print(f"DEBUG: {plant.display_name} - plant_type={plant_type}")

        if plant_type == genetics_type_lower:
            result.append(plant)

    print(f"DEBUG: Найдено {len(result)} растений")
    return result