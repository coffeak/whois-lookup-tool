import whois
import tkinter as tk
from tkinter import messagebox, scrolledtext, Menu

# Language dictionaries
LANGUAGES = {
    "en": {
        "title": "WHOIS Lookup Tool",
        "enter_domain": "Enter Domain Name:",
        "lookup_button": "WHOIS Lookup",
        "night_mode": "🌙 Night Mode",
        "day_mode": "☀️ Day Mode",
        "warning": "Warning",
        "empty_domain": "Please enter a domain name!",
        "error": "Error",
        "whois_error": "WHOIS lookup error: {error}",
        "about": "About",
        "developer": "Developer: www.coffeak.com",
        "menu_language": "Language",
        "menu_theme": "Theme",
        "menu_help": "Help",
        "no_data": "No data found.",
        "domain": "📌 Domain",
        "registrar": "🏢 Registrar",
        "whois_server": "🌐 WHOIS Server",
        "updated_date": "📅 Updated Date",
        "creation_date": "📆 Creation Date",
        "expiration_date": "⏳ Expiration Date",
        "name_servers": "🖧 Name Servers",
        "dnssec": "🔒 DNSSEC",
        "emails": "📨 Registered Emails",
        "org": "🏢 Organization",
        "status": "📌 Status"
    },
    "tr": {
        "title": "WHOIS Sorgu Aracı",
        "enter_domain": "Domain Adını Girin:",
        "lookup_button": "WHOIS Sorgula",
        "night_mode": "🌙 Gece Modu",
        "day_mode": "☀️ Gündüz Modu",
        "warning": "Uyarı",
        "empty_domain": "Lütfen bir domain adı girin!",
        "error": "Hata",
        "whois_error": "WHOIS sorgusunda hata oluştu: {error}",
        "about": "Hakkında",
        "developer": "Geliştirici: www.coffeak.com",
        "menu_language": "Dil",
        "menu_theme": "Tema",
        "menu_help": "Yardım",
        "no_data": "Veri bulunamadı.",
        "domain": "📌 Domain",
        "registrar": "🏢 Kayıt Şirketi",
        "whois_server": "🌐 WHOIS Sunucusu",
        "updated_date": "📅 Güncellenme Tarihi",
        "creation_date": "📆 Açılış Tarihi",
        "expiration_date": "⏳ Son Kullanma Tarihi",
        "name_servers": "🖧 Name Server'lar",
        "dnssec": "🔒 DNS SEC",
        "emails": "📨 Kayıtlı E-posta",
        "org": "🏢 Kayıtlı Organizasyon",
        "status": "📌 Durum"
    }
}

# Theme colors
THEMES = {
    "day": {
        "bg": "#ffffff", "fg": "#000000", "btn_bg": "#28a745", "btn_fg": "white",
        "text_bg": "#f4f4f4", "text_fg": "#000000", "highlight": "#e0e0e0"
    },
    "night": {
        "bg": "#121212", "fg": "#ffffff", "btn_bg": "#1e88e5", "btn_fg": "white",
        "text_bg": "#333333", "text_fg": "#ffffff", "highlight": "#424242"
    }
}

current_language = "en"  # Default language
current_theme = "day"  # Default theme


def change_language(lang):
    """Change the application language."""
    global current_language
    current_language = lang
    update_ui_text()


def toggle_theme():
    """Toggle between day and night theme."""
    global current_theme
    current_theme = "night" if current_theme == "day" else "day"
    apply_theme()


def apply_theme():
    """Apply the current theme to all widgets."""
    theme = THEMES[current_theme]
    root.configure(bg=theme["bg"])
    entry.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"],
                    highlightbackground=theme["highlight"], highlightcolor=theme["highlight"])
    lookup_button.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
    result_text.configure(bg=theme["text_bg"], fg=theme["text_fg"])
    theme_button.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])

    # Configure menu colors
    menu.configure(bg=theme["bg"], fg=theme["fg"], activebackground=theme["highlight"],
                   activeforeground=theme["fg"])

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])


