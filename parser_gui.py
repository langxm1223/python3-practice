#!/usr/bin/env python3

#Trial of parser GUI
import math
from tkinter import *
from tkinter.ttk import *
from tkinter.dialog import *

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.pyplot import specgram
import getopt, sys
import os.path
import matplotlib.pyplot as plt
import re
import matplotlib
import datetime
from mpl_toolkits.mplot3d import axes3d
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename

# special indicator in log file
ALL = W+N+E+S


def usage():
		print("---- usage ----")
		print("./parser_gui.py")


def print_stats(data_label, data):
	print("")
	print("---- %s ----" % (data_label))
	print("min:   %f" % (min(data)))
	print("max:   %f" % (max(data)))
	print("mean:  %f" % (np.mean(data)))
	print("stdev: %f" % (np.std(data)))
	print("")


def plot_diagram_together(var):
	var_tmp = var.strip().split(',')
	var_num = var.count(',') + 1


	drawPic.a=drawPic.f.add_subplot(111)

	for variable in var_tmp:
		# if the variable has multiple numbers
		data_list = variable_dict[variable]["data"]
		for i in range(len(data_list)):
			if len(data_list) > 1:
				data_label = "%s_%d" % (variable.split("@")[0], i)
			else:
				data_label = variable.split("@")[0]
			drawPic.a.plot(variable_dict[variable]["ts"], data_list[i], label=data_label)

	drawPic.a.legend(loc='upper left')
	drawPic.a.set_xlabel('time (s)')
	drawPic.a.set_ylabel('wow')
	ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:}'.format(str(datetime.timedelta(seconds=x))))
	drawPic.a.xaxis.set_major_formatter(ticks)
	drawPic.a.grid(True)

	drawPic.canvas.draw()


def plot_diagram_sharex(var):
	var_tmp = var.strip().split(',')
	var_num = var.count(',') + 1
	if var_num < 4:
		rowNum = var_num
		colNum = 1
	elif var_num < 9:
		rowNum = math.ceil(var_num / 2)
		colNum = 2
	else:
		messagebox.showwarning(title = 'parser_gui', message = "So many plots together, you\'d better change your option")
		rowNum = math.ceil(var_num / 3)
		colNum = 3
	plot_number = 1
	drawPic.a = drawPic.f.add_subplot(rowNum,colNum,plot_number)

	for variable in var_tmp:
		data_list = variable_dict[variable]["data"]
		# if the variable has multiple numbers
		for i in range(len(data_list)):
			if len(data_list) > 1:
				data_label = "%s_%d" % (variable.split("@")[0], i)
			else:
				data_label = variable.split("@")[0]
			drawPic.a.plot(variable_dict[variable]["ts"], data_list[i], label=data_label)

			print_stats(data_label, data_list[i])

		plot_number += 1

		drawPic.a.legend(loc='upper left')
		drawPic.a.set_xlabel('time (s)')
		drawPic.a.set_ylabel('wow')
		ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:}'.format(str(datetime.timedelta(seconds=x))))
		drawPic.a.xaxis.set_major_formatter(ticks)
		drawPic.a.grid(True)

		if plot_number <= var_num:
			drawPic.a=drawPic.f.add_subplot(rowNum,colNum,plot_number, sharex = drawPic.a)

	drawPic.canvas.draw()


def plot_diagram_2d(var):
	var_tmp = var.strip().split(',')
	var_num = var.count(',') + 1
	if var_num != 2:
		messagebox.showerror(title = 'parser_gui', message = "Your input must be 2 for 2d plot")
		return None
	if len(variable_dict[var_tmp[0]]["data"][0]) != len(variable_dict[var_tmp[1]]["data"][0]):
		messagebox.showerror(title = 'parser_gui', message = "They have different rank, check your selection!")
		return None

	x = variable_dict[var_tmp[0]]["data"][0]
	y = variable_dict[var_tmp[1]]["data"][0]

	drawPic.a=drawPic.f.add_subplot(111)
	drawPic.a.set_title('2d plot')
	drawPic.a.plot(x, y, color = "r",  linewidth = 1.5)

	drawPic.a.set_xlabel(var_tmp[0])
	drawPic.a.set_ylabel(var_tmp[1])
	drawPic.a.grid(True)

	drawPic.canvas.draw()

