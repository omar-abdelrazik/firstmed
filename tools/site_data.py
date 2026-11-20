"""Shared site data. Every visible string is a pair: (English, Arabic).

Honesty rule for this file: only facts we can show. If something is not
confirmed, it is written as "on request" or labelled as a target.
"""

SITE_URL = "https://www.1st-medical.com"

CONTACT = {
    "sales_phone": "+20 128 366 3238",
    "sales_wa": "201283663238",
    "sales_email": "sales@1st-medical.com",
    "export_phone": "+20 100 642 7397",
    "export_wa": "201006427397",
    "export_email": "export@1st-medical.com",
    "maps": "https://www.google.com/maps/search/?api=1&query=Tala%2C%20Menoufia%2C%20Egypt",
}

# ---------------------------------------------------------------- services menu
SERVICES = [
    {
        "slug": "services/enterprises.html",
        "title": ("For enterprises", "للمؤسسات الصحية"),
        "lead": ("Hospitals, clinics and pharmacies", "المستشفيات والعيادات والصيدليات"),
        "items": [
            {"id": "hospitals", "name": ("Hospitals", "المستشفيات"),
             "desc": ("Adhesive dressings for post-operative and ward care, from 6 × 8 to 10 × 35 cm.",
                      "لاصقات جروح لما بعد العمليات وللأقسام الداخلية، من 6 × 8 حتى 10 × 35 سم.")},
            {"id": "clinics", "name": ("Clinics", "العيادات"),
             "desc": ("Packs of 20 and 75 that suit outpatient and primary care.",
                      "عبوات 20 و75 قطعة تناسب العيادات الخارجية والرعاية الأولية.")},
            {"id": "pharmacies", "name": ("Pharmacies", "الصيدليات"),
             "desc": ("Shelf-ready cartons, labelled in Arabic and English.",
                      "كراتين جاهزة للرف، بياناتها بالعربية والإنجليزية.")},
        ],
    },
    {
        "slug": "services/government.html",
        "title": ("For government", "للجهات الحكومية"),
        "lead": ("Public healthcare, NGOs and emergency programmes", "الرعاية الحكومية والمنظمات الأهلية وبرامج الطوارئ"),
        "items": [
            {"id": "government-healthcare", "name": ("Government healthcare", "الرعاية الصحية الحكومية"),
             "desc": ("We prepare the documents your tender asks for, and say early what we can supply.",
                      "نجهّز المستندات التي تطلبها المناقصة، ونوضّح مبكرًا ما نستطيع توريده.")},
            {"id": "ngos", "name": ("NGOs", "المنظمات الأهلية"),
             "desc": ("Fair pricing for humanitarian and community health programmes.",
                      "أسعار عادلة لبرامج الإغاثة والصحة المجتمعية.")},
            {"id": "emergency", "name": ("Emergency response", "الاستجابة للطوارئ"),
             "desc": ("A straight answer on what is in stock and how fast it can move.",
                      "إجابة واضحة عمّا في المخزن، وعن أقرب موعد للتسليم.")},
        ],
    },
    {
        "slug": "services/partners.html",
        "title": ("For partners", "للشركاء"),
        "lead": ("Distributors, export partners and private label", "الموزعون وشركاء التصدير والعلامات الخاصة"),
        "items": [
            {"id": "distributors", "name": ("Distributors", "الموزعون"),
             "desc": ("Volume pricing, with lead times confirmed before you order.",
                      "أسعار للكميات، ومواعيد توريد نؤكدها قبل الطلب.")},
            {"id": "export", "name": ("Export partners", "شركاء التصدير"),
             "desc": ("The Gulf and Europe are our 2027 target. Talk to us early.",
                      "الخليج وأوروبا هدفنا في 2027. تواصل معنا من الآن.")},
            {"id": "oem", "name": ("OEM and private label", "التصنيع بعلامتك التجارية"), "page": "services/oem.html",
             "desc": ("Your brand on our dressings: pouch, carton and pack count.",
                      "علامتك التجارية على منتجاتنا: الكيس والكرتونة وعدد القطع.")},
        ],
    },
]

# ---------------------------------------------------------------- products
CATEGORIES = [
    {"id": "wound", "name": ("Wound care", "العناية بالجروح"),
     "desc": ("Adhesive dressings, absorbent pads and gauze.", "لاصقات الجروح والوسادات الماصّة والشاش.")},
    {"id": "eye", "name": ("Eye care", "العناية بالعين"),
     "desc": ("Adhesive eye pads.", "أغطية العين اللاصقة.")},
    {"id": "nonwoven", "name": ("Non-woven materials", "الخامات غير المنسوجة"),
     "desc": ("Non-woven fabric on rolls.", "قماش غير منسوج على رولات.")},
]

