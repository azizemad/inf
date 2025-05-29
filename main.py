from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# دالة البحث عن الرقم (نفس الدالة الأصلية)
def search_number(phone_number):
    url = "https://hellocallers.com/user/search/contact"
    payload = {
        "iso_code": "eg",
        "contact": phone_number,
        "_token": "Pm40jky7FvwCVTLSNlPmmCzRIZRKcftrpFjXFMiU"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Linux\"",
        'x-xsrf-token': "eyJpdiI6Ildib1Ewc09hd2w1S1d1dHYxZ2Nra3c9PSIsInZhbHVlIjoieExBN2ZzZlVaWVB5blhDUENyTmJDYTVDMkpCWVBNZ2lxSHJySWxiXC9iTlpCc0pzcXl2RCtFMlVYTmxcL1gySDRlUDJzYXVJSmY4S1VYZXlZQVVsek9TaEYraWF2WmRaekNOR1FPRFJ4bThTcnZhYlZ2c2Q2c2JWenBWZHZlXC9OVWQiLCJtYWMiOiIwOGU1NDY5MDA5ZTFlYWUyNjQxY2UwZmRmNDNhZWI0ODZkOTExMzMzMmQ1ZTlkMzZhZmE1NDMwY2I5ODgzZjRmIn0=",
        'sec-ch-ua': "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        'content-type': "application/json;charset=UTF-8",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://hellocallers.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://hellocallers.com/user/search?iso2=eg&query=" + phone_number,
        'accept-language': "en-EG,en;q=0.9,ar-EG;q=0.8",
        'priority': "u=1, i",
        'Cookie': "PHPSESSID=ng47sm3e75f1ps5073g7t65nn7; _gcl_au=1.1.472119449.1742905471; _fbp=fb.1.1742905480977.107656991292432494; _clck=18ydvkj%7C2%7Cfui%7C0%7C1910; _ga=GA1.1.694449081.1742905485; hci_si=KK7A7c1uU7pWXKXACuJcT4sEtnaW9Etpf6XBj1rT; fpestid=SvDD_UH2J8B_epxtl20m_bunl3XGG_37mNxcZZAUJZgiFJTVMSg3jCRBDX5j5Wy1MJjSmg; XSRF-TOKEN=eyJpdiI6Ildib1Ewc09hd2w1S1d1dHYxZ2Nra3c9PSIsInZhbHVlIjoieExBN2ZzZlVaWVB5blhDUENyTmJDYTVDMkpCWVBNZ2lxSHJySWxiXC9iTlpCc0pzcXl2RCtFMlVYTmxcL1gySDRlUDJzYXVJSmY4S1VYZXlZQVVsek9TaEYraWF2WmRaekNOR1FPRFJ4bThTcnZhYlZ2c2Q2c2JWenBWZHZlXC9OVWQiLCJtYWMiOiIwOGU1NDY5MDA5ZTFlYWUyNjQxY2UwZmRmNDNhZWI0ODZkOTExMzMzMmQ1ZTlkMzZhZmE1NDMwY2I5ODgzZjRmIn0%3D; _clsk=o8al9y%7C1742905581542%7C2%7C1%7Cl.clarity.ms%2Fcollect; _ga_RSKK6VSJVH=GS1.1.1742905484.1.1.1742905581.0.0.0; _cc_id=8d4083d0df84951293716667981d0ade; panoramaId_expiry=1743510380792; panoramaId=ccf3bf21279b07fc0d1ee4788d2616d5393891caa16d14318473cfd444692aea; panoramaIdType=panoIndiv; __gads=ID=ede7dadbf313b4d4:T=1742905578:RT=1742905578:S=ALNI_MapAVPhUZ2HI9yF1AIGDbHRpqaisw; __eoi=ID=d5c75b815fe8a337:T=1742905578:RT=1742905578:S=AA-AfjaxPkRx-ba2OByy0h_2Jke-; __stripe_mid=329e92cf-24a7-4835-9d19-30c3a6dc59fa142ac3; __stripe_sid=10d7bbf2-c751-4a99-9a63-9e4d76bd7a5f2a1c69"
    }
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            data = response.json()
            contacts = data.get("data", {}).get("contacts", {}).get("data", [])
            if not contacts:
                return {"error": "❌ لم يتم العثور على أي بيانات لهذا الرقم."}
            
            contact = contacts[0]  # أول نتيجة
            
            # استخراج البيانات المطلوبة
            details = {
                "📞 الرقم الدولي": contact.get("international", "غير متوفر"),
                "📌 الرقم المحلي": contact.get("national", "غير متوفر"),
                "🌍 الدولة": contact.get("country_name", "غير متوفر"),
                "🔢 كود الدولة": contact.get("iso_code", "غير متوفر"),
                "🚨 Spam؟": "نعم" if contact.get("is_spam", 0) else "لا",
                "🔄 مرات الإبلاغ عن Spam": contact.get("spams_count", "غير متوفر"),
                "🔠 عدد الأسماء": contact.get("names_count", "غير متوفر"),
                "📋 الأسماء": ", ".join([name.get("name", "غير متوفر") for name in contact.get("names", [])]) or "غير متوفر",
                "🔗 عدد الروابط": contact.get("links_count", "غير متوفر"),
                "🔗 الروابط": ", ".join(contact.get("links_slug", [])) or "غير متوفر",
                "📶 نوع الخط": contact.get("carrier_type_text", "غير متوفر"),
                "📡 شركة الاتصالات": contact.get("carrier_name", "غير متوفر"),
                "🆔 UUID": contact.get("uuid", "غير متوفر"),
                "🎨 لون الأفاتار": contact.get("avatar_color", "غير متوفر"),
                "🕒 تاريخ الإنشاء": contact.get("created_at", "غير متوفر"),
                "🕒 آخر تحديث": contact.get("updated_at", "غير متوفر"),
                "📩 عدد الإيميلات": contact.get("emails_count", "غير متوفر"),
                "📩 الإيميلات": ", ".join([email.get("email", "غير متوفر") for email in contact.get("emails", [])]) or "غير متوفر",
                "📑 الصفحة الأولى": data["data"]["contacts"].get("firage_url", "غير متوفر"),
                "📑 الصفحة الأخيرة": data["data"]["contacts"].get("lasge_url", "غير متوفر"),
                "🔍 رابط البحث": data["data"]["contacts"].get("th", "غير متوفر"),
                "🚨 Spam من المستخدم؟": "نعم" if contact.get("spammed_by_user", False) else "لا",
                "📊 عدد النتائج": data["data"]["contacts"].get("total", "غير متوفر"),
                "📢 حالة الإعلانات": "مفعلة" if data["data"]["auth_info"].get("enable_ads", False) else "غير مفعلة",
            }
            return {"success": True, "data": details}
        else:
            return {"error": f"❌ خطأ في البحث، كود الحالة: {response.status_code}"}
    except Exception as e:
        return {"error": f"⚠️ حدث خطأ أثناء البحث: {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        if not phone_number.startswith('+'):
            return render_template('index.html', 
                               error="يجب أن يبدأ الرقم بعلامة + (مثال: +201234567890)")
        
        result = search_number(phone_number)
        if 'error' in result:
            return render_template('index.html', error=result['error'])
        else:
            return render_template('index.html', 
                               phone_number=phone_number, 
                               result=result['data'])
    
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number or not phone_number.startswith('+'):
        return jsonify({"error": "يجب أن يبدأ الرقم بعلامة +"}), 400
    
    result = search_number(phone_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
