import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import scraper as m
import pandas as pd
import webbrowser
import requests
from tkinter import filedialog, messagebox
class SimpleGUI:
    def __init__(self, root):
        self.resDf = None
        self.root = root
        self.root.title("MultiCrawler")
        # Add an icon to the window
        self.root.state('zoomed')
        img = tk.Image("photo", file="icon.png")
        self.root.iconphoto(True, img)
        self.file_path = None
        self.df = None

        # Styling options
        self.entry_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")
        self.button_bg = "#C6D6FF"
        self.button_fg = "#000000"
        self.button_bd = 2
        self.path_label = tk.Label(self.root, text="[TEST] Công cụ tìm kiếm Google, Lazada", font=self.entry_font)
        self.path_label.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        # Create a frame for the left part of the UI
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Create a frame for the right part of the UI
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        self.input_label = tk.Label(self.left_frame, text="Sản phẩm đầu vào", font=("Helvetica", 14, "bold"))
        self.input_label.pack(pady=10, padx=20, anchor='w')
        # Add widgets to the left frame
        self.entry = tk.Entry(self.left_frame, font=self.entry_font, bd=2, relief="solid")
        self.entry.insert(0, "Excel Path")
        self.entry.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        
        self.divider = ttk.Separator(self.left_frame, orient='horizontal')
        self.divider.pack(fill='x', pady=10, padx=20)
        self.file_button = tk.Button(self.left_frame, text="Open File", command=self.open_file_dialog, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.file_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width

        self.lazada_button = tk.Button(self.left_frame, text="crawl lazada", command=self.crawl_lazada, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.lazada_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width

        self.google_button = tk.Button(self.left_frame, text="crawl google", command=self.crawl_google, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.google_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.show_res_button = tk.Button(self.left_frame, text="show crawl res", command=self.show_res, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.show_res_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        # Create a frame for the table
        self.table_frame = tk.Frame(self.left_frame)
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

        # Add widgets to the right frame
        # Add a label for "Sản phẩm đã crawl"
        self.crawl_label = tk.Label(self.right_frame, text="Sản phẩm đã crawl", font=("Helvetica", 14, "bold"))
        self.crawl_label.pack(pady=10, padx=20, anchor='w')
        # Create a dropdown menu
        self.dropdown_var = tk.StringVar(self.right_frame)
        self.dropdown_var.set("Không có sản phẩm nào")  # Default value
        self.search_label = tk.Label(self.right_frame, text="Nhập từ khóa để tìm kiếm", font=self.entry_font)
        self.search_label.pack(pady=0, padx=20, anchor='w')
        self.searchQuery = tk.Entry(self.right_frame, font=self.entry_font, bd=2, relief="solid")
        self.searchQuery.pack(pady=5, padx=20, fill='x')  # Add padding and stretch to fill width
        self.search_button = tk.Button(self.right_frame, text="search", command=self.search, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.search_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.clear_search_button = tk.Button(self.right_frame, text="clear search", command=self.show_res, font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.clear_search_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.send_to_list_of_providers_button = tk.Button(self.right_frame, command=self.on_button_clicked_power_automate, text="gửi cho các nhà cung cấp", font=self.button_font, bg=self.button_bg, fg=self.button_fg, bd=self.button_bd)
        self.send_to_list_of_providers_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width
        self.delete_file_button = tk.Button(self.right_frame,
                                                          command=self.delete_file,
                                                          text="xóa file", font=self.button_font,
                                                          bg='#FFC6C6', fg=self.button_fg, bd=self.button_bd)
        self.delete_file_button.pack(pady=5, padx=10, fill='x')  # Add padding and stretch to fill width

        self.dropdown_menu = tk.OptionMenu(self.right_frame, self.dropdown_var, "Không có sản phẩm nào")
        self.dropdown_menu = tk.OptionMenu(self.right_frame, self.dropdown_var, "Không có sản phẩm nào")

        self.dropdown_menu.config(font=self.entry_font)
        self.dropdown_menu.pack(pady=5, padx=5)  # Add padding and stretch to fill width
        # Create a frame for the results table
        self.results_frame = tk.Frame(self.right_frame)
        self.results_frame.pack(pady=20, padx=20, fill='both', expand=True)
        # Define columns for the results table
        self.results_columns = ("Tên SP", "Giá SP", "Đường Link", "Tỷ lệ khớp (approx)", "Tỷ lệ khớp (exact)", "Nhà cung cấp")
        self.sort_order = {col: True for col in self.results_columns}
        # Create Treeview for the results
        self.results_tree = ttk.Treeview(self.results_frame, columns=self.results_columns, show='headings')
        # Add horizontal and vertical scrollbars to the results_tree
        self.results_tree_scroll_x = ttk.Scrollbar(self.results_frame, orient='horizontal', command=self.results_tree.xview)
        self.results_tree_scroll_y = ttk.Scrollbar(self.results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(xscrollcommand=self.results_tree_scroll_x.set, yscrollcommand=self.results_tree_scroll_y.set)
        self.results_tree_scroll_x.pack(side='bottom', fill='x')
        self.results_tree_scroll_y.pack(side='right', fill='y')
        # Register a click event for the columns
        for col in self.results_columns:
            self.results_tree.heading(col, text=col, command=lambda _col=col: self.on_column_click(_col))
        # Define headings for the results table
        for col in self.results_columns:
            self.results_tree.heading(col, text=col)

        # Add Treeview to the results frame
        self.results_tree.pack(fill='both', expand=True)
    def on_column_click(self, col):
        # Add arrows to columns when clicked
        self.sort_order[col] = not self.sort_order[col]
        for _col in self.results_columns:
            if self.sort_order[col] and col == _col:
                self.results_tree.heading(col, text=f"{col} ↓")
            elif col == _col:
                self.results_tree.heading(col, text=f"{col} ↑")
            else:
                self.results_tree.heading(_col, text=_col)
        # Get all rows from the treeview
        rows = [(self.results_tree.set(item, col), item) for item in self.results_tree.get_children('')]
        # Sort the rows based on the selected column
        if col == "Giá SP":
            rows.sort(key=lambda x: float(x[0].replace('₫', '').replace(',', '')), reverse=self.sort_order[col])
        else:
            rows.sort(reverse=self.sort_order[col])  # Change to True for descending order
        # Rearrange the rows in the treeview
        for index, (value, item) in enumerate(rows):
            self.results_tree.move(item, '', index)
    def delete_file(self):
        if tk.messagebox.askyesno("Xóa file excel kết quả", "Bạn có muốn xóa file kết quả crawl excel?"):
            try:
                os.remove('res.xlsx')
                tk.messagebox.showinfo("Đã xóa file", "File excel crawl đã được xóa thành công.")
            except FileNotFoundError:
                tk.messagebox.showwarning("Không tìm thấy file", "Không thể tìm thấy file excel này.")
    def search(self):
        query = self.searchQuery.get()
        selected_product = self.dropdown_var.get()
        df = self.resDf.parse(selected_product)
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        self.update_res_table(selected_product)
        self.results_tree.delete(*self.results_tree.get_children())
        for index, row in filtered_df.iterrows():
            self.results_tree.insert("", "end", values=(row["prod_name"], row["prod_price"], row["prod_link"], row["fuzz_partial_ratio"], row["fuzz_ratio"]))
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
        for col in self.columns:
            self.tree.heading(col, text=col)
        for index, row in f.iterrows():
            self.results_tree.insert("", "end", values=(row["prod_name"], "{:,.0f}₫".format(row["prod_price"]), row["prod_link"], row["fuzz_partial_ratio"], row["fuzz_ratio"], row["provider"]))
        self.results_tree.bind("<Double-1>", self.on_row_double_click)
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
            
    def on_button_clicked_power_automate(self):
        # URL của flow Power Automate
        flow_url = 'https://prod-42.southeastasia.logic.azure.com:443/workflows/0974535838d340819df4429b61d10ff2/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=MneFsBGvVcw_CDgATsHbPan1HmGBfmTHWeAF9iv8MNk'
        # Tạo button
        # Gửi yêu cầu POST đến Power Automate API để kích hoạt flow
        headers = {
        'Content-Type': 'application/json',
        # Thêm header Authorization nếu flow của bạn yêu cầu xác thực
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
        response = requests.post(flow_url, headers=headers)
    def on_row_double_click(self, event):
        item = self.results_tree.selection()[0]
        row_values = self.results_tree.item(item, "values")
        tk.messagebox.showinfo("Mở link vào trang web của sản phẩm", "Hệ thống sẽ mở trình duyệt để vào đường link của sản phẩm này.")
        webbrowser.open(row_values[2])
        print(f"Double-clicked on row: {row_values[2]}")
    def crawl_google(self):
        crawler = m.GoogleScraper(file_path=self.file_path)
        crawler.crawl()
        tk.messagebox.showinfo("Đã hoàn thành quá trình crawl.", "Crawl sản phẩm từ google thành công.")
        self.show_res()
    def crawl_lazada(self):
        crawler = m.LazadaScraper(file_path=self.file_path)
        crawler.crawl()
        tk.messagebox.showinfo("Đã hoàn thành quá trình crawl.", "Crawl sản phẩm từ lazada thành công.")