RIGHT_PRO_SIZES = [
    # key, label, pieces per carton, image
    ("6x8", "6 × 8 cm", 75, "img/products/right-pro-6x8.webp"),
    ("10x12", "10 × 12 cm", 20, "img/products/right-pro-10x12.webp"),
    ("10x18", "10 × 18 cm", 20, "img/products/right-pro-10x18.webp"),
    ("10x25", "10 × 25 cm", 20, "img/products/right-pro-10x25.webp"),
    ("10x35", "10 × 35 cm", 20, "img/products/right-pro-10x35.webp"),
]

PRODUCTS = [
    {
        "id": "right-pro", "cat": "wound", "featured": True,
        "name": ("Right Pro adhesive dressing", "لاصق جروح رايت برو"),
        "short": ("Five sizes, packs of 20 and 75", "خمسة مقاسات، عبوات 20 و75 قطعة"),
        "desc": ("Non-woven fabric adhesive wound dressing with an absorbent pad that does not stick to the wound.",
                 "لاصق جروح من القماش غير المنسوج، بوسادة ماصّة لا تلتصق بالجرح."),
        "img": "img/products/right-pro-10x18.webp",
        "spec": [
            (("Material", "الخامة"), ("Non-woven fabric with adhesive, absorbent non-stick pad", "قماش غير منسوج لاصق، ووسادة ماصّة لا تلتصق بالجرح")),
            (("Labelling", "البيانات"), ("Arabic and English", "بالعربية والإنجليزية")),
            (("Every pouch", "على كل كيس"), ("Production and expiry dates", "تاريخ الإنتاج وتاريخ الانتهاء")),
            (("Made in", "بلد الصنع"), ("Tala, Menoufia, Egypt", "تلا، المنوفية، مصر")),
        ],
    },
    {
        "id": "pads", "cat": "wound",
        "name": ("Absorbent pads", "وسادات ماصّة"),
        "short": ("Non-adhesive, three shapes", "غير لاصقة، بثلاثة أشكال"),
        "desc": ("Soft, non-adhesive absorbent pads for wound care, held in place with gauze or a bandage.",
                 "وسادات ماصّة ناعمة وغير لاصقة للعناية بالجروح، تُثبَّت بالشاش أو الرباط."),
        "img": "img/products/pad-square.webp",
        "variants": [
            ("square", ("Square", "مربعة"), "img/products/pad-square.webp"),
            ("large", ("Large square", "مربعة كبيرة"), "img/products/pad-square-large.webp"),
            ("rect", ("Rectangular", "مستطيلة"), "img/products/pad-rectangular.webp"),
        ],
        "spec": [
            (("Type", "النوع"), ("Non-adhesive absorbent pad", "وسادة ماصّة غير لاصقة")),
            (("Sizes", "المقاسات"), ("On request", "حسب الطلب")),
        ],
    },
    {
        "id": "gauze", "cat": "wound",
        "name": ("Gauze swabs", "شاش طبي مطوي"),
        "short": ("Folded cotton gauze", "شاش قطني مطوي"),
        "desc": ("Folded cotton gauze swabs for cleaning, covering and absorbing.",
                 "شاش قطني مطوي للتنظيف والتغطية والامتصاص."),
        "img": "img/products/gauze-swabs.webp",
        "spec": [
            (("Material", "الخامة"), ("Cotton gauze", "شاش قطني")),
            (("Sizes and ply", "المقاسات وعدد الطبقات"), ("On request", "حسب الطلب")),
        ],
    },
    {
        "id": "eye-pad", "cat": "eye",
        "name": ("Adhesive eye pad, adult", "غطاء عين لاصق للكبار"),
        "short": ("Oval, with a soft absorbent centre", "بيضاوي، بوسادة ماصّة ناعمة"),
        "desc": ("Oval adhesive eye pad with a soft absorbent centre, made under our Right Pro name.",
                 "غطاء عين بيضاوي لاصق، بوسادة ماصّة ناعمة في المنتصف، ضمن منتجات رايت برو."),
        "img": "img/products/eye-pad-oval.webp",
        "spec": [
            (("Shape", "الشكل"), ("Oval", "بيضاوي")),
            (("Size", "المقاس"), ("Adult", "للكبار")),
            (("Labelling", "البيانات"), ("Arabic and English", "بالعربية والإنجليزية")),
        ],
    },
    {
        "id": "nonwoven-rolls", "cat": "nonwoven",
        "name": ("Non-woven fabric rolls", "رولات قماش غير منسوج"),
        "short": ("For medical use", "للاستخدام الطبي"),
        "desc": ("Non-woven fabric on rolls for medical use.",
                 "قماش غير منسوج على رولات للاستخدام الطبي."),
        "img": "img/products/nonwoven-roll.webp",
        "spec": [
            (("Colours, widths, weights", "الألوان والعروض والأوزان"), ("On request", "حسب الطلب")),
        ],
    },
]
