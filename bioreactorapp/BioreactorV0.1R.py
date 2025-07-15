# ejecuta con Alt + V notepad windows
# resolucion maxima 800 x 480
import time

from tkinter import *
from tkinter import filedialog, messagebox, ttk

import serial

from Co2Sen import *
from RdMega import *
# from ReadPress import *
from SaveDataDay import *
from ServPWM import *

colorg = "#d1e1c4"
root = Tk()

root.title("Bioreactor")
# root.iconbitmap("icono.ico")
root.geometry("800x480")  # window dimenssion
root.resizable(0, 0)  # No resize

myFrame = Frame(root, bg=colorg)
myFrame.pack(fill="both")

s = ttk.Style()
s.theme_create(
    "greeny",
    parent="alt",
    settings={
        "TNotebook": {
            "configure": {"tabmargins": [2, 5, 2, 0], "background": colorg},
        },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": colorg},
            "map": {
                "background": [("selected", colorg)],
                "expand": [("selected", [1, 1, 1, 0])],
            },
        },
    },
)
s.theme_use("greeny")

tabs = ttk.Notebook(myFrame)
tabs.pack(pady=10, padx=10, fill="both", expand=True)

# frames configuration
frameView = Frame(tabs, bg=colorg, width=780, height=460)
frameView.pack(fill="both", expand=True)
frameLight = Frame(tabs, bg=colorg, width=780, height=460)
frameLight.pack(fill="both", expand=True)
frameConfiguration = Frame(tabs, bg=colorg, width=780, height=460)
frameConfiguration.pack(fill="both", expand=True)

# tabs definition
tabs.add(frameView, text="Sensors View")
tabs.add(frameLight, text="Light Adjust")
tabs.add(frameConfiguration, text="Configurations")

# images
scheme = PhotoImage(file="/home/pi/BioreactorApp/Scheme.png")
# 5-10 Relation to resize
scheme = scheme.zoom(5)
scheme = scheme.subsample(10)

# serial connection
ser = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout=1)
ser.flush()

##
flg = 0
# variables sensores

ph = "0"
valuePH = StringVar()
valuePH.set(ph)  # valuePH.set(10)

od = "0"
valueOD = StringVar()
valueOD.set(od)

tmp = "0"
valueTMP = StringVar()
valueTMP.set(tmp)

lvl = "2.8"
valueLVL = StringVar()
valueLVL.set(lvl)

co2 = "850"
valueCO2 = StringVar()
valueCO2.set(co2)

led = "0"
valueLED = StringVar()
valueLED.set(led)

red = "0"
valueRED = StringVar()
valueRED.set(red)

blue = "0"
valueBLU = StringVar()
valueBLU.set(blue)

green = "0"
valueGRE = StringVar()
valueGRE.set(green)

pmp = "0"
valuePmp = StringVar()
valuePmp.set(pmp)

wint = "0"
valueWIn = StringVar()
valueWIn.set(wint)

wint = "0"
valueWIn = StringVar()
valueWIn.set(wint)

aout = "0"
valueAOut = StringVar()
valueAOut.set(aout)

cint = "0"
valueCIn = StringVar()
valueCIn.set(cint)

ampsin = "50"
valueAmpSin = StringVar()
valueAmpSin.set(ampsin)

persin = "1"
valuePerSin = StringVar()
valuePerSin.set(persin)

ampsqr = "50"
valueAmpSqr = StringVar()
valueAmpSqr.set(ampsqr)

persqr = "1"
valuePerSqr = StringVar()
valuePerSqr.set(persqr)

fname = "bio_data"
valueFName = StringVar()
valueFName.set(fname)

route = "/home/pi/Desktop/BioreactorData"
valueRoute = StringVar()
valueRoute.set(route)

# variable Radiobutton
default = "1"
typeOption = IntVar()
typeOption.set(default)
lightOption = IntVar()
lightOption.set(default)

# variable checkbox
algaeOut = IntVar()
lvlCtrl = IntVar()
phCtrl = IntVar()
logActive = IntVar()

# funcines

def is_time_between(start, end):
    now = time.localtime().tm_hour
    
    if start <= end:
        return start <= now <= end
    else:
        return now >= start or now <= end


def types():
    if lightOption.get() == 1:
        putWhInt.config(state="normal")
        putRedInt.config(state="disabled")
        putBluInt.config(state="disabled")
        putGreInt.config(state="disabled")
    elif lightOption.get() == 2:
        putWhInt.config(state="disabled")
        putRedInt.config(state="normal")
        putBluInt.config(state="normal")
        putGreInt.config(state="normal")


