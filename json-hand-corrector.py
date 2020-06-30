import io
import json
import tkinter as tk
from tkinter import font as tkFont

with io.open('tables.txt', mode='r', encoding="utf-8") as file:
	data = json.load(file)

word_idx = 0
max_idx = len(data) - 1

root = tk.Tk()

def load():
	txt_word.delete("1.0", tk.END)
	for line_idx in range(len(data[word_idx])):
		if line_idx == 0:
			prefix = ''
		else:
			prefix = '\n'
		if isinstance(data[word_idx][line_idx], (list, tuple)):
			forms = [form for form in data[word_idx][line_idx]]
			place = 1
			if line_idx != 0:
				txt_word.insert(str(line_idx+1) + ".0", '\n')
			for form in forms:
				txt_word.insert(str(line_idx+1) + "." + str(place), form + ', ')
				place += len(form) + 2
		else:
			txt_word.insert(str(line_idx+1) + ".0", prefix + data[word_idx][line_idx])

def skip():
	global word_idx
	if word_idx + 1 > max_idx:
		return
	word_idx += 1
	load()
	# print(root.winfo_screenwidth(), 'x', root.winfo_screenheight())

def change():
	global word_idx
	for line_idx in range(len(data[word_idx])):
		lines = txt_word.get(str(line_idx+1) + ".0", tk.END)
		line_content = lines.splitlines()[0]
		line_content = line_content.lstrip('\n')
		forms = line_content.split(', ')
		try:
			while True:
				forms.remove('')
		except ValueError:
			pass
		if len(forms) == 0:
			data[word_idx][line_idx] = ''
		elif len(forms) == 1:
			data[word_idx][line_idx] = forms[0]
		else:
			form_list = [form for form in forms]
			data[word_idx][line_idx] = form_list

	print(data[word_idx], 'len:', len(data[word_idx]))
	if word_idx + 1 > max_idx:
		return
	word_idx +=1
	load()


pixels_height = tkFont.Font(family='Courier New', size=12).metrics('linespace')
font = tkFont.Font(family='Courier New', size=12, weight='normal')
pixels_width = font.measure('0')

txt_word = tk.Text(
	root, font=font, width=int(root.winfo_screenwidth()*0.4/pixels_width),
	height=int(root.winfo_screenheight()*0.8/pixels_height)
	)
txt_word.grid(row=0, column=1, columnspan=2)
scr_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
scr_scrollbar.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E)

txt_word.config(xscrollcommand=scr_scrollbar.set, wrap=tk.NONE)
scr_scrollbar.config(command=txt_word.xview)

labels = (
	'nom. sg.', 'gen. sg.', 'acc. sg.', 'par. sg.', 'ill. sg.', 'ine. sg.',
	'all. sg.', 'ade. sg.', 'ela. sg.', 'abl. sg.', 'ess. sg.', 'abe. sg.',
	'tra. sg.', 'ins. sg.', 'com. sg.', 'nom. pl.', 'gen. pl.', 'acc. pl.',
	'par. pl.', 'ill. pl.', 'ine. pl.', 'all. pl.', 'ade. pl.', 'ela. pl.',
	'abl. pl.', 'ess. pl.', 'abe. pl.', 'tra. pl.', 'ins. pl.', 'com. pl.',
	'eng. tr.'
	)
txt_labels = tk.Text(
	root, width=int(root.winfo_screenheight()*0.3/pixels_height),
	height=int(root.winfo_screenheight()*0.8/pixels_height),
	font=font
	)
counter = 0
for label in labels:
	if counter != 0:
		label = '\n' + label
	txt_labels.insert(str(counter+1)+'.0', label)
	counter += 1
txt_labels.grid(row=0, column=0)
txt_labels.config(state=tk.DISABLED)
btn_skip = tk.Button(
	root, text="Skip", font=('Helvetica', 14, 'bold'), command=skip,
	width=10
	)
btn_skip.grid(row=2, column=1, pady=10)
btn_change = tk.Button(
	root, text="Change", font=('Helvetica', 14, 'bold'), command=change,
	width=10
	)
btn_change.grid(row=2, column=2, pady=10)

load()

root.mainloop()

with io.open('tables.txt', mode='w', encoding="utf-8") as file:
	json.dump(data, file)