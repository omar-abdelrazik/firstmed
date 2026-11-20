"""Shared site data. Every visible string is a pair: (English, Arabic).

Each language is written for its own reader. Never put the other language's
word next to a title on a page.
"""

# The address the site is served from. Link previews (WhatsApp, LinkedIn) load the logo from here,
# so switch it to https://www.1st-medical.com only once that domain points at the site.
SITE_URL = "https://firstmed.vercel.app"

CONTACT = {
    "sales_phone": "+20 128 366 3238",
    "wa": "201006427397",               # every WhatsApp button goes here
    "wa_display": "+20 100 642 7397",
    "sales_email": "sales@1st-medical.com",
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
                      "غيار لاصق لجروح ما بعد العمليات وللأقسام الداخلية، من 6 × 8 حتى 10 × 35 سم.")},
            {"id": "clinics", "name": ("Clinics", "العيادات"),
             "desc": ("Packs of 20 and 75 that suit outpatient and primary care.",
                      "عبوات 20 و75 قطعة تناسب العيادات الخارجية والرعاية الأولية.")},
            {"id": "pharmacies", "name": ("Pharmacies", "الصيدليات"),
             "desc": ("Shelf-ready cartons, labelled in Arabic and English.",
                      "كراتين جاهزة للعرض، بياناتها بالعربية والإنجليزية.")},
        ],
    },
    {
        "slug": "services/government.html",
        "title": ("For government", "للجهات الحكومية"),
        "lead": ("Public healthcare, NGOs and emergency programmes", "الرعاية الصحية العامة والمنظمات الأهلية وبرامج الطوارئ"),
        "items": [
            {"id": "government-healthcare", "name": ("Government healthcare", "الرعاية الصحية الحكومية"),
             "desc": ("Tender documents prepared to your specification.",
                      "مستندات المناقصة نجهّزها وفق كراسة الشروط.")},
            {"id": "ngos", "name": ("NGOs", "المنظمات الأهلية"),
             "desc": ("Fair pricing for humanitarian and community health programmes.",
                      "أسعار عادلة لبرامج الإغاثة والصحة المجتمعية.")},
            {"id": "emergency", "name": ("Emergency response", "الاستجابة للطوارئ"),
             "desc": ("Clear answers on stock and delivery when time matters.",
                      "إجابات واضحة عن المخزون ومواعيد التسليم وقت الحاجة.")},
        ],
    },
    {
        "slug": "services/partners.html",
        "title": ("For partners", "للشركاء"),
        "lead": ("Distributors, export partners and private label", "الموزعون وشركاء التصدير والعلامات الخاصة"),
        "items": [
            {"id": "distributors", "name": ("Distributors", "الموزعون"),
             "desc": ("Volume pricing, with lead times confirmed before you order.",
                      "أسعار للكميات، ومواعيد توريد مؤكدة قبل الطلب.")},
            {"id": "export", "name": ("Export partners", "شركاء التصدير"),
             "desc": ("Gulf and European markets, targeted for 2027.",
                      "أسواق الخليج وأوروبا، ضمن خطتنا لعام 2027.")},
            {"id": "oem", "name": ("OEM and private label", "التصنيع بعلامتك التجارية"), "page": "services/oem.html",
             "desc": ("Your brand on our dressings: pouch, carton and pack count.",
                      "علامتك التجارية على منتجاتنا: العبوة والكرتونة وعدد القطع.")},
        ],
    },
]