def forms():
    if typeOption.get() == 1:
        putAmpSin.config(state="disabled")
        putPerSin.config(state="disabled")
        putAmpSqr.config(state="disabled")
        putPerSqr.config(state="disabled")
    elif typeOption.get() == 2:
        putAmpSin.config(state="normal")
        putPerSin.config(state="normal")
        putAmpSqr.config(state="disabled")
        putPerSqr.config(state="disabled")
    elif typeOption.get() == 3:
        putAmpSin.config(state="disabled")
        putPerSin.config(state="disabled")
        putAmpSqr.config(state="normal")
        putPerSqr.config(state="normal")


def only_numbers(char):
    return char.isdigit()


validation = root.register(only_numbers)


def updateVal():
    global counter
    global ph
    global od
    global tmp
    global flg

    if ser.inWaiting() > 0:
        try:
            data = ser.readline().decode("UTF-8")
            ser.flushInput()
            data = data.split(",")
            if len(data) < 5:
                raise IndexError()
            #print(data)
            ph = data[2]
            od = data[1]
            tmp = data[3]
            #print(time.localtime()[5], od, ph, tmp)
        except IndexError:
            dummy=0
            
    # ph = phvalue(0)  ##ph sensor
    valuePH.set(ph)

    # od=dovalue(od)  ##dissolved oxygen snsor
    valueOD.set(od)

    # tmp=tmpvalue(tmp)  ##temperature sensor
    tmp2 = round((float(tmp) * (9 / 5)) + 32, 2)  ##fahrenheit conversion
    valueTMP.set(tmp)

    co2_V = co2Sen() * 0.003222  ##co2 sensor where 0.05 is the gain
    co2_mA = (co2_V / 165.0) * 1000
    co2 = round(((200000 - 0) / (40 - 4)) * (co2_mA - 4))
    valueCO2.set(co2)

    lvl = 999  ##readPress()  ##presure sensor
    lvl2 = round(lvl / 100, 2)  ##gain
    valueLVL.set(lvl2)

    fname = valueFName.get()
    route = valueRoute.get()

    ############### WHITE ###############
    if valueLED.get():
        try:
            if len(valueLED.get()) == 0:  ##null entry?
                pwv = 0
            elif float(valueLED.get()) > 100:  ##max 100 percent
                pwv = 4095
                valueLED.set("100")
            else:
                pwv = round(
                    int(float(valueLED.get())) * 40.95,
                )  ##Round var and scale to 0-4095
            
            if is_time_between(9, 21):
                pwmWhite(pwv)  ##set white led intensity percent
            else:
                pwmWhite(0)
        except ValueError:
            messagebox.showerror(
                title="Not a number",
                message="Please only numbers",
            )
            valueLED.set("0")

    ############### GREEN ###############
    if valueGRE.get():
        try:
            if len(valueGRE.get()) == 0:  ##null entry?
                pgv = 0
            elif float(valueGRE.get()) > 100:  ##max 100 percent RED GRE BLU
                pgv = 4095
                valueGRE.set("100")
            else:
                pgv = round(
                    int(float(valueGRE.get())) * 40.95,
                )  ##Round var and scale to 0-4095
            pwmGreen(pgv)  ##set green led intensity percent
        except ValueError:
            messagebox.showerror(
                title="Not a number",
                message="Please only numbers",
            )
            valueGRE.set("0")

    ############### RED ###############
    if valueRED.get():
        try:
            if len(valueRED.get()) == 0:  ##null entry?
                prv = 0
                valueRED.set("0")
            elif float(valueRED.get()) > 100:  ##max 100 percent RED GRE BLU
                prv = 4095
                valueRED.set("100")
            else:
                prv = round(
                    int(float(valueRED.get())) * 40.95,
                )  ##Round var and scale to 0-4095
            pwmRed(prv)  ##set green led intensity percent
        except ValueError:
            messagebox.showerror(
                title="Not a number",
                message="Please only numbers",
            )
            valueRED.set("0")

    ############### BLUE ###############
    if valueBLU.get():
        try:
            if len(valueBLU.get()) == 0:  ##null entry?
                pbv = 0
            elif float(valueBLU.get()) > 100:  ##max 100 percent RED GRE BLU
                pbv = 4095
                valueBLU.set("100")
            else:
                pbv = round(
                    int(float(valueBLU.get())) * 40.95,
                )  ##Round var and scale to 0-4095
            pwmBlue(pbv)  ##set green led intensity percent
        except ValueError:
            messagebox.showerror(
                title="Not a number",
                message="Please only numbers",
            )
            valueBLU.set("0")

    ############### PUMP ###############
    if valuePmp.get():
        try:
            if len(valuePmp.get()) == 0:  ##null entry?
                ppv = 0
            elif float(valuePmp.get()) > 100:  ##max 100 percent RED GRE BLU
                ppv = 4095
                valuePmp.set("100")
            else:
                ppv = round(
                    int(float(valuePmp.get())) * 40.95,
                )  ##Round var and scale to 0-4095
            pwmPump(ppv)  ##set green led intensity percent
        except ValueError:
            messagebox.showerror(
                title="Not a number",
                message="Please only numbers",
            )
            valuePmp.set("0")

    ############## save data  ##############

    datatosave = {
        valuePH.get()
        + ","
        + valueOD.get()
        + ","
        + valueTMP.get()
        + ","
        + valueLVL.get()
        + ","
        + valueCO2.get()
        + ","
        + valueLED.get()
        + ","
        + valueRED.get()
        + ","
        + valueGRE.get()
        + ","
        + valueBLU.get()
        + ","
        + valuePmp.get(),
    }

    ##data info message
    if flg == 0:
        datatosave = {
            "PH value,DO value,Temperature value,Level value,CO2 value"
            + ",White LED value,Red LED value, Green LED value, Blue LED value, Power pump value",
        }
        flg = 1

    if logActive.get() == 0:
        flg = 0

    ##add condition
    if logActive.get() == 1:
        savedata(route, fname, datatosave)

    root.after(1000, updateVal)


