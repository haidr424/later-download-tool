import os
import time
import pyautogui

# إعداد خاصية الأمان لـ pyautogui
pyautogui.FAILSAFE = True

def read_settings():
    """دالة لقراءة الإعدادات من المستند النصي بأمان وتجنب مشاكل المسافات"""
    file_name = "مستند نصي جديد.txt"
    settings = {"loops": 1, "timeout": 40} # قيم افتراضية في حال حدوث خطأ
    
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if "التكرار" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            settings["loops"] = int(parts[1].strip())
                    elif "الانتظار" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            settings["timeout"] = int(parts[1].strip())
        except Exception as e:
            print(f"حدث خطأ أثناء قراءة ملف الإعدادات: {e}")
    else:
        print("ملف الإعدادات غير موجود، تم تطبيق الإعدادات الافتراضية.")
        
    return settings

def automate_download():
    config = read_settings()
    total_loops = config["loops"]
    timeout_limit = config["timeout"]
    
    print(f"⚙️ تم تحميل الإعدادات: التكرار ({total_loops}) | وقت الانتظار ({timeout_limit} ثانية).")
    print("🚀 بدء تشغيل الأداة تلقائياً ومراقبة الشاشة...")

    for i in range(total_loops):
        print(f"\n🔄 بدء الدورة رقم {i + 1} من أصل {total_loops}...")
        
        # 1. انتظار والنقر على زر "video_btn.png"
        print("🔍 بانتظار ظهور زر 'تحميل هذا الفيديو'...")
        start_time = time.time()
        video_clicked = False
        
        while time.time() - start_time < timeout_limit:
            try:
                # استخدام الاسم الإنجليزي الجديد لتجنب خطأ القراءة
                btn_pos = pyautogui.locateOnScreen('video_btn.png', confidence=0.8)
                if btn_pos is not None:
                    click_x, click_y = pyautogui.center(btn_pos)
                    pyautogui.click(click_x, click_y)
                    print("✅ تم النقر على زر 'تحميل هذا الفيديو'.")
                    video_clicked = True
                    break
            except Exception as e:
                pass
            time.sleep(0.5)
            
        if not video_clicked:
            print("⚠️ انتهى وقت الانتظار ولم يظهر زر التحميل.")
            continue

        # 2. انتظار ظهور نافذة IDM والنقر على "later_btn.png"
        print("🔍 بانتظار ظهور نافذة التحميل لتأكيد 'التحميل لاحقاً'...")
        later_clicked = False
        start_time = time.time()
        
        while time.time() - start_time < 15:
            try:
                later_pos = pyautogui.locateOnScreen('later_btn.png', confidence=0.8)
                if later_pos is not None:
                    later_x, later_y = pyautogui.center(later_pos)
                    pyautogui.click(later_x, later_y)
                    print("✅ تم النقر على زر 'التحميل لاحقاً' بنجاح.")
                    later_clicked = True
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if not later_clicked:
            print("⚠️ لم تظهر نافذة 'التحميل لاحقاً'.")
            
        time.sleep(1)

    print("\n🎉 اكتملت جميع العمليات بنجاح.")

if __name__ == "__main__":
    automate_download()
