import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import main as m
import pandas as pd

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MultiCrawler")
        self.root.geometry("700x500")  # Set the window size
        
        self.file_path = None
        self.df = None

        # Styling options
        self.entry_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")
        self.button_bg = "#4CAF50"
        self.button_fg = "#FFFFFF"
        self.button_bd = 2
        self.path_label = tk.Label(self.root, text="[TEST] Công cụ tìm kiếm Google, Lazada", font=self.entry_font)
        self.path_label.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        self.entry = tk.Entry(self.root, font=self.entry_font, bd=2, relief="solid")
        self.entry.insert(0, "Excel Path")
        self.entry.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        
        self.divider = ttk.Separator(self.root, orient='horizontal')
        self.divider.pack(fill='x', pady=10, padx=20)
        self.file_button = tk.Button(self.root, text="Open File", command=self.open_file_dialog, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.file_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width

        self.lazada_button = tk.Button(self.root, text="crawl lazada", command=self.crawl_lazada, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.lazada_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width

        self.google_button = tk.Button(self.root, text="crawl google", command=self.crawl_google, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.google_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.show_res_button = tk.Button(self.root, text="show crawl res", command=self.show_res, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.show_res_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        # Create a frame for the table
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Define columns
        self.columns = ("Barcode", "Tên MH", "ĐVT", "Loại sản phẩm")

        # Create Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show='headings')

        # Define headings
        for col in self.columns:
            self.tree.heading(col, text=col)

        # Add Treeview to the frame
        self.tree.pack(fill='both', expand=True)
        # Add a label for "Sản phẩm đã crawl"
        self.crawl_label = tk.Label(self.root, text="Sản phẩm đã crawl", font=("Helvetica", 14, "bold"))
        self.crawl_label.pack(pady=10, padx=20, anchor='w')
        # Create a dropdown menu
        self.dropdown_var = tk.StringVar(self.root)
        self.dropdown_var.set("Không có sản phẩm nào")  # Default value
        self.search_label = tk.Label(self.root, text="Nhập từ khóa để tìm kiếm", font=self.entry_font)
        self.search_label.pack(pady=0, padx=20, anchor='w')
        self.searchQuery = tk.Entry(self.root, font=self.entry_font, bd=2, relief="solid")
        self.searchQuery.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        self.search_button = tk.Button(self.root, text="search", command=self.search, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.search_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.dropdown_menu = tk.OptionMenu(self.root, self.dropdown_var, "Không có sản phẩm nào")
        self.dropdown_menu.config(font=self.entry_font)
        self.dropdown_menu.pack(pady=5, padx=5)  # Add padding and stretch to fill width
        # Create a frame for the results table
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Define columns for the results table
        self.results_columns = ("prod_name", "prod_price", "prod_link", "fuzz_partial_ratio", "fuzz_ratio")

        # Create Treeview for the results
        self.results_tree = ttk.Treeview(self.results_frame, columns=self.results_columns, show='headings')

        # Define headings for the results table
        for col in self.results_columns:
            self.results_tree.heading(col, text=col)

        # Add Treeview to the results frame
        self.results_tree.pack(fill='both', expand=True)
        
    def search(self):
        query = self.searchQuery.get()
        selected_product = self.dropdown_var.get()
        df = self.resDf.parse(selected_product)
        print(df)
        print(f"Selected product from dropdown: {selected_product}")
        print(query)    
    def show_res(self):
        self.resDf = pd.ExcelFile('res.xlsx')
        print(self.resDf.sheet_names)
        self.dropdown_menu['menu'].delete(0, 'end')
        self.update_res_table(self.resDf.sheet_names[1])
        for product in self.resDf.sheet_names:
            self.dropdown_menu['menu'].add_command(label=product, command=tk._setit(self.dropdown_var, product, lambda e: self.update_res_table(e)))
        self.dropdown_var.set(self.resDf.sheet_names[1])
    def update_res_table(self, val):
        f = self.resDf.parse(val)
        self.results_tree.delete(*self.results_tree.get_children())
        for index, row in f.iterrows():
            self.results_tree.insert("", "end", values=(row["prod_name"], row["prod_price"], row["prod_link"], row["fuzz_partial_ratio"], row["fuzz_ratio"]))
    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            print(f"Selected file: {self.file_path}")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.file_path)
            self.df = pd.read_excel(rf"{self.file_path}")
            # Clear the existing data in the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data into the treeview
            for index, row in self.df.iterrows():
                self.tree.insert("", "end", values=(row["Barcode"], row["Tên MH"], row["ĐVT"], row["Loại sản phẩm"]))

    def crawl_google(self):
        crawler = m.GoogleScraper(file_path=self.file_path)
        crawler.crawl()
        tk.messagebox.showinfo("Crawling Complete", "The Google crawl has completed successfully.")
        self.show_res()
    def crawl_lazada(self):
        crawler = m.LazadaScraper(file_path=self.file_path)
        crawler.crawl()
        tk.messagebox.showinfo("Crawling Complete", "The Lazada crawl has completed successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