def on_closing():
    response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if response:
        root.withdraw()
        root.quit()


def browsepath():
    path = filedialog.askdirectory()

    valueRoute.set(path)


# -------------------------------------------------------------------------------------------------
# Indicators 1st tab
txtp1 = Label(frameView, text="", bg=colorg)
txtp1.grid(row=0, column=0, pady=3, padx=50)

imgScheme = Label(frameView, image=scheme)
imgScheme.grid(row=0, column=3, pady=3, padx=60, rowspan=12)

txtPH = Label(frameView, text="PH", font=("Arial", 12), bg=colorg)
txtPH.grid(row=0, column=1, pady=3, padx=3, sticky="W")
showVPH = Entry(frameView, textvariable=valuePH, width=8, font=("Arial", 12))
showVPH.grid(row=0, column=2, pady=3, padx=3)

txtOD = Label(
    frameView,
    text="Dissolved Oxygen (mg/L)",
    font=("Arial", 12),
    bg=colorg,
)
txtOD.grid(row=1, column=1, pady=3, padx=3, sticky="W")
showOD = Entry(frameView, textvariable=valueOD, width=8, font=("Arial", 12))
showOD.grid(row=1, column=2, pady=3, padx=3)

txtTMP = Label(frameView, text="Temperature (F)", font=("Arial", 12), bg=colorg)
txtTMP.grid(row=2, column=1, pady=3, padx=3, sticky="W")
showTMP = Entry(frameView, textvariable=valueTMP, width=8, font=("Arial", 12))
showTMP.grid(row=2, column=2, pady=3, padx=3)

txtLVL = Label(frameView, text="Water level (L)", font=("Arial", 12), bg=colorg)
txtLVL.grid(row=3, column=1, pady=3, padx=3, sticky="W")
showLVL = Entry(frameView, textvariable=valueLVL, width=8, font=("Arial", 12))
showLVL.grid(row=3, column=2, pady=3, padx=3)

txtCO2 = Label(
    frameView,
    text="Concentration CO2 (ppm)",
    font=("Arial", 12),
    bg=colorg,
)
txtCO2.grid(row=4, column=1, pady=3, padx=3, sticky="W")
showCO2 = Entry(frameView, textvariable=valueCO2, width=8, font=("Arial", 12))
showCO2.grid(row=4, column=2, pady=3, padx=3)
# showCO2.config(state= "disabled")

txtLED = Label(
    frameView,
    text="White light intensity (%)",
    font=("Arial", 12),
    bg=colorg,
)
txtLED.grid(row=5, column=1, pady=3, padx=3, sticky="W")
showLED = Entry(frameView, textvariable=valueLED, width=8, font=("Arial", 12))
showLED.grid(row=5, column=2, pady=3, padx=3)