def plot_diagram_3d(var):
	var_tmp = var.strip().split(',')
	var_num = var.count(',') + 1
	if var_num != 3:
		messagebox.showerror(title = 'parser_gui', message = "Your input must be 3 for 3d plot")
		return None
	if (len(variable_dict[var_tmp[0]]["data"][0]) != len(variable_dict[var_tmp[1]]["data"][0])) or \
		(len(variable_dict[var_tmp[0]]["data"][0]) != len(variable_dict[var_tmp[2]]["data"][0])):
		messagebox.showerror(title = 'parser_gui', message = "They have different rank, check your selection!")
		return None

	x = variable_dict[var_tmp[0]]["data"][0]
	y = variable_dict[var_tmp[1]]["data"][0]
	z = variable_dict[var_tmp[2]]["data"][0]

	drawPic.a=drawPic.f.add_subplot(111, projection = '3d')
	drawPic.a.plot(x,y,z)
	drawPic.a.set_title('xyz-plot')

	drawPic.a.set_xlabel(var_tmp[0])
	drawPic.a.set_ylabel(var_tmp[1])
	drawPic.a.set_zlabel(var_tmp[2])

	drawPic.a.grid(True)

	drawPic.canvas.draw()

def drawPic():
	drawPic.f.clf()
	count = 0
	output = ''
	for i in checkList:
		if i.get() == 1:
			output = output + orderedKey[count] +','
		count += 1
	if output != '' :
		output = output[:-1]
		if option.get() == 1:
			plot_diagram_together(output)
		elif mode.get() == 1 and option.get() == 0:
			plot_diagram_2d(output)
		elif mode.get() == 2 and option.get() == 0:
			plot_diagram_3d(output)
		else:
			plot_diagram_sharex(output)
	else:
		messagebox.showwarning(title = 'parser_gui', message = "No variables are selected.\nChoose at least one variable.")

def drawInterval():
	drawPic.f.clf()
	count = 0
	output = ''
	for i in checkList:
		if i.get() == 1:
			output = orderedKey[count]
			break
		count += 1
	if output == '':
		messagebox.showwarning(title = 'parser_gui', message = "No variables are selected.\nChoose at least one variable.")
		return None

	drawPic.a=drawPic.f.add_subplot(111)
	drawPic.a.set_title('interval plot')
	drawPic.a.plot(variable_dict[output]["ts"][1:], variable_dict[output]["interval"][1:], label = output+' interval')
	# drawPic.a.hist(variable_dict[output]["interval"][1:], 500)
	drawPic.a.grid(True)
	drawPic.canvas.draw()