def update_ui_text():
    """Update all UI text elements based on current language."""
    lang = LANGUAGES[current_language]
    root.title(lang["title"])
    domain_label.config(text=lang["enter_domain"])
    lookup_button.config(text=lang["lookup_button"])
    theme_button.config(text=lang["night_mode"] if current_theme == "day" else lang["day_mode"])

    # Update menu labels
    language_menu.entryconfig(0, label=f"{lang['menu_language']} (English)")
    language_menu.entryconfig(1, label=f"{lang['menu_language']} (Türkçe)")
    theme_menu.entryconfig(0,
                           label=f"{lang['menu_theme']} ({lang['day_mode'] if current_theme == 'night' else lang['night_mode']})")
    help_menu.entryconfig(0, label=lang["about"])


def show_about():
    """Show about information."""
    lang = LANGUAGES[current_language]
    messagebox.showinfo(lang["about"], lang["developer"])


def whois_lookup():
    """Perform WHOIS lookup and display results."""
    domain = entry.get().strip()
    lang = LANGUAGES[current_language]

    if not domain:
        messagebox.showwarning(lang["warning"], lang["empty_domain"])
        return

    try:
        domain_info = whois.whois(domain)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        info_list = []

        def add_item(title_key, data):
            """Helper function to add formatted data to results."""
            if data:
                if isinstance(data, list):
                    data = ", ".join(map(str, data))
                info_list.append(f"{lang[title_key]}: {data}")

        add_item("domain", domain_info.get("domain_name"))
        add_item("registrar", domain_info.get("registrar"))
        add_item("whois_server", domain_info.get("whois_server"))
        add_item("updated_date", domain_info.get("updated_date"))
        add_item("creation_date", domain_info.get("creation_date"))
        add_item("expiration_date", domain_info.get("expiration_date"))
        add_item("name_servers", domain_info.get("name_servers"))
        add_item("dnssec", domain_info.get("dnssec"))
        add_item("emails", domain_info.get("emails"))
        add_item("org", domain_info.get("org"))
        add_item("status", domain_info.get("status"))

        result_text.insert(tk.END, "\n".join(info_list) if info_list else lang["no_data"])
        result_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror(lang["error"], lang["whois_error"].format(error=e))


# Create main window
root = tk.Tk()
root.title(LANGUAGES[current_language]["title"])
root.geometry("700x500")  # Initial size
root.minsize(500, 400)  # Minimum size

# Create menu bar
menu = Menu(root, tearoff=0)
root.config(menu=menu)

# Language menu
language_menu = Menu(menu, tearoff=0)
menu.add_cascade(label=LANGUAGES[current_language]["menu_language"], menu=language_menu)
language_menu.add_command(label="English", command=lambda: change_language("en"))
language_menu.add_command(label="Türkçe", command=lambda: change_language("tr"))

# Theme menu
theme_menu = Menu(menu, tearoff=0)
menu.add_cascade(label=LANGUAGES[current_language]["menu_theme"], menu=theme_menu)
theme_menu.add_command(
    label=f"{LANGUAGES[current_language]['day_mode'] if current_theme == 'night' else LANGUAGES[current_language]['night_mode']}",
    command=toggle_theme
)

# Help menu
help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label=LANGUAGES[current_language]["menu_help"], menu=help_menu)
help_menu.add_command(label=LANGUAGES[current_language]["about"], command=show_about)

# Domain entry
domain_label = tk.Label(root, text=LANGUAGES[current_language]["enter_domain"], font=("Arial", 12))
domain_label.pack(pady=5, fill="x")

entry = tk.Entry(root, font=("Arial", 12), relief=tk.SOLID, borderwidth=1)
entry.pack(pady=5, padx=10, fill="x", expand=True)

# Lookup button
lookup_button = tk.Button(root, text=LANGUAGES[current_language]["lookup_button"],
                          font=("Arial", 12), command=whois_lookup)
lookup_button.pack(pady=5, padx=10, fill="x", expand=True)

# Results text area with scrollbar
result_text = scrolledtext.ScrolledText(root, font=("Consolas", 10), height=15,
                                        wrap=tk.WORD, relief=tk.SOLID, borderwidth=1)
result_text.pack(pady=10, padx=10, fill="both", expand=True)
result_text.config(state=tk.DISABLED)

# Theme toggle button
theme_button = tk.Button(root,
                         text=LANGUAGES[current_language]["night_mode"] if current_theme == "day" else
                         LANGUAGES[current_language]["day_mode"],
                         font=("Arial", 12), command=toggle_theme)
theme_button.pack(pady=5, padx=10, fill="x", expand=True)

# Apply initial theme and language
apply_theme()
update_ui_text()

# Start the main loop
root.mainloop()