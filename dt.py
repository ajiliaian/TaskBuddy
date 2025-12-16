import json
import os
from datetime import datetime, timedelta
import time
import threading
from enum import Enum
import random

class Priority(Enum):
    LOW = "Aşağı"
    MEDIUM = "Orta"
    HIGH = "Yüksək"
    URGENT = "Təcili"

class Subject(Enum):
    MATH = "Riyaziyyat"
    SCIENCE = "Elm"
    HISTORY = "Tarix"
    LANGUAGE = "Dil"
    LITERATURE = "Ədəbiyyat"
    PHYSICS = "Fizika"
    CHEMISTRY = "Kimya"
    BIOLOGY = "Biologiya"
    GEOGRAPHY = "Coğrafiya"
    ART = "İncəsənət"
    MUSIC = "Musiqi"
    SPORT = "İdman"
    OTHER = "Digər"

class HomeworkTracker:
    def __init__(self):
        self.data_file = "homework_data.json"
        self.schedule_file = "study_schedule.json"
        self.load_data()
        self.reminder_thread = None
        self.stop_reminders = False
        
    def load_data(self):
        """Məlumatları yüklə"""
       
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.homeworks = json.load(f)
        else:
            self.homeworks = []
            
       
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.schedule = json.load(f)
        else:
            self.schedule = self.create_default_schedule()
            self.save_schedule()
    
    def create_default_schedule(self):
        """Standart tədris cədvəli yarat"""
        return {
            "monday": [
                {"subject": "Riyaziyyat", "start": "16:00", "end": "17:30"},
                {"subject": "Fizika", "start": "18:00", "end": "19:00"}
            ],
            "tuesday": [
                {"subject": "Kimya", "start": "16:30", "end": "17:30"},
                {"subject": "Ədəbiyyat", "start": "18:00", "end": "19:00"}
            ],
            "wednesday": [
                {"subject": "Tarix", "start": "15:00", "end": "16:30"},
                {"subject": "Coğrafiya", "start": "17:00", "end": "18:00"}
            ],
            "thursday": [
                {"subject": "Biologiya", "start": "16:00", "end": "17:30"},
                {"subject": "Dil", "start": "18:00", "end": "19:00"}
            ],
            "friday": [
                {"subject": "Riyaziyyat", "start": "15:00", "end": "16:30"},
                {"subject": "Elm", "start": "17:00", "end": "18:00"}
            ],
            "saturday": [
                {"subject": "Təkrar", "start": "10:00", "end": "12:00"}
            ],
            "sunday": [
                {"subject": "Dinclik", "start": "00:00", "end": "23:59"}
            ]
        }
    
    def save_data(self):
        """Ev tapşırıqlarını saxla"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.homeworks, f, ensure_ascii=False, indent=2)
    
    def save_schedule(self):
        """Tədris cədvəlini saxla"""
        with open(self.schedule_file, 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=2)
    
    def add_homework(self):
        """Yeni ev tapşırığı əlavə et"""
        print("\n" + "="*50)
        print("YENİ EV TAPŞIRIĞI ƏLAVƏ ET")
        print("="*50)
        
        title = input("Tapşırığın adı: ").strip()
        
        print("\nFənn seçin:")
        for i, subject in enumerate(Subject, 1):
            print(f"{i}. {subject.value}")
        subject_choice = int(input("Seçim (1-13): ")) - 1
        subject = list(Subject)[subject_choice].value
        
        description = input("Ətraflı təsvir: ").strip()
        
        deadline = input("Son tarix (GG.AA.İLİL): ").strip()
        
        print("\nPrioritet:")
        for i, priority in enumerate(Priority, 1):
            print(f"{i}. {priority.value}")
        priority_choice = int(input("Seçim (1-4): ")) - 1
        priority = list(Priority)[priority_choice].value
        
        estimated_time = input("Təxmini vaxt (saat): ").strip()
        
        homework = {
            "id": len(self.homeworks) + 1,
            "title": title,
            "subject": subject,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "estimated_time": estimated_time,
            "status": "Gözləmədə",
            "created_date": datetime.now().strftime("%d.%m.%Y"),
            "completed_date": None,
            "notes": []
        }
        
        self.homeworks.append(homework)
        self.save_data()
        
        print(f"\n✅ '{title}' tapşırığı uğurla əlavə edildi!")
        
       
        self.schedule_homework(homework)
    
    def schedule_homework(self, homework):
        """Tapşırığı tədris cədvəlinə əlavə et"""
        print("\n📅 TƏDRİS CƏDVƏLİNƏ ƏLAVƏ ET")
        print("-"*40)
        
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        print("Həftənin günləri:")
        for i, day in enumerate(["Bazar ertəsi", "Çərşənbə axşamı", "Çərşənbə", 
                                "Cümə axşamı", "Cümə", "Şənbə", "Bazar"], 1):
            print(f"{i}. {day}")
        
        day_choice = int(input("Gün seçin (1-7): ")) - 1
        selected_day = days[day_choice]
        
        start_time = input("Başlama vaxtı (saat:dəqiqə, məs: 16:30): ").strip()
        end_time = input("Bitmə vaxtı (saat:dəqiqə): ").strip()
        
       
        if selected_day not in self.schedule:
            self.schedule[selected_day] = []
        
        session = {
            "subject": homework["subject"],
            "homework_id": homework["id"],
            "homework_title": homework["title"],
            "start": start_time,
            "end": end_time,
            "completed": False
        }
        
        self.schedule[selected_day].append(session)
        self.save_schedule()
        
        print(f"\n✅ Tapşırıq {selected_day} günü {start_time}-{end_time} vaxtına planlaşdırıldı!")
    
    def view_homeworks(self, filter_type="all"):
        """Tapşırıqları göstər"""
        print("\n" + "="*60)
        print("EV TAPŞIRIQLARI SİYAHISI")
        print("="*60)
        
        if not self.homeworks:
            print("❌ Heç bir tapşırıq tapılmadı.")
            return
        
        filtered_homeworks = self.homeworks
        
        if filter_type == "pending":
            filtered_homeworks = [h for h in self.homeworks if h["status"] == "Gözləmədə"]
            print("📋 GÖZLƏMƏDƏ OLANLAR")
        elif filter_type == "completed":
            filtered_homeworks = [h for h in self.homeworks if h["status"] == "Tamamlandı"]
            print("✅ TAMAMLANMIŞLAR")
        elif filter_type == "urgent":
            filtered_homeworks = [h for h in self.homeworks if h["priority"] == "Təcili"]
            print("⚠️ TƏCİLİ OLANLAR")
        else:
            print("📚 BÜTÜN TAPŞIRIQLAR")
        
        print("-"*60)
        
        for hw in filtered_homeworks:
            status_icon = "✅" if hw["status"] == "Tamamlandı" else "⏳"
            priority_icon = "⚠️" if hw["priority"] == "Təcili" else "🔄"
            
            print(f"\n{status_icon} ID: {hw['id']}")
            print(f"   📌 {hw['title']}")
            print(f"   📚 Fənn: {hw['subject']}")
            print(f"   ⏰ Son tarix: {hw['deadline']}")
            print(f"   {priority_icon} Prioritet: {hw['priority']}")
            print(f"   🕒 Təxmini vaxt: {hw['estimated_time']} saat")
            print(f"   📝 Status: {hw['status']}")
            
            if hw['notes']:
                print(f"   📎 Qeydlər: {len(hw['notes'])} qeyd")
    
    def mark_completed(self):
        """Tapşırığı tamamlandı kimi qeyd et"""
        self.view_homeworks("pending")
        
        if not any(hw["status"] == "Gözləmədə" for hw in self.homeworks):
            return
        
        hw_id = int(input("\nTamamlanan tapşırığın ID-si: "))
        
        for hw in self.homeworks:
            if hw["id"] == hw_id:
                hw["status"] = "Tamamlandı"
                hw["completed_date"] = datetime.now().strftime("%d.%m.%Y")
                
                
                for day in self.schedule.values():
                    for session in day:
                        if session.get("homework_id") == hw_id:
                            session["completed"] = True
                
                print(f"\n✅ '{hw['title']}' tapşırığı tamamlandı kimi qeyd edildi!")
                self.save_data()
                self.save_schedule()
                return
        
        print("❌ Tapşırıq tapılmadı!")
    
    def view_schedule(self):
        """Tədris cədvəlini göstər"""
        print("\n" + "="*60)
        print("HƏFTƏLİK TƏDRİS CƏDVƏLİ")
        print("="*60)
        
        days_translation = {
            "monday": "Bazar ertəsi",
            "tuesday": "Çərşənbə axşamı",
            "wednesday": "Çərşənbə",
            "thursday": "Cümə axşamı",
            "friday": "Cümə",
            "saturday": "Şənbə",
            "sunday": "Bazar"
        }
        
        for day_en, day_tr in days_translation.items():
            print(f"\n📅 {day_tr.upper()}:")
            print("-"*40)
            
            if day_en in self.schedule and self.schedule[day_en]:
                sessions = sorted(self.schedule[day_en], key=lambda x: x["start"])
                
                for session in sessions:
                    status_icon = "✅" if session.get("completed", False) else "⏳"
                    subject_icon = self.get_subject_icon(session["subject"])
                    
                    print(f"   {status_icon} {subject_icon} {session['start']} - {session['end']}")
                    print(f"      Fənn: {session['subject']}")
                    
                    if "homework_title" in session:
                        print(f"      Tapşırıq: {session['homework_title']}")
                    
                    if session.get("completed", False):
                        print(f"      🎉 Tamamlandı!")
            else:
                print("   🎉 Bu gün tədbir yoxdur!")
    
    def get_subject_icon(self, subject):
        """Fənnə uyğun ikon qaytar"""
        icons = {
            "Riyaziyyat": "🔢",
            "Fizika": "⚛️",
            "Kimya": "🧪",
            "Biologiya": "🧬",
            "Tarix": "📜",
            "Coğrafiya": "🌍",
            "Ədəbiyyat": "📖",
            "Dil": "🔤",
            "Elm": "🔬",
            "İncəsənət": "🎨",
            "Musiqi": "🎵",
            "İdman": "⚽",
            "Digər": "📝"
        }
        return icons.get(subject, "📚")
    
    def edit_schedule(self):
        """Tədris cədvəlini redaktə et"""
        self.view_schedule()
        
        days = list(self.schedule.keys())
        print("\nGünlər:")
        for i, day in enumerate(days, 1):
            print(f"{i}. {day}")
        
        day_choice = int(input("\nRedaktə etmək istədiyiniz günün nömrəsi: ")) - 1
        selected_day = days[day_choice]
        
        print(f"\n{selected_day} gününün sessiyaları:")
        for i, session in enumerate(self.schedule[selected_day], 1):
            print(f"{i}. {session['start']} - {session['end']}: {session['subject']}")
        
        print("\n1. Yeni sessiya əlavə et")
        print("2. Sessiya sil")
        print("3. Sessiyanı tamamlandı kimi qeyd et")
        
        choice = input("Seçim: ")
        
        if choice == "1":
            subject = input("Fənn: ").strip()
            start = input("Başlama vaxtı: ").strip()
            end = input("Bitmə vaxtı: ").strip()
            
            self.schedule[selected_day].append({
                "subject": subject,
                "start": start,
                "end": end,
                "completed": False
            })
            print("✅ Yeni sessiya əlavə edildi!")
            
        elif choice == "2":
            session_idx = int(input("Silinəcək sessiyanın nömrəsi: ")) - 1
            if 0 <= session_idx < len(self.schedule[selected_day]):
                removed = self.schedule[selected_day].pop(session_idx)
                print(f"✅ '{removed['subject']}' sessiyası silindi!")
        
        elif choice == "3":
            session_idx = int(input("Tamamlanan sessiyanın nömrəsi: ")) - 1
            if 0 <= session_idx < len(self.schedule[selected_day]):
                self.schedule[selected_day][session_idx]["completed"] = True
                print("✅ Sessiya tamamlandı kimi qeyd edildi!")
        
        self.save_schedule()
    
    def start_reminders(self):
        """Xatırlatmaları başlat"""
        self.stop_reminders = False
        self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()
        print("\n🔔 Xatırlatmalar aktiv edildi!")
    
    def reminder_loop(self):
        """Xatırlatma dövrü"""
        while not self.stop_reminders:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.strftime("%A").lower()
            
            
            day_translation = {
                "monday": "monday",
                "tuesday": "tuesday", 
                "wednesday": "wednesday",
                "thursday": "thursday",
                "friday": "friday",
                "saturday": "saturday",
                "sunday": "sunday"
            }
            
            
            if current_day in day_translation and day_translation[current_day] in self.schedule:
                sessions = self.schedule[day_translation[current_day]]
                
                for session in sessions:
                    if session["start"] == current_time and not session.get("notified", False):
                        print(f"\n" + "!"*60)
                        print(f"🔔 XATIRLATMA!")
                        print(f"Vaxtıdır: {session['subject']}")
                        if "homework_title" in session:
                            print(f"Tapşırıq: {session['homework_title']}")
                        print(f"Vaxt: {session['start']} - {session['end']}")
                        print("!"*60 + "\n")
                        session["notified"] = True
            
           
            time.sleep(60)
    
    def stop_reminder_service(self):
        """Xatırlatmaları dayandır"""
        self.stop_reminders = True
        if self.reminder_thread:
            self.reminder_thread.join()
        print("\n🔕 Xatırlatmalar dayandırıldı!")
    
    def progress_report(self):
        """Tərəqqi hesabatı"""
        print("\n" + "="*60)
        print("📊 TƏRƏQQİ HESABATI")
        print("="*60)
        
        total_homeworks = len(self.homeworks)
        completed_homeworks = len([h for h in self.homeworks if h["status"] == "Tamamlandı"])
        
        if total_homeworks > 0:
            completion_rate = (completed_homeworks / total_homeworks) * 100
            print(f"\n📈 Ümumi tamamlama: {completion_rate:.1f}%")
            print(f"   ✅ Tamamlanan: {completed_homeworks}")
            print(f"   ⏳ Gözləmədə: {total_homeworks - completed_homeworks}")
            print(f"   📚 Ümumi: {total_homeworks}")
        
        
        print("\n📚 FƏNNLƏRƏ GÖRƏ:")
        print("-"*40)
        
        subjects = {}
        for hw in self.homeworks:
            subj = hw["subject"]
            if subj not in subjects:
                subjects[subj] = {"total": 0, "completed": 0}
            subjects[subj]["total"] += 1
            if hw["status"] == "Tamamlandı":
                subjects[subj]["completed"] += 1
        
        for subj, stats in subjects.items():
            rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            icon = self.get_subject_icon(subj)
            print(f"   {icon} {subj}: {stats['completed']}/{stats['total']} ({rate:.1f}%)")
        
       
        print("\n⚠️ PRIORİTETLƏRƏ GÖRƏ:")
        print("-"*40)
        
        priorities = {}
        for hw in self.homeworks:
            prio = hw["priority"]
            if prio not in priorities:
                priorities[prio] = {"total": 0, "completed": 0}
            priorities[prio]["total"] += 1
            if hw["status"] == "Tamamlandı":
                priorities[prio]["completed"] += 1
        
        for prio, stats in priorities.items():
            rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"   {prio}: {stats['completed']}/{stats['total']} ({rate:.1f}%)")
        
        
        print("\n💪 MOTİVASİYA:")
        print("-"*40)
        messages = [
            "Hər gün kiçik addımlarla böyük nəticələr əldə edə bilərsən!",
            "Əzmkarlıq uğurun açarıdır! Davam et!",
            "Bugün etdiyin hər iş sabahın üçün investisiyadır!",
            "Öyrənmək ən gözəl səyahətdir!",
            "Hər çətinlik səni daha güclü edir!"
        ]
        print(f"   {random.choice(messages)}")
    
    def quick_check_in(self):
        """Cari statusu yoxla"""
        print("\n" + "="*60)
        print("🔍 CARI STATUS")
        print("="*60)
        
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A").lower()
        
        print(f"\n📅 Bugün: {now.strftime('%d.%m.%Y')}")
        print(f"⏰ Cari vaxt: {current_time}")
        
       
        today_homeworks = [hw for hw in self.homeworks 
                          if hw["status"] == "Gözləmədə" and hw["deadline"] == now.strftime("%d.%m.%Y")]
        
        if today_homeworks:
            print("\n⚠️ BUGÜN TAMAMLANMALI TAPŞIRIQLAR:")
            for hw in today_homeworks:
                print(f"   • {hw['title']} ({hw['subject']}) - {hw['priority']} prioritet")
        else:
            print("\n✅ Bugün son tarixi olan tapşırıq yoxdur!")
        
        
        day_translation = {
            "monday": "monday",
            "tuesday": "tuesday",
            "wednesday": "wednesday", 
            "thursday": "thursday",
            "friday": "friday",
            "saturday": "saturday",
            "sunday": "sunday"
        }
        
        if current_day in day_translation and day_translation[current_day] in self.schedule:
            sessions = self.schedule[day_translation[current_day]]
            current_sessions = [s for s in sessions if s["start"] <= current_time <= s["end"]]
            
            if current_sessions:
                print("\n🎯 HAL-HAZIRDA DAVAM EDƏN:")
                for session in current_sessions:
                    status = "✅ Tamamlandı" if session.get("completed") else "⏳ Davam edir"
                    print(f"   • {session['subject']} ({session['start']}-{session['end']}) - {status}")
            else:
                print("\n🕒 Hal-hazırda aktiv sessiya yoxdur")
                
              
                future_sessions = [s for s in sessions if s["start"] > current_time]
                if future_sessions:
                    next_session = min(future_sessions, key=lambda x: x["start"])
                    print(f"\n⏭️ NÖVBƏTİ SESSİYA: {next_session['start']} - {next_session['subject']}")
    
    def run(self):
        """Əsas proqram dövrü"""
        print("\n" + "="*60)
        print("🎓 EV TAPŞIRIĞI İDARƏ ETMƏ SİSTEMİ")
        print("="*60)
        
        
        self.start_reminders()
        
        try:
            while True:
                print("\n" + "="*60)
                print("ƏSAS MENYU")
                print("="*60)
                print("1. 📝 Yeni ev tapşırığı əlavə et")
                print("2. 📋 Tapşırıqları göstər")
                print("3. ✅ Tapşırığı tamamlandı kimi qeyd et")
                print("4. 📅 Tədris cədvəlini göstər")
                print("5. ✏️ Tədris cədvəlini redaktə et")
                print("6. 🔍 Cari statusu yoxla")
                print("7. 📊 Tərəqqi hesabatı")
                print("8. ⚙️ Xatırlatmaları idarə et")
                print("9. 💾 Saxla və çıx")
                print("="*60)
                
                choice = input("Seçiminiz (1-9): ").strip()
                
                if choice == "1":
                    self.add_homework()
                elif choice == "2":
                    print("\n1. Bütün tapşırıqlar")
                    print("2. Gözləmədə olanlar")
                    print("3. Tamamlanmışlar")
                    print("4. Təcili olanlar")
                    filter_choice = input("Seçim: ")
                    
                    if filter_choice == "1":
                        self.view_homeworks("all")
                    elif filter_choice == "2":
                        self.view_homeworks("pending")
                    elif filter_choice == "3":
                        self.view_homeworks("completed")
                    elif filter_choice == "4":
                        self.view_homeworks("urgent")
                elif choice == "3":
                    self.mark_completed()
                elif choice == "4":
                    self.view_schedule()
                elif choice == "5":
                    self.edit_schedule()
                elif choice == "6":
                    self.quick_check_in()
                elif choice == "7":
                    self.progress_report()
                elif choice == "8":
                    print("\n1. Xatırlatmaları aktiv et")
                    print("2. Xatırlatmaları dayandır")
                    reminder_choice = input("Seçim: ")
                    
                    if reminder_choice == "1":
                        self.start_reminders()
                    elif reminder_choice == "2":
                        self.stop_reminder_service()
                elif choice == "9":
                    self.save_data()
                    self.save_schedule()
                    self.stop_reminder_service()
                    print("\n✨ Məlumatlar saxlanıldı. Sağ olun!")
                    break
                else:
                    print("\n❌ Yanlış seçim!")
                
                input("\n↵ Davam etmək üçün Enter düyməsini basın...")
                
        except KeyboardInterrupt:
            self.stop_reminder_service()
            print("\n\n👋 Proqramdan çıxılır...")


if __name__ == "__main__":
    app = HomeworkTracker()
    app.run()
