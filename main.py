import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from flask import Flask, request, jsonify
from thefuzz import fuzz
from thefuzz import process
from fake_useragent import UserAgent
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
from ui import SimpleGUI
if __name__ == '__main__':
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()