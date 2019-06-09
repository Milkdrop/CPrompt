#! /usr/bin/python3
import subprocess, readline
from datetime import date, datetime
import sys, time, random, string, os

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

Lang = "c"
Compiler = "gcc"

Includes = ["#include <stdio.h>"]
Defines = []
Cmdlist = []
MultiLine = 0

ProgramID = ""
fname = ""
while (os.path.isfile(fname) == True or fname == ""): # Avoid Collisions
	ProgramID = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
	fname = "/tmp/CPython_{}".format(ProgramID)

WelcomeMessage = """CPrompt 0.0.3 (default, {}, {})
- CPrompt Commands are entered using: // Command
- Type '//help' for a list of available commands
Program ID is {}
""".format(date.today().strftime("%B %d %Y"), datetime.now().strftime("%H:%M:%S"), ProgramID)

HelpMessage = """Commands:
- clear / clean\t- Clears program
- setlang c / cpp\t- Sets language as C
"""

print (WelcomeMessage)

while True:
	try:
		PStack = []
		invalid = False
		if (MultiLine == 0):
			cmd = input(">>> ") + "\n"
		else:
			cmd += input ("... ") + "\n"

		for character in cmd:
			if (character == "{"):
				PStack.append(1)
			elif (character == "}"):
				invalid = False
				if (len(PStack) > 0):
					if (PStack[-1] == 1):
						PStack = PStack[:-1]
					else:
						invalid = True
				else:
					invalid = True
			elif (character == "("):
				PStack.append(2)
			elif (character == ")"):
				invalid = False
				if (len(PStack) > 0):
					if (PStack[-1] == 2):
						PStack = PStack[:-1]
					else:
						invalid = True
				else:
					invalid = True
		
		if (len(PStack) == 0 or invalid == True):
			MultiLine = 0
		else:
			MultiLine = 1
		
		if (cmd[:8] == "#include"):
			Includes.append(cmd)
			cmd = "//Include " + cmd
		elif (cmd[:7] == "#define"):
			Defines.append(cmd)
			cmd = "//Define " + cmd
		elif (cmd[:2] == "//"):
			cmd = cmd[2:].strip().lower()
			if (cmd == "help"):
				print (HelpMessage)
			elif (cmd[:7] == "setlang"):
				cmd = cmd.split(" ")[1]
				if (cmd == "c"):
					print ("Language set as C")
					Lang = "c"
					Compiler = "gcc"
				elif (cmd == "cpp"):
					print ("Language set as C++")
					Lang = "cpp"
					Compiler = "g++"
				else:
					print ("Invalid Language: {}".format(cmd))
			elif (cmd[:5] == "clean" or cmd[:5] == "clear"):
				Includes = ["#include <stdio.h>"]
				Defines = []
				Cmdlist = []
				MultiLine = 0
			else:
				print ("Unknown Command: {}".format(cmd))
		else:
			if (MultiLine == 0):
				Cmdlist.append(cmd)
				cmd = "//RegularCmd " + cmd

		Program = ""
		for include in Includes:
			Program += include + "\n"
		for define in Defines:
			Program += define + "\n"
		
		Program += "int main() {\n"
		for _cmd in Cmdlist:
			Program += _cmd
		Program += "\n}"

		if (MultiLine == 0):
			open (fname + "." + Lang, "w").write (Program)
			code = os.system("{2} -w -O2 {0}.{1} -o {0}".format(fname, Lang, Compiler))
	
			if (code == 0):
				output = subprocess.check_output([fname]).decode("utf-8")
				if (output != ""):
					print (output)
					Cmdlist = Cmdlist[:-1]
			else:
				if (cmd[:10] == "//Include "):
					Includes = Includes[:-1]
				elif (cmd[:9] == "//Define "):
					Defines = Defines[:-1]
				else:
					Cmdlist = Cmdlist[:-1]
	except Exception as e:
		print ("Error: {}".format(e))