txtRED = Label(
    frameView,
    text="Red light intensity (%)",
    font=("Arial", 12),
    bg=colorg,
)
txtRED.grid(row=6, column=1, pady=3, padx=3, sticky="W")
showRED = Entry(frameView, textvariable=valueRED, width=8, font=("Arial", 12))
showRED.grid(row=6, column=2, pady=3, padx=3)

txtGRE = Label(
    frameView,
    text="Green light intensity (%)",
    font=("Arial", 12),
    bg=colorg,
)
txtGRE.grid(row=7, column=1, pady=3, padx=3, sticky="W")
showGRE = Entry(frameView, textvariable=valueGRE, width=8, font=("Arial", 12))
showGRE.grid(row=7, column=2, pady=3, padx=3)

txtBLU = Label(
    frameView,
    text="Blue light intensity (%)",
    font=("Arial", 12),
    bg=colorg,
)
txtBLU.grid(row=8, column=1, pady=3, padx=3, sticky="W")
showBLU = Entry(frameView, textvariable=valueBLU, width=8, font=("Arial", 12))
showBLU.grid(row=8, column=2, pady=3, padx=3)

txtPMP = Label(
    frameView,
    text="Air pump power (%)",
    font=("Arial", 12),
    bg=colorg,
)
txtPMP.grid(row=9, column=1, pady=3, padx=3, sticky="W")
showPMP = Entry(frameView, textvariable=valuePmp, width=8, font=("Arial", 12))
showPMP.grid(row=9, column=2, pady=3, padx=3)
# -------------------------------------------------------------------------------------------------
# Indicators 2nd tab
########## TYPE
txtp1 = Label(frameLight, text="", bg=colorg)
txtp1.grid(row=0, column=0, pady=3, padx=50)

txtLT = Label(
    frameLight,
    text="Select type of light",
    font=("Arial", 12, "bold"),
    bg=colorg,
)
txtLT.grid(row=0, column=1, pady=3, padx=3, columnspan=8)

whiteLight = Radiobutton(
    frameLight,
    text="White light",
    font=("Arial", 12),
    variable=lightOption,
    value=1,
    command=types,
    bg=colorg,
)
whiteLight.grid(row=1, column=1, pady=3, padx=3, columnspan=4)

rgbLight = Radiobutton(
    frameLight,
    text="RGB light",
    font=("Arial", 12),
    variable=lightOption,
    value=2,
    command=types,
    bg=colorg,
)
rgbLight.grid(row=1, column=5, pady=3, padx=3, columnspan=4)

# Read value white bright
txtWhInt = Label(
    frameLight,
    text="White light intensity (0-100%)",
    font=("Arial", 12),
    bg=colorg,
)
txtWhInt.grid(row=2, column=3, pady=3, padx=3, columnspan=3)
putWhInt = Entry(frameLight, textvariable=valueLED, width=8, font=("Arial", 12))
putWhInt.grid(row=2, column=6, pady=3, padx=3)

# Wite slider
txtSlidWh = Label(frameLight, text="White light", font=("Arial", 12), bg=colorg)
txtSlidWh.grid(row=3, column=1, pady=3, padx=3)
WhSlid = Scale(
    frameLight,
    from_=0,
    to=100,
    length=400,
    orient="horizontal",
    variable=valueLED,
    bg=colorg,
)
WhSlid.grid(row=3, column=2, pady=3, padx=3, columnspan=6)

txtrgbInt = Label(
    frameLight,
    text="Please, put red, green and blue intensity (0-100%)",
    font=("Arial", 12),
    bg=colorg,
)
txtrgbInt.grid(row=4, column=1, pady=3, padx=3, columnspan=8)

# read values R G B
txtRedInt = Label(frameLight, text="Red light", font=("Arial", 12), bg=colorg)
txtRedInt.grid(row=5, column=2, pady=3, padx=3)
putRedInt = Entry(
    frameLight,
    textvariable=valueRED,
    width=8,
    font=("Arial", 12),
)
putRedInt.grid(row=5, column=3, pady=3, padx=3)

txtGreInt = Label(frameLight, text="Green light", font=("Arial", 12), bg=colorg)
txtGreInt.grid(row=5, column=4, pady=3, padx=3)
putGreInt = Entry(
    frameLight,
    textvariable=valueGRE,
    width=8,
    font=("Arial", 12),
)
putGreInt.grid(row=5, column=5, pady=3, padx=3)

