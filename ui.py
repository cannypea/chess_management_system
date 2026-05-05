import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as tb 
from ttkbootstrap.constants import *
import random
import os
import re # Professional Addition: Regex for validation
from datetime import datetime

# --- Internal Imports ---
from models import Player, Tournament, Club, Match, Round
from pairing import swiss_pair
from storage import save, load, list_tournaments, save_clubs, load_clubs
from report import generate_report
from rating import update_elo
from service import TournamentService

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("♟ Castle Chess Management System")
        self.root.geometry("1300x850")

        # --- THEME SETUP ---
        self.style = tb.Style(theme="superhero")

        # --- DATA STATE ---
        self.service = TournamentService()
        self.clubs = []
        self.active_club = None
        self.tournament = None
        
        self.initialize_data()
        self.setup_ui()
        self.refresh_ui()

    def initialize_data(self):
        raw_clubs = load_clubs()
        self.clubs = []
        for c_data in raw_clubs:
            club = Club(c_data["name"])
            for p_data in c_data.get("players", []):
                club.players.append(Player.from_dict(p_data))
            self.clubs.append(club)
        
        if not self.clubs:
            self.clubs.append(Club("Castle Chess Default"))
        
        self.active_club = self.clubs[0]

    def setup_ui(self):
        """Main UI Layout Construction."""
        container = tb.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        # --- LEFT SIDEBAR (Clubs) ---
        sidebar = tb.Frame(container, width=300)
        sidebar.pack(side="left", fill="y", padx=(0, 20))

        tb.Label(sidebar, text="PARTICIPATING CLUBS", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w", pady=(0, 10))
        
        # FEATURE PRESERVATION: Custom Listbox styling
        self.club_listbox = tk.Listbox(
            sidebar, 
            font=("Segoe UI", 11), 
            bg="#2b3e50", 
            fg="white",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#4e5d6c",
            selectbackground="#df691a",
            activestyle='none'
        )
        self.club_listbox.pack(fill="both", expand=True, pady=(0, 10))
        self.club_listbox.bind("<<ListboxSelect>>", self.on_club_select)
        
        club_btn_frame = tb.Frame(sidebar)
        club_btn_frame.pack(fill="x")
        tb.Button(club_btn_frame, text="+ Club", bootstyle="outline-success", command=self.create_club).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tb.Button(club_btn_frame, text="Delete", bootstyle="outline-danger", command=self.delete_club).pack(side="left", fill="x", expand=True)

        # --- CENTER CONTENT ---
        center = tb.Frame(container)
        center.pack(side="left", fill="both", expand=True)

        header_frame = tb.Frame(center)
        header_frame.pack(fill="x", pady=(0, 20))
        tb.Label(header_frame, text="Tournament Standings", font=("Helvetica", 24, "bold")).pack(side="left")
        
        # FEATURE PRESERVATION: Custom Treeview columns/widths
        cols = ("ID", "Name", "Club", "Score", "Rating")
        self.tree = tb.Treeview(center, columns=cols, show="headings", bootstyle="primary")
        
        widths = {"ID": 100, "Name": 200, "Club": 150, "Score": 80, "Rating": 80}
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=widths.get(col, 100))
        self.tree.pack(fill="both", expand=True)

        # --- DIAGNOSTIC AREA ---
        self.diag_container = tb.Frame(center, bootstyle="secondary", padding=1)
        self.diag_container.pack(fill="x", pady=(20, 0))
        
        self.diag_inner = tb.Frame(self.diag_container, padding=10)
        self.diag_inner.pack(fill="both")
        
        tb.Label(self.diag_inner, text="SYSTEM DIAGNOSTIC", font=("Helvetica", 8, "bold"), bootstyle="info").pack(anchor="w")
        
        self.test_console = tk.Text(
            self.diag_inner, 
            height=7, 
            font=("Consolas", 10), 
            bg="#1a252f", 
            fg="#95a5a6", 
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.test_console.pack(fill="x", pady=(5, 0))
        self.test_console.tag_config("pass", foreground="#2ecc71", font=("Consolas", 10, "bold"))

        # --- RIGHT SIDEBAR (Actions) ---
        actions = tb.Frame(container, width=220, padding=(20, 0, 0, 0))
        actions.pack(side="right", fill="y")

        tb.Label(actions, text="OPERATIONS", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w", pady=(0, 15))

        self.btn(actions, "New Tournament", "primary", self.new_tournament)
        self.btn(actions, "Register Player", "success", self.add_player)
        self.btn(actions, "Delete Player", "danger-outline", self.delete_player)
        
        tb.Separator(actions, bootstyle="secondary").pack(fill="x", pady=20)
        
        self.btn(actions, "Next Round (Manual)", "info", self.next_round)
        self.btn(actions, "Simulate Tournament", "warning", self.run_simulation)
        self.btn(actions, "Run Diagnostic", "secondary", self.run_smoke_test)
        
        tb.Separator(actions, bootstyle="secondary").pack(fill="x", pady=20)
        
        self.btn(actions, "Export PDF Report", "light", self.report)

    def btn(self, parent, text, style, cmd):
        btn = tb.Button(parent, text=text, bootstyle=style, command=cmd, width=20)
        btn.pack(fill="x", pady=5)
        return btn

    # --- LOGIC METHODS ---

    def create_club(self):
        name = simpledialog.askstring("Club", "Enter Club Name:")
        if name:
            self.clubs.append(Club(name))
            save_clubs(self.clubs)
            self.refresh_ui()

    def delete_club(self):
        if self.active_club and messagebox.askyesno("Confirm", f"Delete {self.active_club.name}?"):
            self.clubs.remove(self.active_club)
            self.active_club = self.clubs[0] if self.clubs else None
            save_clubs(self.clubs)
            self.refresh_ui()

    def add_player(self):
        if not self.active_club:
            messagebox.showwarning("Club Needed", "Please select or create a club first.")
            return
        name = simpledialog.askstring("Player", "Full Name:")
        if not name or len(name.strip()) < 2: return # Protection

        # GOLD STANDARD UPGRADE: Regex Validation
        cid = simpledialog.askstring("Player", "Chess ID (AB12345):")
        if not cid or not re.match(r"^[A-Z]{2}\d{5}$", cid):
            messagebox.showerror("Validation Error", "ID must be 2 Uppercase letters + 5 digits (e.g. XY12345)")
            return

        p = Player(name=name, email=f"{name.replace(' ','').lower()}@chess.com", chess_id=cid, birthdate="1990-01-01")
        self.active_club.players.append(p)
        if self.tournament: self.tournament.add_player(p)
        save_clubs(self.clubs)
        self.refresh_ui()

    def delete_player(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a player from the table first.")
            return
        
        cid = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Remove player {cid}?"):
            self.active_club.players = [p for p in self.active_club.players if p.chess_id != cid]
            if self.tournament:
                self.tournament.players = [p for p in self.tournament.players if p.chess_id != cid]
            save_clubs(self.clubs)
            self.refresh_ui()

    def run_simulation(self):
        if not self.active_club or len(self.active_club.players) < 4:
            messagebox.showinfo("Sim", "Add at least 4 players to the club first.")
            return
        
        self.tournament = self.service.create_tournament("Auto-Sim", "Virtual Venue", "2026-05-01", "2026-05-02")
        self.tournament.players = self.active_club.players[:]
        
        for r in range(1, 5):
            pairs = swiss_pair(self.tournament.players, r)
            rnd = Round(f"Round {r}")
            for p1, p2 in pairs:
                res = random.choice([1, 0, 0.5])
                m = Match(p1, p2)
                m.set_result(res, 1-res if res != 0.5 else 0.5)
                update_elo(p1, p2, m.s1, m.s2)
                rnd.matches.append(m)
            self.tournament.rounds.append(rnd)
        
        save(self.tournament.name, self.tournament.to_dict())
        self.refresh_ui()
        messagebox.showinfo("Success", "4-Round Simulation Complete!")

    def run_smoke_test(self):
        try:
            from test_smoke import run_dashboard_tests
            self.test_console.delete("1.0", tk.END)
            self.test_console.insert(tk.END, "🚀 Initializing Full System Diagnostic...\n")
            
            test_gen = run_dashboard_tests()

            def process_test_step():
                try:
                    result = next(test_gen)
                    self.test_console.insert(tk.END, f"> {result}\n")
                    if "PASSED" in result:
                        idx = self.test_console.search("PASSED", "end-2l", "end")
                        if idx:
                            self.test_console.tag_add("pass", idx, f"{idx} + 6c")
                    self.test_console.see(tk.END)
                    self.root.after(400, process_test_step)
                except StopIteration:
                    self.test_console.insert(tk.END, "✅ Smoke Test Complete.\n")
                except Exception as e:
                    self.test_console.insert(tk.END, f"❌ Error during test: {e}\n")

            process_test_step()
        except (ImportError, AttributeError):
            messagebox.showerror("Error", "test_smoke.py with run_dashboard_tests() not found.")

    def refresh_ui(self):
        self.club_listbox.delete(0, tk.END)
        for c in self.clubs:
            self.club_listbox.insert(tk.END, c.name)

        for item in self.tree.get_children(): self.tree.delete(item)
        
        players_to_show = self.tournament.standings() if self.tournament else self.active_club.players
        for p in players_to_show:
            self.tree.insert("", "end", values=(p.chess_id, p.name, self.active_club.name, p.score, round(p.rating, 1)))

    def on_club_select(self, event):
        idx = self.club_listbox.curselection()
        if idx:
            self.active_club = self.clubs[idx[0]]
            self.refresh_ui()

    def new_tournament(self):
        if not self.active_club or not self.active_club.players:
            messagebox.showwarning("Warning", "Create a club with players first.")
            return
        self.tournament = self.service.create_tournament("New Event", "Main Hall", "2026-05-04", "2026-05-05")
        self.tournament.players = self.active_club.players[:]
        self.refresh_ui()

    # GOLD STANDARD UPGRADE: Manual Result Entry Dialog
    def next_round(self):
        if not self.tournament: return
        r_num = len(self.tournament.rounds) + 1
        pairs = swiss_pair(self.tournament.players, r_num)
        rnd = Round(f"Round {r_num}")
        
        for p1, p2 in pairs:
            # Replaces auto-win logic with a choice
            msg = f"{p1.name} vs {p2.name}\n\nDid {p1.name} win?\n(Yes = P1 wins, No = P2 wins, Cancel = Draw)"
            choice = messagebox.askquestion(f"Result Entry - {rnd.name}", msg, type=messagebox.YESNOCANCEL)
            
            m = Match(p1, p2)
            if choice == 'yes':
                m.set_result(1, 0)
            elif choice == 'no':
                m.set_result(0, 1)
            else:
                m.set_result(0.5, 0.5)
            
            update_elo(p1, p2, m.s1, m.s2)
            rnd.matches.append(m)
            
        self.tournament.rounds.append(rnd)
        self.refresh_ui()
        messagebox.showinfo("Round Finished", f"{rnd.name} results recorded.")

    def report(self):
        if self.tournament:
            os.makedirs("data/reports", exist_ok=True)
            path = f"data/reports/{self.tournament.name}.pdf"
            generate_report(self.tournament, path)
            messagebox.showinfo("Report", f"PDF Generated at {path}")
        else:
            messagebox.showwarning("No Tournament", "Start or simulate a tournament first.")

# GOLD STANDARD UPGRADE: Global Crash Logging
if __name__ == "__main__":
    try:
        root = tb.Window(themename="superhero")
        app = App(root)
        root.mainloop()
    except Exception as e:
        with open("crash_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] CRITICAL ERROR: {e}\n")
        print(f"The app encountered an error. Logged to crash_log.txt.")