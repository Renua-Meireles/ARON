from PyQt5.uic import compileUi
def compilar(nome_interface):
	nome_arq = nome_interface[:-3]+'.py'
	with open(nome_arq,'w') as arq:
		indentar_com_tab = 0
		compileUi(nome_interface,arq,indent=indentar_com_tab)
		arq.seek(0)
		arq.write('#-*- coding:ISO-8859-1 -*-\n#')