# ---------------------------------------------------------------- products
CATEGORIES = [
    {"id": "wound", "name": ("Wound care", "العناية بالجروح"),
     "desc": ("Adhesive dressings and non-adhesive dressing pads.", "الغيار الطبي اللاصق وغيار الدريسنج.")},
    {"id": "eye", "name": ("Eye care", "العناية بالعين"),
     "desc": ("Adhesive eye patches.", "غيار العين اللاصق.")},
    {"id": "nonwoven", "name": ("Non-woven materials", "الخامات غير المنسوجة"),
     "desc": ("Non-woven fabric on rolls.", "قماش نون ووفن على أتواب.")},
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
        "name": ("Right Pro adhesive dressing", "غيار طبي لاصق رايت برو"),
        "short": ("Five sizes, packs of 20 and 75", "خمسة مقاسات، عبوات 20 و75 قطعة"),
        "desc": ("Non-woven fabric adhesive wound dressing with an absorbent pad that does not stick to the wound.",
                 "غيار لاصق من القماش غير المنسوج، بوسادة ماصّة لا تلتصق بالجرح."),
        "img": "img/products/right-pro-10x18.webp",
        "spec": [
            (("Material", "الخامة"), ("Non-woven fabric with adhesive; absorbent, non-stick pad", "قماش غير منسوج لاصق، ووسادة ماصّة لا تلتصق بالجرح")),
            (("Labelling", "البيانات"), ("Arabic and English", "بالعربية والإنجليزية")),
            (("On every pouch", "على كل عبوة"), ("Production and expiry dates", "تاريخ الإنتاج وتاريخ الانتهاء")),
            (("Made in", "بلد الصنع"), ("Tala, Menoufia, Egypt", "تلا، المنوفية، مصر")),
        ],
    },
    {
        "id": "pads", "cat": "wound",
        "name": ("Dressing pads", "غيار طبي دريسنج"),
        "short": ("Three sizes, 10 to 25 per pack", "ثلاثة مقاسات، من 10 إلى 25 قطعة في العبوة"),
        "desc": ("Soft, non-adhesive absorbent dressing for wound care, held in place with a bandage or tape.",
                 "غيار ماصّ ناعم غير لاصق للعناية بالجروح، يُثبَّت بالرباط أو البلاستر."),
        "img": "img/products/pad-square.webp",
        "spec": [
            (("10 × 10 cm", "10 × 10 سم"), ("25 pieces per pack", "25 قطعة في العبوة")),
            (("10 × 20 cm", "10 × 20 سم"), ("15 pieces per pack", "15 قطعة في العبوة")),
            (("15 × 25 cm", "15 × 25 سم"), ("10 pieces per pack", "10 قطع في العبوة")),
        ],
    },
    {
        "id": "eye-pad", "cat": "eye",
        "name": ("Adhesive eye patch", "غيار عين لاصق"),
        "short": ("Box of 40, carton of 45 boxes", "علبة 40 قطعة، وكرتونة 45 علبة"),
        "desc": ("Oval adhesive eye patch with a soft absorbent centre, part of the Right Pro range.",
                 "غيار عين بيضاوي لاصق بوسادة ماصّة ناعمة في المنتصف، ضمن منتجات رايت برو."),
        "img": "img/products/eye-pad-oval.webp",
        "spec": [
            (("Shape", "الشكل"), ("Oval", "بيضاوي")),
            (("Size", "المقاس"), ("Adult", "للكبار")),
            (("Pieces per box", "عدد القطع في العلبة"), ("40", "40 قطعة")),
            (("Boxes per carton", "عدد العلب في الكرتونة"), ("45 boxes, 1,800 pieces in total", "45 علبة، بإجمالي 1800 قطعة")),
            (("Labelling", "البيانات"), ("Arabic and English", "بالعربية والإنجليزية")),
        ],
    },
    {
        "id": "nonwoven-rolls", "cat": "nonwoven",
        "name": ("Non-woven fabric rolls", "أتواب نون ووفن"),
        "short": ("90 cm wide, 30 m per roll", "عرض 90 سم، وطول التوب 30 مترًا"),
        "desc": ("Non-woven fabric on rolls for medical use.",
                 "قماش نون ووفن على أتواب للاستخدام الطبي."),
        "img": "img/products/nonwoven-roll.webp",
        "spec": [
            (("Width", "العرض"), ("90 cm", "90 سم")),
            (("Length per roll", "طول التوب"), ("30 m", "30 مترًا")),
        ],
    },
]