def drawPSD():
	drawPic.f.clf()
	count = 0
	output = ''
	for i in checkList:
		if i.get() == 1:
			output = orderedKey[count]
			break
		count += 1
	if output == '':
		messagebox.showwarning(title = 'parser_gui', message = "No variables are selected.\nChoose at least one variable.")
		return None

	data_list = variable_dict[output]["data"]
	if (len(data_list) != 3):
		messagebox.showerror(title = 'parser_gui', message = "Only Accelerometer or Gyrometer data could print spectrogram, and acc or gyro must \
			be printed in ONE variable with equal dimension! Check your print or selection!")
		return None

	x = np.array(data_list[0])
	y = np.array(data_list[1])
	z = np.array(data_list[2])
	norm = np.sqrt(x * x + y * y + z * z)
	
	num = len(z)
	dur = variable_dict[output]["ts"][num-1] - variable_dict[output]["ts"][0]
	dt = dur/float(num-1)
	sr = 1/dt
	print("Duration of data: %f sec" % dur)
	print("Sampling rate: %f Hz" % sr)

	NW = dur
	nfft = 2**int(np.log(float(num)/float(NW))/np.log(2))
	noverlap=nfft/2

	drawPic.a=drawPic.f.add_subplot(211)
	drawPic.a.set_title('IMU_plot')
	drawPic.a.plot(variable_dict[output]["ts"], z, label = output.split("@")[0])
	drawPic.a.legend(loc='upper left')
	drawPic.a.set_xlabel('time')
	drawPic.a.set_ylabel('IMU z data')
	ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:}'.format(str(datetime.timedelta(seconds=x))))
	drawPic.a.xaxis.set_major_formatter(ticks)
	drawPic.a.grid(True)

	# drawPic.a=drawPic.f.add_subplot(212, sharex = drawPic.a)
	drawPic.a=drawPic.f.add_subplot(212)
	drawPic.a.set_title('PSD plot')
	pxx, freq, t, cax = drawPic.a.specgram(z, NFFT=nfft, Fs=sr, noverlap=noverlap, cmap='viridis')
	cbar = drawPic.f.colorbar(cax)
	cbar.set_label('Intensity dB')
	ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:}'.format(str(datetime.timedelta(seconds=x+variable_dict[output]["ts"][0]))))
	drawPic.a.xaxis.set_major_formatter(ticks)
	# drawPic.a.axis("tight")
	drawPic.a.set_xlabel('time')
	drawPic.a.set_ylabel('Freq(Hz)')
	drawPic.a.grid(True)
	drawPic.canvas.draw()

def fitCurve():
	drawPic.f.clf()
	data_x = np.array(variable_dict['baro_temperature@[ms5611.c:357]']["data"][0])
	data_y = np.array(variable_dict['baro_pressure@[ms5611.c:357]']["data"][0])

	c = zip(data_x, data_y)
	c = sorted(c, key=lambda x: x[0])
	data_x, data_y = zip(*c)
	fitting = np.polyfit(data_x, data_y, 5)
	coeff = np.poly1d(fitting)
	print(coeff)
	fitted_y = coeff(data_x)

	drawPic.a=drawPic.f.add_subplot(111)
	drawPic.a.set_title('curve fitting')
	drawPic.a.plot(data_x, data_y, 's',label='original values')
	drawPic.a.plot(data_x, fitted_y, 'r',label='polyfit values')
	drawPic.a.set_xlabel('temperature')
	drawPic.a.set_ylabel('pressure')
	drawPic.a.grid(True)
	drawPic.canvas.draw()