txtBluInt = Label(frameLight, text="Blue light", font=("Arial", 12), bg=colorg)
txtBluInt.grid(row=5, column=6, pady=3, padx=3)
putBluInt = Entry(
    frameLight,
    textvariable=valueBLU,
    width=8,
    font=("Arial", 12),
)
putBluInt.grid(row=5, column=7, pady=3, padx=3)

# Red slider
txtSlidWh = Label(frameLight, text="Red light", font=("Arial", 12), bg=colorg)
txtSlidWh.grid(row=6, column=1, pady=3, padx=3)
WhSlid = Scale(
    frameLight,
    from_=0,
    to=100,
    length=400,
    orient="horizontal",
    variable=valueRED,
    bg=colorg,
)
WhSlid.grid(row=6, column=2, pady=3, padx=3, columnspan=6)

# Green slider
txtSlidWh = Label(frameLight, text="Green light", font=("Arial", 12), bg=colorg)
txtSlidWh.grid(row=7, column=1, pady=3, padx=3)
WhSlid = Scale(
    frameLight,
    from_=0,
    to=100,
    length=400,
    orient="horizontal",
    variable=valueGRE,
    bg=colorg,
)
WhSlid.grid(row=7, column=2, pady=3, padx=3, columnspan=6)

# Blue slider
txtSlidWh = Label(frameLight, text="Blue light", font=("Arial", 12), bg=colorg)
txtSlidWh.grid(row=8, column=1, pady=3, padx=3)
WhSlid = Scale(
    frameLight,
    from_=0,
    to=100,
    length=400,
    orient="horizontal",
    variable=valueBLU,
    bg=colorg,
)
WhSlid.grid(row=8, column=2, pady=3, padx=3, columnspan=6)

# Read value air pump bright
txtPInt = Label(
    frameLight,
    text="Air pump power (0-100%)",
    font=("Arial", 12),
    bg=colorg,
)
txtPInt.grid(row=9, column=3, pady=3, padx=3, columnspan=3)
putPInt = Entry(frameLight, textvariable=valuePmp, width=8, font=("Arial", 12))
putPInt.grid(row=9, column=6, pady=3, padx=3)

# Pump slider
txtSlidPm = Label(frameLight, text="Air pump", font=("Arial", 12), bg=colorg)
txtSlidPm.grid(row=10, column=1, pady=3, padx=3)
PmSlid = Scale(
    frameLight,
    from_=0,
    to=100,
    length=400,
    orient="horizontal",
    variable=valuePmp,
    bg=colorg,
)
PmSlid.grid(row=10, column=2, pady=3, padx=3, columnspan=6)

# -------------------------------------------------------------------------------------------------
# Indicators 3rd tab
txtLg = Label(
    frameConfiguration,
    text="Data logger configuration",
    font=("Arial", 12, "bold"),
    bg=colorg,
)
txtLg.grid(row=1, column=1, pady=3, padx=3, columnspan=6)

txtLog = Label(
    frameConfiguration,
    text="Save data logger",
    font=("Arial", 12),
    bg=colorg,
)
txtLog.grid(row=2, column=3, pady=3, padx=3, sticky="W")
chkLog = Checkbutton(
    frameConfiguration,
    text="Enable",
    font=("Arial", 12),
    variable=logActive,
    onvalue=1,
    offvalue=0,
    bg=colorg,
)
chkLog.grid(row=2, column=4, pady=3, padx=3, sticky="W")

txtFName = Label(
    frameConfiguration,
    text="File name",
    font=("Arial", 12),
    bg=colorg,
)
txtFName.grid(row=3, column=3, pady=3, padx=3, sticky="W")
putFName = Entry(
    frameConfiguration,
    textvariable=valueFName,
    width=12,
    font=("Arial", 12),
)
putFName.grid(row=3, column=4, pady=3, padx=3, sticky="W")

txtRoute = Label(
    frameConfiguration,
    text="File path",
    font=("Arial", 12),
    bg=colorg,
)
txtRoute.grid(row=4, column=1, pady=3, padx=3)
putRoute = Entry(
    frameConfiguration,
    textvariable=valueRoute,
    width=70,
    font=("Arial", 12),
)
putRoute.grid(row=4, column=2, pady=3, padx=3, columnspan=4)
btnRoute = Button(
    frameConfiguration,
    text="Save",
    font=("Arial", 12),
    command=browsepath,
)
btnRoute.grid(row=4, column=6, pady=3, padx=3)


root.after(1000, updateVal)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