def parse_file(input_file):

	global variable_dict
	global checkList
	global orderedKey

	with open(input_file, 'r') as fh:
		lines_total = 0
		while 1:
			buffer = fh.read(8*1024*1024)
			if not buffer:
				break
			lines_total += buffer.count('\n')
	print("File total lines : %d" % lines_total)

	fh = open(input_file, 'r')
	variable_dict = {}
	lines_count = 0

	popup = Toplevel()
	popup.grab_set()
	Label(popup, text="Loading").grid(row=0,column=0)
	progress_var = DoubleVar()
	progress_bar = Progressbar(popup, length = 400, mode = "determinate", variable=progress_var, orient=HORIZONTAL, maximum = lines_total)
	progress_bar.grid(row=1, column=0)
	# popup.pack_slaves()
	progress_step = lines_total // 2000 + 1

	try:
		for line in fh:
			# search p[...] pattern and skip the line if pattern not present
			lines_count += 1
			if not lines_count % progress_step:
				popup.update()
				progress_var.set(lines_count)

			if 'p[' not in line:
				continue

			line = line[line.find("p[")+2:]

			if "]" not in line:
				continue

			line = line[0:line.find("]")]

			# parse the line with : separator
			filename, linu_num, time_usec, data = line.strip().split(':')
			time_sec = float(time_usec)/1000000
			# tokenize data groups sperated by comma
			data_groups = data.split(",")

			for g in data_groups:

				# in each data group, the fields are space separated:
				# data_name value1 value2 value3 ... valueN
				t = g.strip().split(" ")

				data_cnt = len(t) - 1

				# use dataname@[filename:line] tuple as dictionary key
				# in case the same dataname occurs at different places
				data_key = "%s@[%s:%s]" % (t[0], filename, linu_num)

				# the dictionary element format:
				# {"ts": 12345, "data": [[], [], [], ...], "interval": []}
				if data_key not in variable_dict:
					variable_dict[data_key] = {"ts":[], "data":[[] for i in range(data_cnt)], "interval":[0]}
				else:
					time_interval = time_sec - variable_dict[data_key]["ts"][-1]
					variable_dict[data_key]["interval"].append(time_interval)

				variable_dict[data_key]["ts"].append(time_sec)

				for i in range(data_cnt):
					variable_dict[data_key]["data"][i].append(float(t[i+1]))
	except:
		print("Illegal log pattern occurred!")
	finally:
		fh.close()
		popup.destroy()

	orderedKey = sorted(variable_dict)
	checkRow = 0
	checkColumn = 0
	if checkColumn == 0:
		checkOrder = W+N
	else:
		checkOrder = E+N

	varCanvas.delete("all")
	varFrame = Frame(varCanvas)
	varCanvas.create_window((0,0), window=varFrame, anchor="nw")
	varFrame.bind("<Configure>", lambda event, canvas=varCanvas: onFrameConfigure(varCanvas))

	checkList=[]
	for key in orderedKey:
		w = IntVar()

		if len(variable_dict[key]["data"]) > 1:
			Checkbutton(varFrame, text = str(key.split("@")[0]) + '*%d' % len(variable_dict[key]["data"]), variable = w).grid(row = checkRow, column = checkColumn, sticky = checkOrder)
		else:
			Checkbutton(varFrame, text = key.split("@")[0], variable = w).grid(row = checkRow, column = checkColumn, sticky = checkOrder)

		if checkRow < (len(variable_dict) // 2):
			checkRow += 1
		else:
			checkRow = 0
			checkColumn = 1
		# checkRow += 1
		checkList.append(w)

def onFrameConfigure(canvas):
	'''Reset the scroll region to encompass the inner frame'''
	canvas.configure(scrollregion=canvas.bbox("all"))

def openFile(root):
	global input_file
	path = askopenfilename()
	if path:
		base_name = os.path.basename(path)
		input_file = os.path.abspath(path)
		root.title("----- %s -----" % (base_name))
		print(input_file)
		if os.path.isfile(input_file):
			parse_file(input_file)

def interfaceInit():

	global mode
	global option
	global varCanvas
	global varFrame

	# GUI initialization
	root = Tk()
	root.rowconfigure(1, weight = 1)
	root.columnconfigure(1, weight = 1)
	root.columnconfigure(2, weight = 1)
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()
	root.geometry("%dx%d" %(w, h))

	canvasFrame = Frame(root)
	canvasFrame.grid(row = 1, column = 0, sticky = ALL)

	varCanvas = Canvas(canvasFrame, borderwidth=0)
	varFrame = Frame(varCanvas)
	varScrollbar = Scrollbar(canvasFrame, orient="vertical", command=varCanvas.yview)
	varCanvas.configure(yscrollcommand=varScrollbar.set)

	varScrollbar.pack(side="right", fill="y")
	varCanvas.pack(side="left", fill="both", expand=True)
	varCanvas.create_window((0,0), window=varFrame, anchor="nw")

	varFrame.bind("<Configure>", lambda event, canvas=varCanvas: onFrameConfigure(varCanvas))

	def resetVar():
		for i in checkList:
			if i.get() == 1:
				i.set(0)

	def selectAll():
		for i in checkList:
			i.set(1)

	sep = Separator(root, orient = "horizontal")
	sep.grid(row = 2, column = 0, sticky = ALL)

	optFrame = Frame(root)
	optFrame.grid(row = 3, column = 0, sticky = ALL)

	optFrame.columnconfigure(0, weight = 1)
	optFrame.columnconfigure(1, weight = 1)
	optFrame.columnconfigure(2, weight = 1)
	# Label(optFrame, text = 'google.com',bg = 'red',width = 40,height = 3,wraplength = 80,anchor = 'w').grid(row = 0, column = 0, columnspan = 2)

	option = IntVar()
	option.set(0)
	rb_opt1 = Radiobutton(optFrame,text = 'share-time', variable = option, value = 0)
	rb_opt2 = Radiobutton(optFrame,text = 'all-in-one', variable = option, value = 1)
	rb_opt1.grid(row = 1, column = 0, sticky = W)
	rb_opt2.grid(row = 1, column = 1, sticky = W)

	mode = IntVar()
	mode.set(0)
	rb_mode1 = Radiobutton(optFrame,text = 'normal', variable = mode, value = 0)
	rb_mode2 = Radiobutton(optFrame,text = '2d', variable = mode, value = 1)
	rb_mode3 = Radiobutton(optFrame,text = '3d', variable = mode, value = 2)
	rb_mode1.grid(row = 2, column = 0, sticky = W)
	rb_mode2.grid(row = 2, column = 1, sticky = W)
	rb_mode3.grid(row = 2, column = 2, sticky = W)

	ResetSelectallFrame = Frame(root)
	ResetSelectallFrame.grid(row = 4, column = 0, sticky = ALL)

	ResetSelectallFrame.columnconfigure(0, weight = 1)
	ResetSelectallFrame.columnconfigure(1, weight = 1)

	resetButton = Button(ResetSelectallFrame, text = 'RESET', command = resetVar)
	resetButton.grid(row = 0, column = 0, sticky = ALL)

	allButton = Button(ResetSelectallFrame, text = 'Select All', command = selectAll)
	allButton.grid(row = 0, column = 1, sticky = ALL)

	buttonFrame = Frame(root)
	buttonFrame.grid(row = 5, column = 0, sticky=ALL)
	buttonFrame.columnconfigure(0, weight = 1, uniform = '')
	buttonFrame.columnconfigure(1, weight = 1)
	buttonFrame.columnconfigure(2, weight = 1)
	buttonFrame.columnconfigure(3, weight = 1)

	drawButton = Button(buttonFrame,text = 'Draw',command = drawPic)
	drawButton.grid(row = 0, column = 0, sticky = ALL)

	drawIntvButton = Button(buttonFrame, text = 'Draw Interval', command = drawInterval)
	drawIntvButton.grid(row = 0, column = 1, sticky = ALL)

	drawPSDButton = Button(buttonFrame, text = 'PSD', command = drawPSD)
	drawPSDButton.grid(row = 0, column = 2, sticky = ALL)

	drawPSDButton = Button(buttonFrame, text = 'Fitting Curve', command = fitCurve)
	drawPSDButton.grid(row = 0, column = 3, sticky = ALL)

	drawPic.f = Figure()
	drawPic.canvas = FigureCanvasTkAgg(drawPic.f, root)
	drawPic.canvas.draw()
	drawPic.canvas.get_tk_widget().grid(row = 1, rowspan = 5, column = 1, columnspan = 2, sticky = ALL)

	openButton = Button(root, text = 'OPEN', command = lambda : openFile(root))
	openButton.grid(row = 0, column = 0, sticky = ALL)

	toolbarFrame = Frame(root)
	toolbarFrame.grid(row = 0, column = 1, sticky = W)
	toolbar = NavigationToolbar2Tk(drawPic.canvas, toolbarFrame)
	toolbar.update()

	def _quit():
		root.quit()   # stops mainloop
		root.destroy()  # this is necessary on Windows to prevent
		sys.exit()    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

	button = Button(master=root, text='Quit', command=_quit)
	button.grid(row = 0, column = 2, sticky = E)
	root.protocol("WM_DELETE_WINDOW", _quit)

	root.mainloop()

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()

	interfaceInit()
	sys.exit()

if __name__ == "__main__":
	main()
